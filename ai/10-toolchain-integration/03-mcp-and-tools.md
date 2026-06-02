# 第3章 MCP 协议与工具系统
# Chapter 3: MCP Protocol & Tool System

> **MCP (Model Context Protocol) is the standardized interface that connects LLMs to the external world. Think of it as "USB-C for AI tools" — a universal protocol that any LLM can use to call any tool, and any tool can expose itself to any LLM.**
>
> **MCP（Model Context Protocol）是连接 LLM 与外部世界的标准化接口。可以把它想象成"AI 工具的 USB-C"——一个通用协议，任何 LLM 都可以用它调用任何工具，任何工具也可以向任何 LLM 暴露自身。**

**前置知识 (Prerequisites):** 了解 Tool Calling（第 9.3 节）、了解 Agent Harness（第 10.2 节）
**配套代码 (Code):** `code/custom_mcp_server.py`

---

## 目录 (Table of Contents)

1. [MCP 协议 (MCP Protocol)](#1-mcp-协议-mcp-protocol)
2. [工具定义与注册 (Tool Definition & Registration)](#2-工具定义与注册-tool-definition--registration)
3. [自定义 MCP 服务器 (Custom MCP Server)](#3-自定义-mcp-服务器-custom-mcp-server)
4. [常见 MCP 实践 (Common MCP Practices)](#4-常见-mcp-实践-common-mcp-practices)
5. [运行示例 (Running Example)](#5-运行示例-running-example)

---

## 1. MCP 协议 (MCP Protocol)

### 1.1 什么是 MCP？

MCP 由 Anthropic 于 2024 年 11 月提出，是一个开放标准协议，定义了 LLM 与外部工具和服务之间的通信方式。它解决了 AI 工具生态中的"碎片化"问题——在此之前，每个 LLM 平台都有自己的工具调用格式（OpenAI Function Calling、Anthropic Tool Use、Google Function Declaration），开发者需要为每个平台编写适配代码。

**核心架构 (Core Architecture):**

```
+------------------+     JSON-RPC      +------------------+     LLM API      +---------------+
|                  | <---------------> |                  | <--------------> |               |
|   MCP Server     |                   |   MCP Client     |                 |     LLM       |
|  (defines tools) |    stdio / SSE    |  (agent harness) |    tool_use     |               |
|                  |                   |                  |                 |               |
+------------------+                   +------------------+                 +---------------+
```

- **MCP Server**: 定义并实现工具。每个工具通过 `name`、`description` 和 `inputSchema`（JSON Schema）描述自己。
- **MCP Client**: Agent Harness 中的组件，负责发现服务器上的工具、将 LLM 的工具请求路由到对应服务器、执行工具并返回结果。
- **LLM**: 通过 Tool Calling 机制生成工具调用指令，MCP Client 将其转换为标准化的 MCP 请求。

### 1.2 传输层 (Transport)

MCP 支持两种传输方式：

| 传输方式 | 协议 | 适用场景 | 特点 |
|---------|------|---------|------|
| **stdio** | 标准输入/输出 | 本地工具 | 零配置、进程隔离、高安全性 |
| **SSE** (Server-Sent Events) | HTTP | 远程工具 | 跨网络、支持多客户端、可扩展 |

**stdio 传输示例 (stdio transport):**

```
+--------------------------------+
|        Agent Process            |
|  +--------------------------+   |
|  |   MCP Client (Parent)    |   |
|  +------------+-------------+   |
|               | spawns          |
|  +------------v-------------+   |
|  |   MCP Server (Child)     |   |
|  |   stdin  <- JSON-RPC     |   |
|  |   stdout -> JSON-RPC     |   |
|  +--------------------------+   |
+--------------------------------+
```

### 1.3 核心方法 (Core Methods)

MCP 协议基于 JSON-RPC 2.0，定义了以下核心方法：

| 方法 | 方向 | 描述 |
|------|------|------|
| `tools/list` | Server -> Client | 列出所有可用工具及其 schema |
| `tools/call` | Client -> Server | 调用指定工具，传入参数 |
| `tools/notify` | Server -> Client | 工具状态变更通知（可选） |

**请求/响应示例 (Request/Response Example):**

```json
// tools/list request
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}

// tools/list response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "calculator",
        "description": "Evaluate a mathematical expression",
        "inputSchema": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Math expression like '2 + 3 * 4'"
            }
          },
          "required": ["expression"]
        }
      }
    ]
  }
}

// tools/call request
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 2,
  "params": {
    "name": "calculator",
    "arguments": {
      "expression": "2 + 3 * 4"
    }
  }
}

// tools/call response
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "14"
      }
    ]
  }
}

// tools/call error response
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": "division by zero"
  }
}
```

### 1.4 生命周期 (Lifecycle)

MCP Server 的生命周期遵循以下流程：

1. **初始化 (Initialize)**: Client 发送 `initialize` 请求，Server 返回支持的协议版本和能力
2. **工具发现 (Discover)**: Client 调用 `tools/list` 获取所有工具定义
3. **工具调用 (Execute)**: Client 根据 LLM 的请求调用 `tools/call`
4. **关闭 (Shutdown)**: Client 发送关闭信号，Server 清理资源并退出

```
Client                               Server
  |                                    |
  +-- initialize ------------------->  |
  | <-- initialized(version, caps) ---+
  |                                    |
  +-- tools/list ------------------->  |
  | <-- tool_definitions -------------+
  |                                    |
  +-- tools/call(name="calc", args) -> |
  | <-- result/error -----------------+
  |                                    |
  +-- tools/call(name="search", args)->|
  | <-- result/error -----------------+
  |                                    |
  +-- shutdown ----------------------> |
  | <-- exited -----------------------+
```

---

## 2. 工具定义与注册 (Tool Definition & Registration)

### 2.1 工具描述规范

每个 MCP 工具由三部分组成：

```python
ToolDefinition = {
    "name": str,            # 工具名称，唯一标识
    "description": str,     # 自然语言描述，帮助 LLM 理解何时使用
    "inputSchema": {        # JSON Schema，定义参数结构
        "type": "object",
        "properties": { ... },
        "required": [...]
    }
}
```

**好的描述 vs 不好的描述 (Good vs Bad Descriptions):**

| 类型 | 示例 | 评价 |
|------|------|------|
| 模糊 | `"A calculator tool"` | LLM 不知道何时使用 |
| 清晰 | `"Evaluate mathematical expressions. Use for arithmetic, algebra, or any numeric computation."` | LLM 能准确判断 |
| 缺失参数说明 | 没有描述每个参数的含义 | LLM 可能传错参数 |
| 完整参数说明 | 每个参数都有 description 和示例值 | LLM 能正确调用 |

### 2.2 工具调用流程 (Tool Call Flow)

完整的工具调用流程包含以下步骤：

```
Step 1: LLM 生成工具调用
---------------------------------
LLM output: {"name": "calculator", "arguments": {"expression": "2+3*4"}}

Step 2: MCP Client 解析并路由
---------------------------------
Client 解析 LLM 输出 -> 提取 name 和 arguments
-> 在注册表中查找对应的 tool handler
-> 验证参数是否符合 inputSchema

Step 3: MCP Server 执行工具
---------------------------------
handler("calculator", {"expression": "2+3*4"})
-> 计算表达式 -> 返回结果 "14"

Step 4: Client 将结果返回给 LLM
---------------------------------
Client 将结果包装为 tool_result 格式
-> 发送给 LLM 继续生成回复

Step 5: LLM 生成最终回复
---------------------------------
LLM: "The result is 14."
```

### 2.3 参数验证 (Parameter Validation)

MCP Server 在调用工具前应验证参数：

```python
def validate_arguments(schema: dict, args: dict) -> list[str]:
    """Validate arguments against JSON Schema. Returns list of errors."""
    errors = []

    # Check required fields
    for field in schema.get("required", []):
        if field not in args:
            errors.append(f"Missing required field: '{field}'")

    # Check types
    for field, value in args.items():
        if field in schema.get("properties", {}):
            prop = schema["properties"][field]
            expected_type = prop.get("type")
            if expected_type == "string" and not isinstance(value, str):
                errors.append(f"Field '{field}' should be string, got {type(value).__name__}")
            elif expected_type == "number" and not isinstance(value, (int, float)):
                errors.append(f"Field '{field}' should be number, got {type(value).__name__}")

    return errors
```

### 2.4 工具注册表 (Tool Registry)

工具注册表是 MCP Client 的核心组件，维护 name -> handler 的映射：

```python
class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}
        self._handlers: dict[str, Callable] = {}

    def register(self, name: str, description: str,
                 input_schema: dict, handler: Callable):
        self._tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema
        }
        self._handlers[name] = handler

    def list_tools(self) -> list[dict]:
        return list(self._tools.values())

    def call_tool(self, name: str, arguments: dict) -> dict:
        if name not in self._handlers:
            return {"error": {"code": -32601, "message": f"Tool not found: {name}"}}
        try:
            result = self._handlers[name](**arguments)
            return {"content": [{"type": "text", "text": str(result)}]}
        except Exception as e:
            return {"error": {"code": -32603, "message": str(e)}}
```

---

## 3. 自定义 MCP 服务器 (Custom MCP Server)

### 3.1 从零开始构建 (Building from Scratch)

本节的配套代码 `code/custom_mcp_server.py` 实现了一个完整的、从零构建的 MCP 服务器，不依赖任何第三方 MCP SDK。它包含：

- **MCP 协议实现**: JSON-RPC 2.0 请求/响应处理
- **三个工具**: calculator（计算器）、file_read（文件读取）、search（文本搜索）
- **工具发现与调用**: 完整的 `tools/list` 和 `tools/call` 流程
- **错误处理**: 参数验证、工具不存在、运行时异常
- **stdio 传输**: 通过标准输入输出通信
- **MCP Client**: 一个内嵌的客户端用于演示

### 3.2 核心实现架构 (Core Architecture)

```python
# Server 端核心逻辑
class MCPServer:
    def __init__(self):
        self.tools: dict[str, ToolDef] = {}

    def register_tool(self, name, description, input_schema, handler):
        self.tools[name] = ToolDef(name, description, input_schema, handler)

    def handle_request(self, request: dict) -> dict:
        method = request.get("method")
        if method == "tools/list":
            return self._handle_list()
        elif method == "tools/call":
            return self._handle_call(request.get("params", {}))
        else:
            return {"error": {"code": -32601, "message": f"Method not found: {method}"}}

    def _handle_list(self) -> dict:
        return {
            "result": {
                "tools": [t.definition() for t in self.tools.values()]
            }
        }

    def _handle_call(self, params: dict) -> dict:
        name = params.get("name")
        args = params.get("arguments", {})
        if name not in self.tools:
            return {"error": {"code": -32602, "message": f"Unknown tool: {name}"}}
        try:
            result = self.tools[name].handler(**args)
            return {"result": {"content": [{"type": "text", "text": str(result)}]}}
        except Exception as e:
            return {"error": {"code": -32603, "message": str(e)}}
```

### 3.3 工具实现示例 (Tool Implementation)

**Calculator 工具 (Calculator Tool):**

```python
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    allowed = set("0123456789+-*/.()% ")
    if not all(c in allowed for c in expression):
        raise ValueError("Expression contains invalid characters")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{result}"
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")
```

**File Read 工具 (File Read Tool):**

```python
def file_read(path: str, max_chars: int = 500) -> str:
    """Read contents of a file with safety restrictions."""
    if ".." in path:
        raise PermissionError("Path traversal detected")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Not a file: {path}")
    if os.path.getsize(path) > 1024 * 1024:
        raise ValueError("File too large (>1MB)")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read(max_chars)
    return content
```

**Search 工具 (Search Tool):**

```python
def search_text(pattern: str, path: str = ".") -> str:
    """Search for a pattern in files within a directory."""
    if ".." in path:
        raise PermissionError("Path traversal detected")
    results = []
    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.startswith("."):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if pattern in line:
                            results.append(f"{fpath}:{i}: {line.strip()[:100]}")
                            if len(results) >= 20:
                                break
            except Exception:
                continue
    if not results:
        return f"No matches found for '{pattern}'"
    return "\n".join(results)
```

### 3.4 启动方式 (Starting the Server)

**作为独立进程 (Standalone):**

```bash
$ python ai/10-toolchain-integration/code/custom_mcp_server.py

=== MCP Server Started (d:emo transport) ===
Server PID: 12345
Listening on stdin/stdout for JSON-RPC messages.
Type 'quit' to exit, or send JSON-RPC requests.
```

**通过 MCP Inspector 测试 (Testing with MCP Inspector):**

MCP Inspector 是官方提供的调试工具，可以可视化地测试 MCP Server：

```bash
npx @anthropic/mcp-inspector python ai/10-toolchain-integration/code/custom_mcp_server.py
```

### 3.5 使用 Python SDK（官方推荐）

虽然我们的配套代码是从零构建的，但在生产环境中推荐使用官方的 MCP Python SDK：

```python
# 使用 MCP SDK（需要安装：pip install mcp）
from mcp.server import Server, stdio_server

app = Server("my-tool-server")

@app.tool()
def my_tool(param: str) -> str:
    return f"Hello, {param}"

if __name__ == "__main__":
    stdio_server.run(app)
```

使用 SDK 的优势：
- 自动处理 JSON-RPC 序列化/反序列化
- 内置参数类型校验（通过 Python 类型注解）
- 自动生成 JSON Schema
- 支持 SSE 传输（通过 `sse_server`）

---

## 4. 常见 MCP 实践 (Common MCP Practices)

### 4.1 SSH 工具 (SSH Tool)

**用途 (Use Case):** 在远程服务器上执行命令，用于运维自动化、部署、日志查看等。

```python
def ssh_execute(host: str, command: str, username: str = "root") -> str:
    """Execute a command on a remote server via SSH."""
    import subprocess
    ssh_cmd = ["ssh", f"{username}@{host}", command]
    result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return f"Error (exit {result.returncode}): {result.stderr}"
    return result.stdout
```

**风险与注意事项 (Risks & Considerations):**

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| 命令注入 | LLM 可能生成恶意命令 | 限制允许的命令列表；使用白名单 |
| 权限泄露 | SSH 密钥可能被滥用 | 使用专用只读密钥；限制目标主机 |
| 资源滥用 | 执行耗时命令阻塞服务器 | 设置超时；限制并发数 |
| 数据泄露 | 敏感信息被读回 | 对输出进行过滤；限制可访问的路径 |

**权限设计建议 (Permission Design):**
- SSH 工具应默认**禁止**，需要用户显式授权
- 每次执行前应向用户展示将要执行的命令
- 记录所有 SSH 操作的审计日志

### 4.2 Docker 工具 (Docker Tool)

**用途 (Use Case):** 管理容器生命周期——创建、启动、停止、查看日志。

```python
def docker_exec(container_name: str, command: str) -> str:
    """Execute a command inside a Docker container."""
    import subprocess
    cmd = ["docker", "exec", container_name] + command.split()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout

def docker_logs(container_name: str, tail: int = 100) -> str:
    """Fetch logs from a Docker container."""
    import subprocess
    cmd = ["docker", "logs", "--tail", str(tail), container_name]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.stdout or result.stderr
```

**安全建议 (Security Recommendations):**

| 原则 | 说明 |
|------|------|
| 避免 `docker run` | 创建新容器可能导致资源耗尽 |
| 限定 `docker exec` | 只在已有容器中执行命令 |
| 只读模式 | 使用 `--read-only` 挂载的容器 |
| 资源限制 | 使用 Docker 的 CPU/内存限制 |

### 4.3 数据库工具 (Database Tool)

**用途 (Use Case):** 对数据库执行只读查询（SELECT），用于数据分析、运维检查。

```python
import sqlite3

def db_query(database: str, query: str, limit: int = 100) -> str:
    """Execute a read-only SQL query on a SQLite database."""
    query_upper = query.strip().upper()
    if not query_upper.startswith("SELECT"):
        raise PermissionError("Only SELECT queries are allowed")

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(query)
    rows = cursor.fetchmany(limit)
    conn.close()

    if not rows:
        return "No results."

    headers = rows[0].keys()
    result = " | ".join(headers) + "\n"
    result += "-" * len(result) + "\n"
    for row in rows:
        result += " | ".join(str(v)[:30] for v in row) + "\n"
    return result
```

**重要原则 (Important Principles):**

| 原则 | 说明 |
|------|------|
| **只读强制** | 禁止 INSERT/UPDATE/DELETE/DDL |
| **行数限制** | 防止返回过多数据导致 token 溢出 |
| **超时控制** | 防止慢查询阻塞服务器 |
| **禁止动态表名** | 防止 SQL 注入 |
| **连接池管理** | 避免资源泄露 |

### 4.4 通用安全模式 (General Security Patterns)

无论实现哪种工具的 MCP Server，都应遵循以下安全模式：

```python
class ToolSecurity:
    """Security patterns applicable to all MCP tools."""

    @staticmethod
    def validate_path(path: str, allowed_dirs: list[str]) -> str:
        """Prevent path traversal attacks."""
        real_path = os.path.realpath(path)
        for allowed in allowed_dirs:
            allowed_real = os.path.realpath(allowed)
            if real_path.startswith(allowed_real):
                return real_path
        raise PermissionError(f"Access denied: {path}")

    @staticmethod
    def sanitize_output(text: str, max_length: int = 10000) -> str:
        """Limit output size and remove sensitive patterns."""
        import re
        text = re.sub(r'(?i)(password|secret|token|key)[=:]\s*\S+',
                      r'\1=***', text)
        return text[:max_length]
```

### 4.5 MCP 服务器类型对比

| 工具类型 | 复杂度 | 风险等级 | 典型用途 |
|---------|--------|---------|---------|
| Calculator | * | 低 | 数学计算 |
| File Read | ** | 中 | 读取文件内容 |
| File Write | ** | 高 | 写入/修改文件 |
| Search | ** | 低 | 文本搜索 |
| SSH | *** | 高 | 远程命令执行 |
| Docker | *** | 高 | 容器管理 |
| Database | ** | 高 | 数据查询 |
| Web Fetch | ** | 中 | 网络请求 |
| Code Execute | *** | 高 | 运行任意代码 |

---

## 5. 运行示例 (Running Example)

启动配套的 MCP 服务器，观察完整的工具调用流程：

```bash
$ python ai/10-toolchain-integration/code/custom_mcp_server.py
```

**预期输出 (Expected Output):**

```
--------------------------------------------------------
  DEMO: MCP Protocol -- Tool Discovery & Calling
--------------------------------------------------------

--------------------------------------------------------
  Part 1: Tool Discovery (tools/list)
--------------------------------------------------------
  >>> tools/list
  <<< Found 3 tools:
      [0] calculator
          Description: Evaluate a mathematical expression...
          Parameters: ['expression']
          Required: ['expression']
      [1] file_read
          Description: Read the contents of a file...
          Parameters: ['path', 'max_chars']
          Required: ['path']
      [2] search
          Description: Search for a text pattern in files...
          Parameters: ['pattern', 'path']
          Required: ['pattern']

--------------------------------------------------------
  Part 2: Tool Calling (tools/call)
--------------------------------------------------------
  >>> tools/call(name="calculator", arguments={"expression": "2 + 3 * 4"})
  <<< 14

  >>> tools/call(name="calculator", arguments={"expression": "(42 + 3.14) * 2"})
  <<< 90.28

--------------------------------------------------------
  Part 3: Error Handling
--------------------------------------------------------
  >>> tools/call(name="unknown_tool")
  <<< Error (-32601): Tool not found: 'unknown_tool'

  >>> tools/call(name="calculator", arguments={"expression": "1/0"})
  <<< Error (-32603): Division by zero is not allowed

  >>> tools/call(name="file_read", arguments={"path": "../../etc/passwd"})
  <<< Error (-32603): Path traversal detected: '..' is not allowed

  >>> tools/call(name="calculator", arguments={"expression": "__import__(...)..."})
  <<< Error (-32603): Expression contains invalid characters
```

完整的代码实现和运行说明请参见配套文件 `code/custom_mcp_server.py`。

---

> **MCP 是 AI 工具生态的关键协议。** 理解它不仅能帮助你构建更强大的 Agent，也能让你更深入地理解现代 AI 编码助手的工作方式。掌握了 MCP，你就掌握了让 LLM 连接世界的钥匙。
>
> **MCP is the key protocol for the AI tool ecosystem.** Understanding it helps you build more powerful agents and deepens your understanding of how modern AI coding assistants work. Master MCP, and you hold the key to connecting LLMs with the world.
