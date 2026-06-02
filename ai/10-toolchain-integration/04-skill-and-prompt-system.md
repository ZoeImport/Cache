# 第4章 技能与提示词系统
# Chapter 4: Skill & Prompt System

> **Skills are the modular units of AI capability. A skill bundles a specialized prompt with tool permissions and execution constraints, turning a general-purpose LLM into a domain-specific agent. This chapter covers how skills are defined, loaded, injected into prompts, and composed into multi-agent workflows.**
>
> **技能是 AI 能力的模块化单元。一个技能将专用提示词与工具权限和执行约束捆绑在一起，将通用 LLM 转变为特定领域的智能体。本章涵盖技能的定义、加载、注入到提示词中，以及编排多智能体工作流。**

**前置知识 (Prerequisites):** Agent Harness（第 10.2 节）、MCP 协议与工具系统（第 10.3 节）
**配套代码 (Code):** `code/custom_skill.py`

---

## 目录 (Table of Contents)

1. [技能设计模式 (Skill Design Patterns)](#1-技能设计模式-skill-design-patterns)
2. [Prompt 层级结构 (Prompt Hierarchy)](#2-prompt-层级结构-prompt-hierarchy)
3. [上下文窗口优化 (Context Window Optimization)](#3-上下文窗口优化-context-window-optimization)
4. [多 Agent 协作 (Multi-Agent Workflows)](#4-多-agent-协作-multi-agent-workflows)
5. [运行示例 (Running Example)](#5-运行示例-running-example)

---

## 1. 技能设计模式 (Skill Design Patterns)

### 1.1 什么是技能？(What is a Skill?)

A skill is a structured bundle of three components:

```
+------------------------------------------------------+
|                   SKILL DEFINITION                     |
|                                                        |
|  +------------------+  +--------------+  +-----------+ |
|  |  Specialized     |  |  Tool        |  | Execution | |
|  |  Prompt          |  |  Permissions |  | Constraints| |
|  |  (behavioral     |  |  (what tools |  | (timeouts, | |
|  |   instructions)  |  |   it can use)|  |  budgets)  | |
|  +------------------+  +--------------+  +-----------+ |
+------------------------------------------------------+
```

技能 = 专用提示词 + 工具权限 + 执行约束。每个技能解决一个特定领域的问题，而不是一个通用智能体。

### 1.2 技能类型 (Skill Types)

| 类型 | 描述 | 示例工具 | 权限 |
|------|------|---------|------|
| **Research** | 信息检索与整合 | `web_search`, `web_fetch` | 网络访问 |
| **Coding** | 代码编写、审查、调试 | `file_read`, `file_write`, `command_run` | 文件系统、执行 |
| **System** | 系统管理与运维 | `service_status`, `config_edit`, `log_tail` | 文件系统、执行 |

### 1.3 技能定义格式 (Skill Definition Format)

Skills are defined in YAML with four sections: metadata, prompt, tools, and constraints.

**完整技能定义 (Complete Skill Definition):**

```yaml
name: web_researcher
version: 1.0.0
description: >
  Research any topic by searching the web, fetching pages, and
  extracting structured information from online sources.

prompt: |
  You are a Web Research specialist.
  - Search the web using the search tool for current information.
  - Fetch full page content when you need detailed context.
  - Extract structured data (tables, lists, key facts) from pages.
  - Cite your sources with URLs in every response.

tools:
  - name: web_search
    description: Search the web for a query. Returns top results with snippets.
    permissions: [network]
  - name: web_fetch
    description: Fetch the full content of a URL. Returns markdown.
    permissions: [network]

permissions:
  network: true
  filesystem: false
  execution: false

constraints:
  max_tokens: 4096
  timeout_ms: 30000
  allowed_domains: ["*"]
```

### 1.4 技能加载流程 (Skill Loading Pipeline)

```
Skill Registry (YAML files)
    |
    v
YAML Parser (validate schema)
    |
    v
Skill Object (in-memory representation)
    |
    v
Permission Checker (verify constraints)
    |
    v
Prompt Injector (merge into system prompt)
    |
    v
LLM Runtime (execute with injected context)
```

**实际运行输出 (Actual Console Output):**

```
$ python custom_skill.py

  Phase 1: Loading Skill Definitions from YAML
========================================================================
Loaded 3 skills:
  [web_researcher  ] v1.0.0  |  2 tools  |  permissions: network
  [code_writer     ] v2.1.0  |  3 tools  |  permissions: filesystem, execution
  [system_admin    ] v1.2.0  |  3 tools  |  permissions: filesystem, execution
```

The loader scans a directory for `.yaml` files, parses each into a `Skill` object, validates required fields (name, prompt, tools), and registers them in a dictionary keyed by skill name.

---

## 2. Prompt 层级结构 (Prompt Hierarchy)

### 2.1 四层模型 (4-Level Model)

The system prompt follows a strict hierarchy. Each level constrains the next. Lower levels override higher levels for specific behavior.

```
Level 0: Engine Prompt (core identity, rarely changes)
+----------------------------------------------------------+
| You are an AI assistant with dynamic skill injection.     |
| Your core capabilities include: reasoning, planning,      |
| and tool use. Always follow the active skill's instructions. |
+----------------------------------------------------------+
                            |
Level 1: Skill Prompt (injected at load time)
+----------------------------------------------------------+
| --- Active Skill: web_researcher v1.0.0 ---               |
| Research any topic by searching the web...                |
| You are a Web Research specialist.                        |
| - Search the web for current information.                 |
| - Cite your sources with URLs in every response.          |
| Available tools:                                          |
|   - web_search: Search the web for a query...             |
|   - web_fetch: Fetch the full content of a URL...         |
| Constraints:                                              |
|   max_tokens: 4096                                        |
|   timeout_ms: 30000                                       |
+----------------------------------------------------------+
                            |
Level 2: Task Prompt (per-request instruction)
+----------------------------------------------------------+
| --- Task Instruction ---                                  |
| Search for the latest AI research papers on               |
| multi-agent systems.                                      |
+----------------------------------------------------------+
                            |
Level 3: User Input (conversation turns)
+----------------------------------------------------------+
| User: Can you find papers about multi-agent...            |
| Assistant: Here are the latest papers...                  |
| User: Can you summarize the key findings?                 |
| ...                                                       |
+----------------------------------------------------------+
```

### 2.2 Prompt 注入过程 (Prompt Injection)

The `PromptInjector` assembles these layers into a single system prompt:

```python
def build_system_prompt(skill: Skill, task_instruction: str = "") -> str:
    layers = [
        engine_prompt,                    # Level 0: Engine
        "# Skill Context",                # Level 1: Skill begins
        f"--- Active Skill: {skill.name} v{skill.version} ---",
        skill.description,
        skill.prompt,                     # Behavioral instructions
        skill.tool_list_text,             # Tool definitions
        skill.constraint_text,            # Guardrails
    ]
    if task_instruction:
        layers.append(f"--- Task Instruction ---\n{task_instruction}")
    return "\n\n".join(layers)
```

**实际运行输出 (Actual Console Output):**

```
  Phase 3: Prompt Injection
========================================================================

--- Active Skill: web_researcher v1.0.0 ---

Research any topic by searching the web, fetching pages, and
extracting structured information from online sources.

You are a Web Research specialist.
- Search the web using the search tool for current information.
- Fetch full page content when you need detailed context.
- Extract structured data (tables, lists, key facts) from pages.
- Cite your sources with URLs in every response.

Available tools:
  - web_search: Search the web for a query. Returns top results with snippets.
  - web_fetch: Fetch the full content of a URL. Returns markdown.

Constraints:
  max_tokens: 4096
  timeout_ms: 30000
  allowed_domains: ['*']

--- Task Instruction ---
Search for the latest AI research papers on multi-agent systems.

Prompt length: 951 chars
Estimated tokens: 237
```

### 2.3 层级优先级规则 (Priority Rules)

| Level | Name | Scope | Override |
|-------|------|-------|----------|
| 0 | Engine Prompt | Global, all sessions | Never overridden |
| 1 | Skill Prompt | Per-skill, loaded at init | Overrides Engine for domain behavior |
| 2 | Task Instruction | Per-request | Overrides Skill for specific goals |
| 3 | User Input | Per-turn | Overrides Task via conversation |

Key principle: **lower levels override higher levels for specific behavior, but can never remove capabilities granted by higher levels.** A task can tell a skill to focus on a subtopic, but it cannot grant network access if the skill does not have that permission.

---

## 3. 上下文窗口优化 (Context Window Optimization)

### 3.1 Token 预算管理 (Token Budgeting)

Context windows are finite. We must decide what to keep when the window fills.

**预算分配策略 (Budget Allocation Strategy):**

```
                    small (4K)         medium (8K)         large (32K)
                +--------------+    +--------------+    +--------------+
                | system   20% |    | system   20% |    | system   20% |
                | skill    15% |    | skill    15% |    | skill    15% |
                | history  35% |    | history  35% |    | history  35% |
                | tools    20% |    | tools    20% |    | tools    20% |
                | reserve  10% |    | reserve  10% |    | reserve  10% |
                +--------------+    +--------------+    +--------------+
```

**实际运行输出 (Actual Console Output):**

```
  Phase 7: Token Budget Planning
========================================================================

Context window: small  (  4096 tokens)
  system_prompt         :   819 tokens ████████
  skill_context         :   614 tokens ██████
  conversation_history  :  1433 tokens ██████████████
  tool_results          :   819 tokens ████████
  reserved              :   409 tokens ████
  headroom              :     2 tokens

Context window: medium (  8192 tokens)
  system_prompt         :  1638 tokens ████████████████
  skill_context         :  1228 tokens ████████████
  conversation_history  :  2867 tokens ████████████████████████████
  tool_results          :  1638 tokens ████████████████
  reserved              :   819 tokens ████████
  headroom              :     2 tokens

Context window: large  ( 32768 tokens)
  system_prompt         :  6553 tokens ███████████████████████████████████
  skill_context         :  4915 tokens █████████████████████████████████
  conversation_history  : 11468 tokens █████████████████████████████████
  tool_results          :  6553 tokens █████████████████████████████████
  reserved              :  3276 tokens ██████████████████
  headroom              :     3 tokens
```

### 3.2 窗口管理策略 (Window Management Strategies)

三种核心策略，各有适用场景：

#### 策略一：滑动窗口 (Sliding Window)

Keep the last N tokens, discard the rest.

```
Input:  [A][B][C][D][E][F][G][H]          (8 turns)
Window:              [D][E][F][G][H]       (keep last 5)
```

**适用场景:** 对话式交互，最近的内容最重要。

#### 策略二：摘要压缩 (Summary Compression)

Summarize older messages into a compressed representation.

```
Input:  [A][B][C][D][E][F][G][H]
                    |
                    v
        [Summary of A-E][F][G][H]          (replace old with summary)
```

**适用场景:** 长文档处理、代码审查，需要保留全局上下文。

#### 策略三：检索增强 (Retrieval-Based)

Only include relevant history based on similarity to current query.

```
Input:  [A][B][C][D][E][F][G][H]  +  Query: "deploy the app"
                    |
                    v
        [C](deploy related) [G](deploy related) + [H](current)
```

**适用场景:** 知识库问答、多轮复杂推理。

### 3.3 Cache-Aware Prompt Ordering

LLM 的 KV cache 通常对 prompt 开头部分缓存效果最好。关键策略：

```
Ordering Principle: Static before dynamic, system before user.

1. Engine prompt          (static, cached once)
2. Skill definitions      (semi-static, cached per-skill)
3. Conversation history   (dynamic, partially cached)
4. Latest user input      (dynamic, not cached)
```

**优化后的预算示例 (Optimized Budget for code_writer):**

```
  Phase 7b: Optimized Budget for code_writer
========================================================================
Context window : large  ( 32768 total)
(Adjusted for code_writer: 4 tools + execution permissions)
  system_prompt         :  6553 tokens
  skill_context         :  4915 tokens
  conversation_history  :  9830 tokens     (reduced by 5%)
  tool_results          :  8191 tokens     (increased by 5%)
  reserved              :  3276 tokens
  headroom              :     3 tokens
```

Skills with execution permissions get more `tool_results` budget because command output tends to be large. Skills with fewer tools get more `conversation_history` budget.

---

## 4. 多 Agent 协作 (Multi-Agent Workflows)

### 4.1 三种协作模式 (Three Collaboration Patterns)

#### 模式一：顺序链 (Sequential Chain)

One skill's output becomes the next skill's context.

```
Research Task
    |
    v
[web_researcher] -- finds latest async patterns
    |
    v
[code_writer]    -- writes code example based on research
    |
    v
Output: well-researched, well-written code
```

**实际运行输出 (Actual Console Output):**

```
  Phase 4: Skill Chaining (Sequential)
========================================================================
Step 1: web_researcher
  Prompt tokens : 240
  Prompt preview: You are an AI assistant with dynamic skill injection...

Step 2: code_writer
  Prompt tokens : 258
  Prompt preview: You are an AI assistant with dynamic skill injection...
```

**适用场景:** Research -> Write -> Test 流水线。每个步骤依赖前一个步骤的输出。

#### 模式二：监督者模式 (Supervisor Pattern)

An orchestrator skill delegates sub-tasks to specialist skills.

```
                         [system_admin] (orchestrator)
                         /                \
                        v                  v
              [code_writer]           [system_admin]
              (build the app)         (deploy & monitor)
                        \                  /
                         v                v
                     Result: deployed application
```

**实际运行输出 (Actual Console Output):**

```
  Phase 5: Skill Chaining (Supervisor Pattern)
========================================================================
Orchestrator    : system_admin
Prompt tokens   : 255
Delegated to    :
  - code_writer: You are a Code Writing specialist...
  - system_admin: You are a System Administration specialist...
```

**适用场景:** 复杂任务需要多个专业角色协作。Orchestrator 负责分解任务、分配、整合结果。

#### 模式三：集成投票 (Ensemble Pattern)

Multiple skills answer the same question independently, then vote.

```
Task: "Best approach to deploy a Python web app?"
    |
    +--------+--------+--------+
    |        |        |        |
    v        v        v        v
[researcher] [writer] [admin] [more...]
    |        |        |        |
    +--------+--------+--------+
    |
    v
Majority vote on best approach
```

**实际运行输出 (Actual Console Output):**

```
  Phase 6: Skill Chaining (Ensemble Pattern)
========================================================================
Task            : What is the best approach to deploy a Python web app?
Ensemble size   : 3
Verdict strategy: Majority vote on best approach
  [web_researcher  ] tokens=  235  |  Research any topic by searching...
  [code_writer     ] tokens=  246  |  Write, review, and refactor code...
  [system_admin    ] tokens=  228  |  Manage system configurations...
```

**适用场景:** 需要多样化视角的决策任务。每个技能从自己的专业角度给出答案。

### 4.2 模式对比 (Pattern Comparison)

| 模式 | 延迟 | 质量 | 成本 | 最适合 |
|------|------|------|------|--------|
| **Sequential** | 低 (串行) | 中 (单一视角) | 低 | Research -> Code 流水线 |
| **Supervisor** | 中 (2级调度) | 高 (专业分工) | 中 | 复杂多步骤任务 |
| **Ensemble** | 高 (并行+投票) | 最高 (多视角) | 高 | 关键决策、高风险判断 |

### 4.3 Orchestration Cost vs Quality Tradeoff

```
Quality
  ^
  |                          Ensemble (3 agents, highest quality)
  |                        *
  |                   Supervisor (2 agents, good balance)
  |                 *
  |            Sequential (2 agents, fast)
  |          *
  |     Single Skill (baseline)
  |   *
  +------------------------------------------> Cost (tokens + latency)

Key insight: Ensemble gives the best quality but at 3x cost.
             Supervisor is the sweet spot for most tasks.
```

---

## 5. 运行示例 (Running Example)

### 5.1 快速开始 (Quick Start)

```bash
cd ai/10-toolchain-integration
./code/custom_skill.py
```

### 5.2 完整执行流程 (Full Execution Flow)

```
Execution Flow Diagram:

main()
  |
  +-- Phase 1: Load Skills
  |     SkillLoader.load_from_dict()
  |       -> Parse 3 YAML definitions
  |       -> Create Skill objects
  |       -> Output: 3 skills loaded
  |
  +-- Phase 2: Show YAML
  |     Print web_researcher definition
  |
  +-- Phase 3: Prompt Injection
  |     PromptInjector.build_system_prompt()
  |       -> Assemble 4-level hierarchy
  |       -> Inject skill context
  |       -> Output: 951 chars, ~237 tokens
  |
  +-- Phase 4: Sequential Chain
  |     SkillChainer.chain_sequential()
  |       -> web_researcher -> code_writer
  |       -> Pass context between steps
  |
  +-- Phase 5: Supervisor Pattern
  |     SkillChainer.chain_supervisor()
  |       -> orchestrator: system_admin
  |       -> delegates to code_writer, system_admin
  |
  +-- Phase 6: Ensemble Pattern
  |     SkillChainer.chain_ensemble()
  |       -> 3 skills vote on best approach
  |       -> Majority vote strategy
  |
  +-- Phase 7: Token Budget Planning
  |     TokenBudget.plan()
  |       -> 4 window sizes (4K to 128K)
  |       -> 5 budget categories
  |     TokenBudget.optimize_for_skill()
  |       -> Adjust for code_writer's needs
  |
  +-- Phase 8: Hierarchy Visualization
        Print 4-level prompt model
```

### 5.3 代码结构 (Code Structure)

```
code/custom_skill.py (~230 lines)
  |
  +-- SKILL_YAML_DEFS         (embedded YAML strings for 3 skills)
  |
  +-- ToolDef                 (data class: name, description, permissions)
  +-- Skill                   (data class: prompt, tools, constraints)
  |
  +-- SkillLoader             (parses YAML into Skill objects)
  +-- PromptInjector          (builds system prompt from skill)
  +-- SkillChainer            (composes skills: sequential/supervisor/ensemble)
  +-- TokenBudget             (context window budgeting)
  |
  +-- main()                  (runs all 8 phases with console output)
```

### 5.4 关键设计要点 (Key Design Points)

1. **Skill 定义是声明式的** -- 用 YAML 描述行为，不写代码。这使得非开发者也能创建和修改技能。
2. **Prompt 注入是无侵入的** -- Engine prompt 从不修改，skill prompt 叠加在上面。切换技能 = 切换 prompt 层。
3. **Token 预算是动态的** -- 根据技能的工具数量和权限类型自动调整。执行型技能获得更大的 `tool_results` 预算。
4. **链式调用是可组合的** -- 顺序链、监督者、集成投票三种模式可以嵌套组合，形成任意复杂的工作流。

---

## 总结 (Summary)

| 概念 | 核心要点 |
|------|---------|
| **Skill Design** | YAML 定义 + 专用 Prompt + 工具权限 + 执行约束 |
| **Prompt Hierarchy** | Engine -> Skill -> Task -> User, 低层覆盖高层 |
| **Context Budget** | 20% system + 15% skill + 35% history + 20% tools + 10% reserve |
| **Multi-Agent** | Sequential (流水线), Supervisor (调度), Ensemble (投票) |
| **Cost/Quality** | Ensemble 质量最高但成本 3x, Supervisor 是性价比最优解 |

> **Next:** This concludes the Toolchain Integration series. You should now understand MCP protocol, agent harness internals, tool systems, and skill/prompt architecture — the four pillars of modern AI toolchain integration.
>
> **下一章预告:** 工具链集成系列到此结束。你现在应该理解 MCP 协议、Agent Harness 内部机制、工具系统以及技能/提示词架构——现代 AI 工具链集成的四大支柱。
