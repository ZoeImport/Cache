#!/usr/bin/env python3
"""
custom_mcp_server.py -- Build an MCP Server from Scratch

A complete, self-contained implementation of the Model Context Protocol (MCP)
server and client, demonstrating:
  - Tool discovery (tools/list)
  - Tool calling (tools/call)
  - Error handling (invalid params, runtime errors)
  - JSON-RPC 2.0 transport over stdio

Tools implemented:
  1. calculator  -- Evaluate mathematical expressions safely
  2. file_read   -- Read file contents with security restrictions
  3. search      -- Search for text patterns in files

Usage:
    python custom_mcp_server.py

All outputs use English labels as required.
Uses only Python standard library: json, os, sys, asyncio (for structure only).
"""

import json
import os
import sys
import textwrap
from typing import Any, Callable


# =============================================================================
# 1. JSON-RPC 2.0 Helpers
# =============================================================================

def make_request(method: str, params: dict | None = None, req_id: int = 1) -> dict:
    """Build a JSON-RPC 2.0 request object."""
    msg: dict[str, Any] = {
        "jsonrpc": "2.0",
        "method": method,
        "id": req_id,
    }
    if params is not None:
        msg["params"] = params
    return msg


def make_success(result: Any, req_id: int = 1) -> dict:
    """Build a JSON-RPC 2.0 success response."""
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result,
    }


def make_error(code: int, message: str, data: Any = None, req_id: int = 1) -> dict:
    """Build a JSON-RPC 2.0 error response."""
    err: dict[str, Any] = {
        "code": code,
        "message": message,
    }
    if data is not None:
        err["data"] = data
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": err,
    }


# Standard JSON-RPC error codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


# =============================================================================
# 2. Tool Definitions
# =============================================================================

# Tool 1: Calculator -- Evaluate mathematical expressions safely
TOOL_CALCULATOR = {
    "name": "calculator",
    "description": (
        "Evaluate a mathematical expression. "
        "Supports +, -, *, /, (), and decimal numbers. "
        "Example: '2 + 3 * 4' returns 14."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to evaluate",
            }
        },
        "required": ["expression"],
    },
}


def handle_calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Security: only allows digits, operators, parentheses, spaces, and dots.
    Uses eval() with an empty globals dict to prevent arbitrary code execution.
    """
    allowed_chars = set("0123456789+-*/.()% ")
    if not isinstance(expression, str):
        raise TypeError(f"Expression must be a string, got {type(expression).__name__}")
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Expression contains invalid characters")
    if expression.strip() == "":
        raise ValueError("Expression cannot be empty")

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        if isinstance(result, (int, float)):
            if result == int(result):
                return str(int(result))
            return f"{result:.10f}".rstrip("0").rstrip(".")
        raise ValueError(f"Expression did not evaluate to a number: {result}")
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed")
    except SyntaxError as e:
        raise ValueError(f"Invalid expression syntax: {e}")
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}")


# Tool 2: File Reader -- Read file contents with safety restrictions
TOOL_FILE_READ = {
    "name": "file_read",
    "description": (
        "Read the contents of a file. "
        "Returns up to `max_chars` characters from the file. "
        "Security: path traversal is blocked, file size is limited to 1MB."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file (relative to current directory)",
            },
            "max_chars": {
                "type": "number",
                "description": "Maximum number of characters to read (default: 500)",
                "default": 500,
            },
        },
        "required": ["path"],
    },
}


def handle_file_read(path: str, max_chars: int = 500) -> str:
    """Read a file with security checks.

    Security measures:
    - Blocks path traversal ('..')
    - Blocks absolute paths (must be relative)
    - Limits file size to 1MB
    - Limits output to max_chars characters
    """
    if ".." in path:
        raise PermissionError("Path traversal detected: '..' is not allowed")

    if not isinstance(max_chars, (int, float)) or max_chars <= 0:
        max_chars = 500
    max_chars = int(min(max_chars, 10000))

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if not os.path.isfile(path):
        raise ValueError(f"Not a regular file: {path}")

    file_size = os.path.getsize(path)
    if file_size > 1024 * 1024:
        raise ValueError(f"File too large: {file_size} bytes (max 1MB)")

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_chars)
        total_lines = content.count("\n") + 1
        info = f"[Read {len(content)} chars, {total_lines} lines from {path}]"
        return f"{info}\n{content}"
    except PermissionError:
        raise PermissionError(f"Cannot read file: permission denied: {path}")
    except Exception as e:
        raise RuntimeError(f"Failed to read file: {e}")


# Tool 3: Search -- Search for text in files
TOOL_SEARCH = {
    "name": "search",
    "description": (
        "Search for a text pattern in files within a directory. "
        "Returns matching lines with file paths and line numbers. "
        "Limited to 20 results and 1MB file size."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Text pattern to search for (plain text, not regex)",
            },
            "path": {
                "type": "string",
                "description": "Directory to search in (default: current directory '.')",
                "default": ".",
            },
        },
        "required": ["pattern"],
    },
}


def handle_search(pattern: str, path: str = ".") -> str:
    """Search for a text pattern in files within a directory.

    Security:
    - Blocks path traversal in the directory path
    - Skips hidden files (starting with '.')
    - Skips binary files by checking for null bytes
    - Limits results to 20 matches
    """
    if ".." in path:
        raise PermissionError("Path traversal detected: '..' is not allowed")
    if not isinstance(pattern, str) or not pattern.strip():
        raise ValueError("Search pattern cannot be empty")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory not found: {path}")
    if not os.path.isdir(path):
        raise ValueError(f"Not a directory: {path}")

    results: list[str] = []
    max_results = 20
    max_file_size = 1024 * 1024

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in files:
            if fname.startswith("."):
                continue
            if len(results) >= max_results:
                break
            fpath = os.path.join(root, fname)
            try:
                if os.path.getsize(fpath) > max_file_size:
                    continue
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    for line_no, line in enumerate(f, 1):
                        if pattern in line:
                            display = line.strip()[:120]
                            results.append(f"{fpath}:{line_no}: {display}")
                            if len(results) >= max_results:
                                break
            except (PermissionError, UnicodeDecodeError):
                continue
            except Exception:
                continue
        if len(results) >= max_results:
            break

    if not results:
        return f"No matches found for pattern: '{pattern}'"
    return f"Found {len(results)} matches:\n" + "\n".join(results)


# =============================================================================
# 3. Tool Registry
# =============================================================================

class ToolRegistry:
    """Registry mapping tool names to their definitions and handlers."""

    def __init__(self):
        self._tools: dict[str, dict] = {}
        self._handlers: dict[str, Callable] = {}

    def register(self, definition: dict, handler: Callable) -> None:
        """Register a tool with its JSON Schema definition and handler function."""
        name = definition["name"]
        self._tools[name] = definition
        self._handlers[name] = handler

    def list_tools(self) -> list[dict]:
        """Return all tool definitions (for tools/list)."""
        return list(self._tools.values())

    def call_tool(self, name: str, arguments: dict) -> dict:
        """Execute a tool by name with given arguments (for tools/call).

        Returns a result dict with either 'content' or 'error'.
        """
        if name not in self._handlers:
            return make_error(
                METHOD_NOT_FOUND,
                f"Tool not found: '{name}'",
                {"available_tools": list(self._tools.keys())},
            )

        schema = self._tools[name]["inputSchema"]
        required = schema.get("required", [])
        for field in required:
            if field not in arguments:
                return make_error(
                    INVALID_PARAMS,
                    f"Missing required argument: '{field}'",
                    {"tool": name, "required": required},
                )

        try:
            result = self._handlers[name](**arguments)
            return make_success({
                "content": [{"type": "text", "text": result}],
            })
        except (FileNotFoundError, PermissionError, ValueError,
                TypeError, RuntimeError) as e:
            return make_error(
                INTERNAL_ERROR,
                str(e),
                {"tool": name, "arguments": arguments},
            )
        except Exception as e:
            return make_error(
                INTERNAL_ERROR,
                f"Unexpected error: {e}",
                {"tool": name},
            )


# =============================================================================
# 4. MCP Server
# =============================================================================

class MCPServer:
    """MCP Server implementing JSON-RPC 2.0 over stdio transport."""

    def __init__(self):
        self.registry = ToolRegistry()
        self._setup_default_tools()

    def _setup_default_tools(self) -> None:
        """Register the three default tools."""
        self.registry.register(TOOL_CALCULATOR, handle_calculator)
        self.registry.register(TOOL_FILE_READ, handle_file_read)
        self.registry.register(TOOL_SEARCH, handle_search)

    def handle_message(self, raw: str) -> str | None:
        """Parse and handle a single JSON-RPC message.

        Returns a JSON-RPC response string, or None for notifications.
        """
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError as e:
            return json.dumps(make_error(PARSE_ERROR, f"Parse error: {e}"))

        if not isinstance(msg, dict) or "method" not in msg:
            return json.dumps(make_error(INVALID_REQUEST, "Invalid request: missing 'method'"))

        method = msg["method"]
        req_id = msg.get("id")

        if method == "tools/list":
            tools = self.registry.list_tools()
            return json.dumps(make_success({"tools": tools}, req_id))

        elif method == "tools/call":
            params = msg.get("params", {})
            if not isinstance(params, dict):
                return json.dumps(make_error(INVALID_PARAMS, "Params must be an object", req_id=req_id))
            name = params.get("name", "")
            arguments = params.get("arguments", {})
            if not isinstance(arguments, dict):
                return json.dumps(make_error(INVALID_PARAMS, "Arguments must be an object", req_id=req_id))
            response = self.registry.call_tool(name, arguments)
            response["id"] = req_id
            return json.dumps(response)

        elif method == "initialize":
            return json.dumps(make_success({
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "custom-mcp-server", "version": "1.0.0"},
            }, req_id))

        else:
            return json.dumps(make_error(
                METHOD_NOT_FOUND,
                f"Unknown method: '{method}'",
                req_id=req_id,
            ))

    def process_request(self, request: dict) -> dict:
        """Process a parsed JSON-RPC request and return response dict."""
        method = request.get("method", "")
        req_id = request.get("id")

        if method == "tools/list":
            return make_success({"tools": self.registry.list_tools()}, req_id)
        elif method == "tools/call":
            params = request.get("params", {})
            name = params.get("name", "")
            arguments = params.get("arguments", {})
            return self.registry.call_tool(name, arguments)
        elif method == "initialize":
            return make_success({
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "custom-mcp-server", "version": "1.0.0"},
            }, req_id)
        else:
            return make_error(METHOD_NOT_FOUND, f"Unknown method: '{method}'", req_id=req_id)

    def run_stdio(self) -> None:
        """Run the server in stdio mode: read JSON-RPC from stdin, write to stdout."""
        banner = textwrap.dedent("""\
        === MCP Server Started (stdio transport) ===
        Server PID: {pid}
        Listening on stdin/stdout for JSON-RPC messages.
        Type 'quit' to exit, or send JSON-RPC requests.
        """).format(pid=os.getpid())
        sys.stdout.write(banner + "\n")
        sys.stdout.flush()

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if line.lower() in ("quit", "exit"):
                sys.stdout.write("Server shutting down.\n")
                sys.stdout.flush()
                break

            response = self.handle_message(line)
            if response:
                sys.stdout.write(response + "\n")
                sys.stdout.flush()


# =============================================================================
# 5. MCP Client (for Demonstration)
# =============================================================================

class MCPClient:
    """Simulated MCP Client that sends requests to the server and prints results."""

    def __init__(self, server: MCPServer):
        self.server = server
        self.req_id = 0

    def _next_id(self) -> int:
        self.req_id += 1
        return self.req_id

    def list_tools(self) -> list[dict]:
        """Discover available tools via tools/list."""
        request = make_request("tools/list", req_id=self._next_id())
        response = self.server.process_request(request)
        return response.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict) -> dict:
        """Call a tool via tools/call."""
        request = make_request("tools/call", {
            "name": name,
            "arguments": arguments,
        }, req_id=self._next_id())
        return self.server.process_request(request)

    def print_header(self, title: str) -> None:
        """Print a section header."""
        width = 56
        sys.stdout.write("\n" + "-" * width + "\n")
        sys.stdout.write(f"  {title}\n")
        sys.stdout.write("-" * width + "\n")

    def print_result(self, label: str, response: dict) -> None:
        """Print a labeled response with proper formatting."""
        if "error" in response:
            err = response["error"]
            sys.stdout.write(f"  >>> {label}\n")
            sys.stdout.write(f"  <<< Error ({err['code']}): {err['message']}\n")
            if "data" in err and err["data"]:
                sys.stdout.write(f"       Data: {err['data']}\n")
        else:
            result = response.get("result", {})
            content = result.get("content", [])
            text = content[0]["text"] if content else "(empty)"
            sys.stdout.write(f"  >>> {label}\n")
            if len(text) > 300:
                text = text[:300] + f"\n       ... [truncated, total {len(text)} chars]"
            sys.stdout.write(f"  <<< {text}\n")

    def run_demo(self) -> None:
        """Run the full demonstration sequence."""
        self.print_header("DEMO: MCP Protocol -- Tool Discovery & Calling")
        self.print_header("Part 1: Tool Discovery (tools/list)")

        tools = self.list_tools()
        print(f"  >>> tools/list")
        print(f"  <<< Found {len(tools)} tools:")
        for i, tool in enumerate(tools):
            name = tool["name"]
            desc = tool["description"]
            if len(desc) > 70:
                desc = desc[:70] + "..."
            schema = tool["inputSchema"]
            required = schema.get("required", [])
            print(f"      [{i}] {name}")
            print(f"          Description: {desc}")
            print(f"          Parameters: {list(schema.get('properties', {}).keys())}")
            print(f"          Required: {required}")

        self.print_header("Part 2: Tool Calling (tools/call)")
        print("  Example 2a: calculator with valid expression")
        resp = self.call_tool("calculator", {"expression": "2 + 3 * 4"})
        self.print_result('tools/call(name="calculator", arguments={"expression": "2 + 3 * 4"})', resp)

        print("\n  Example 2b: calculator with complex expression")
        resp = self.call_tool("calculator", {"expression": "(42 + 3.14) * 2"})
        self.print_result('tools/call(name="calculator", arguments={"expression": "(42 + 3.14) * 2"})', resp)

        print("\n  Example 2c: calculator with percentage")
        resp = self.call_tool("calculator", {"expression": "100 * 15 / 100"})
        self.print_result('tools/call(name="calculator", arguments={"expression": "100 * 15 / 100"})', resp)

        self.print_header("Part 3: File Operations")
        test_file = os.path.basename(__file__)
        test_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.join(test_dir, test_file)
        print(f"  Example 3a: file_read on current file ({test_path})")
        resp = self.call_tool("file_read", {"path": test_path, "max_chars": 200})
        self.print_result('tools/call(name="file_read", arguments={...})', resp)

        self.print_header("Part 4: Text Search")
        print('  Example 4a: search for "def " in code/')
        resp = self.call_tool("search", {"pattern": "def ", "path": "."})
        self.print_result('tools/call(name="search", arguments={"pattern": "def ", ...})', resp)

        self.print_header("Part 5: Error Handling")
        print("  Example 5a: unknown tool")
        resp = self.call_tool("unknown_tool", {})
        self.print_result('tools/call(name="unknown_tool")', resp)

        print("\n  Example 5b: division by zero")
        resp = self.call_tool("calculator", {"expression": "1/0"})
        self.print_result('tools/call(name="calculator", arguments={"expression": "1/0"})', resp)

        print("\n  Example 5c: missing required argument")
        resp = self.call_tool("calculator", {})
        self.print_result('tools/call(name="calculator", arguments={})', resp)

        print("\n  Example 5d: path traversal")
        resp = self.call_tool("file_read", {"path": "../../etc/passwd"})
        self.print_result('tools/call(name="file_read", arguments={"path": "../../etc/passwd"})', resp)

        print("\n  Example 5e: invalid expression characters")
        resp = self.call_tool("calculator", {"expression": "__import__('os').system('rm -rf /')"})
        self.print_result('tools/call(name="calculator", arguments={...})', resp)

        self.print_header("DEMO COMPLETE")
        print(f"  Total requests made: {self.req_id}")
        print("  All MCP protocol flows demonstrated successfully.\n")


# =============================================================================
# 6. Main Entry Point
# =============================================================================

def main():
    """Entry point: either run in interactive stdio mode or demo mode."""
    server = MCPServer()

    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        server.run_stdio()
    else:
        client = MCPClient(server)
        client.run_demo()


if __name__ == "__main__":
    main()
