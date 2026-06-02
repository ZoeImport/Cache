# 9.4 Agent 系统 — LLM + Tools + Loop
# 9.4 Agent Systems — LLM + Tools + Loop

> **Agent = LLM + Tools + Loop. An agent is not just a model — it is a model that perceives, thinks, acts, and learns from results.**
>
> **Agent = LLM + Tools + Loop。Agent 不只是一個模型，而是一個能感知、思考、行動並從結果中學習的系統。**

---

**前置知识 (Prerequisites):** 第 9.3 节 Tool Calling, 基础 Python
**依赖库 (Dependencies):** `transformers`, `requests`, `json` (stdlib)
**配套代码 (Code):** `code/agent_framework.py`

---

## 目录 (Table of Contents)

1. [Agent 核心公式 (The Agent Formula)](#1-agent-核心公式-the-agent-formula)
2. [ReAct 循环 ⭐ (The ReAct Loop)](#2-react-循环-the-react-loop)
3. [记忆管理 (Memory Management)](#3-记忆管理-memory-management)
4. [任务规划 (Task Planning)](#4-任务规划-task-planning)
5. [框架对比 (Framework Comparison)](#5-框架对比-framework-comparison)

---

## 1. Agent 核心公式 (The Agent Formula)

Agent 系统的核心可以用一个简单公式表达：

$$
\text{Agent} = \text{LLM} + \text{Tools} + \text{Loop}
$$

**The Core Loop:**

```
┌─────────────────────────────────────────────────┐
│                   The Agent Loop                 │
│                                                   │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│   │ Observe  │───▶│  Think   │───▶│  Decide  │  │
│   └──────────┘    └──────────┘    └──────────┘  │
│        ▲                                          │
│        │         ┌──────────┐    ┌──────────┐    │
│        └─────────│ Observe  │◀───│ Execute  │    │
│                  │  Result  │    │  Action  │    │
│                  └──────────┘    └──────────┘    │
└─────────────────────────────────────────────────┘
```

每一步分解 (Step-by-step):

| 步骤 (Step) | 描述 (Description) | 示例 (Example) |
|---|---|---|
| **Observe** | 接收用户输入或环境反馈 | User: "What's the weather in Tokyo?" |
| **Think** | LLM 分析当前状态，决定下一步 | "I need to call get_weather(location='Tokyo')" |
| **Decide** | 选择工具或直接回答 | Chosen: `get_weather` |
| **Execute** | 运行工具函数，获得结果 | Result: `{"temp": 25, "condition": "sunny"}` |
| **Observe Result** | 将工具结果送回 LLM | "The function returned 25°C and sunny" |
| **Think Again** | LLM 综合信息生成最终回答 | "The temperature in Tokyo is 25°C and sunny." |

> **关键洞察 (Key Insight):** 没有 Loop 的 LLM 只是一次性问答器。Loop 赋予了模型**迭代改进**和**工具使用**的能力。

### 为什么 Agent > 单纯 LLM？

| 能力 (Capability) | 单纯 LLM | Agent (LLM + Tools + Loop) |
|---|---|---|
| 实时数据 (Real-time data) | ❌ 知识截止于训练数据 | ✅ 可查询 API/DB |
| 精确计算 (Precise computation) | ❌ 近似推理 | ✅ 调用计算器 |
| 多步推理 (Multi-step reasoning) | ⚠️ 容易出错 | ✅ 分步验证 |
| 外部操作 (External actions) | ❌ 只能输出文本 | ✅ 发送邮件/创建订单 |
| 自我纠错 (Self-correction) | ❌ 无法 | ✅ 观察结果后调整 |

> 将 Agent 理解为"给 LLM 装上了手和眼睛"——手去执行操作，眼睛去观察结果。

---

## 2. ReAct 循环 ⭐ (The ReAct Loop)

**ReAct = Reason + Act.** 由 Yao et al. (2022) 提出，是目前最主流的 Agent 循环范式。

### 2.1 基本模式 (Basic Pattern)

```
Thought:  分析当前状态和可用信息，决定下一步
Action:   选择一个工具并传入参数
Observation: 工具执行结果的反馈
    ↑________________________|
           (循环直到可以回答)
```

**完整示例 (Full Example):**

```
User: "What is the current temperature in Tokyo?"

--- Round 1 ---
Thought: I need to find the current temperature in Tokyo.
         I have a weather_search tool that can help.
Action: weather_search({"location": "Tokyo"})
Observation: {"temperature": 25, "unit": "celsius", "condition": "sunny"}

--- Round 2 ---
Thought: I now have the temperature information for Tokyo.
         The temperature is 25°C and it's sunny. I can answer the user.
Final Answer: The current temperature in Tokyo is 25°C and it's sunny.
```

### 2.2 ReAct 状态机 (State Machine)

ReAct 循环可以用一个有限状态机来描述：

```
                    ┌──────────────────────────────────────┐
                    │                                      │
                    ▼                                      │
 ┌─────────┐   ┌──────────┐   ┌────────┐   ┌─────────────┐ │
 │  START  │──▶│  THINK   │──▶│ DECIDE │──▶│  EXECUTE    │─┘
 └─────────┘   └──────────┘   └────────┘   └─────────────┘
                    │                            │
                    │ ┌──────────────────────────┘
                    │ │
                    ▼ ▼
               ┌──────────┐
               │  ANSWER  │
               └──────────┘
```

状态转移表 (State Transition Table):

| 当前状态 (Current) | 条件 (Condition) | 下一状态 (Next) | 说明 (Description) |
|---|---|---|---|
| `START` | — | `THINK` | 收到用户输入后启动 |
| `THINK` | 需要更多信息 | `DECIDE` | 模型判断需要调用工具 |
| `THINK` | 已有足够信息 | `ANSWER` | 模型准备好给出最终回答 |
| `DECIDE` | — | `EXECUTE` | 选择具体工具和参数 |
| `EXECUTE` | 工具返回结果 | `THINK` | 观察结果后继续推理 |
| `EXECUTE` | 工具出错 | `THINK` | 错误信息也作为观察输入 |
| `ANSWER` | — | `START` | 输出最终回答，等待下一轮输入 |

### 2.3 伪代码 (Pseudocode)

```
function react_loop(user_input, tools, max_steps=10):
    messages = [user_input]
    
    for step in 1 to max_steps:
        # Step 1: Think — LLM 分析当前状态
        thought = llm.generate(
            prompt="Analyze the current situation. " +
                   "What do you know? What do you need?",
            context=messages
        )
        print(f"Thought: {thought}")
        
        # Step 2: Decide — LLM 选择 Action 或直接回答
        decision = llm.generate(
            prompt="Based on your analysis, choose one:\n" +
                   "1) Call a tool (format: TOOL: name, args)\n" +
                   "2) Give final answer (format: ANSWER: ...)",
            context=messages + [thought]
        )
        
        if decision starts with "ANSWER:":
            # 直接回答
            return decision.remove_prefix("ANSWER:")
        
        elif decision starts with "TOOL:":
            # Step 3: Execute — 调用工具
            tool_name, tool_args = parse(decision)
            result = execute_tool(tool_name, tool_args)
            
            # Step 4: Observe — 将结果添加到上下文
            observation = f"Tool {tool_name} returned: {result}"
            print(f"Observation: {observation}")
            messages.append(observation)
            # 回到 Step 1 (循环)
        
        else:
            # 解析失败，重试
            messages.append("ERROR: Invalid format. Use TOOL: or ANSWER:")
    
    # 超过最大步数
    return "Maximum steps reached. Here's what I have so far: ..."
```

### 2.4 关键设计决策 (Key Design Decisions)

| 决策 (Decision) | 选项 (Options) | 推荐 (Recommendation) |
|---|---|---|
| 何时停止循环 | 固定步数 vs. 模型自主决定 | 最大步数上限 + 模型自主决定 |
| Action 格式 | JSON vs. 自然语言 | JSON（结构化解析） |
| 错误处理 | 重试 vs. 跳过 | 重试 1-2 次后跳过 |
| 上下文管理 | 全部保留 vs. 裁剪 | 窗口 + 摘要混合 |

> **设计哲学 (Design Philosophy):** ReAct 的精髓在于**透明的推理过程**。每一步的 Thought 都应该清晰地展示模型的推理链，这不仅有助于调试，也增加了系统的可解释性。

---

## 3. 记忆管理 (Memory Management)

Agent 需要记忆来维护对话上下文、积累知识和保持行为一致性。记忆分为三个层次：

### 3.1 记忆层次 (Memory Hierarchy)

```
                  短期记忆 (Short-term)
               ┌─────────────────────┐
               │    Conversation     │
               │      History        │
               │   (in context)      │
               └──────────┬──────────┘
                          │ 超出窗口时
                          ▼
               ┌─────────────────────┐
               │  长期记忆 (Long-term) │
               │   Summaries /        │
               │   Vector Store       │
               └──────────┬──────────┘
                          │ 跨会话
                          ▼
               ┌─────────────────────┐
               │ 持久记忆 (Persistent) │
               │   Agent State /      │
               │   User Profile       │
               └─────────────────────┘
```

### 3.2 短期记忆 (Short-term Memory)

**形式:** 完整的对话历史，作为 LLM 上下文窗口的一部分。

**特点:**
- 容量受限于上下文窗口（如 8K, 32K, 128K tokens）
- 精确保留所有信息
- 随着对话增长，最早的信息被丢弃（滑动窗口）

```
# Sliding Window 短期记忆
SHORT_TERM_WINDOW = 4000  # tokens

def manage_short_term(messages):
    total_tokens = count_tokens(messages)
    if total_tokens > SHORT_TERM_WINDOW:
        # 丢弃最早的消息对（保留 system prompt）
        while count_tokens(messages) > SHORT_TERM_WINDOW:
            messages.pop(1)  # 跳过 system prompt
    return messages
```

**优缺点:**

| 优点 (Pros) | 缺点 (Cons) |
|---|---|
| 完全精确，无信息损失 | 受窗口大小限制 |
| 实现简单 | 早期信息完全丢失 |
| 无需额外存储 | 长对话效率低 |

### 3.3 长期记忆 (Long-term Memory)

**形式:** 对话摘要或向量数据库中的嵌入。

**两种主要方法:**

#### 方法一：摘要记忆 (Summary Memory)

定期总结旧对话，用摘要代替原始内容。

```
def summarize_memory(messages):
    # 对早期消息生成摘要
    summary_prompt = "Summarize the key information from this conversation."
    summary = llm.generate(summary_prompt, context=messages[:N])
    
    # 替换原始消息为摘要
    return [summary] + messages[N:]
```

#### 方法二：向量记忆 (Vector Memory)

将信息嵌入到向量空间中，按需检索：

```
def retrieve_relevant(query, vector_store, top_k=5):
    query_embedding = embed(query)
    results = vector_store.similarity_search(query_embedding, k=top_k)
    return results

# 存储记忆
def store_memory(info, vector_store):
    embedding = embed(info)
    vector_store.add(embedding, metadata={"text": info})
```

**检索增强生成的记忆流程:**

```
User Query
    │
    ▼
Retrieve relevant memories ───┐
    │                         │
    ▼                         ▼
LLM + Context = Generated Response
```

### 3.4 持久记忆 (Persistent Memory)

**形式:** 保存到磁盘/数据库的 Agent 状态，跨会话持久化。

```
import json

class PersistentMemory:
    def __init__(self, path="agent_state.json"):
        self.path = path
        self.state = self._load()
    
    def _load(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"user_profile": {}, "task_history": []}
    
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def update_profile(self, key, value):
        self.state["user_profile"][key] = value
        self.save()
```

### 3.5 三种记忆对比 (Comparison)

| 维度 (Dimension) | 短期 (Short-term) | 长期 (Long-term) | 持久 (Persistent) |
|---|---|---|---|
| 存储位置 | LLM 上下文 | RAM / Vector DB | 磁盘 / 数据库 |
| 持久性 | 当前会话 | 可能持久化 | 跨会话持久 |
| 容量 | 有限 (tokens) | 大 | 极大 |
| 检索方式 | 顺序读取 | 语义检索 | 键值查询 |
| 时延 | 低 | 中 (检索耗时) | 低 |
| 精度 | 100% | 有损 (摘要/嵌入) | 100% |

---

## 4. 任务规划 (Task Planning)

### 4.1 Plan-and-Execute

对于复杂任务，Agent 需要先将任务分解为子步骤，再逐步执行。

```
                    ┌─────────────────┐
                    │  Complex Task   │
                    │  "Research AI   │
                    │   news today"   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Step 1: Plan   │
                    │  "1. Search for │
                    │  latest AI news │
                    │  2. Summarize   │
                    │  3. Format"     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │ Execute 1  │ │ Execute 2  │ │ Execute 3  │
     │ Search     │▶│ Summarize  │▶│ Format     │
     └────────────┘ └────────────┘ └────────────┘
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐ ┌────────────┐ ┌────────────┐
     │ Result 1   │ │ Result 2   │ │ Final      │
     │ raw news   │ │ summary    │ │ output     │
     └────────────┘ └────────────┘ └────────────┘
```

**Plan-and-Execute 伪代码:**

```
function plan_and_execute(task, tools):
    # Phase 1: Plan
    plan = llm.generate(
        f"Given the task: '{task}'\n" +
        "Create a step-by-step plan. Each step should specify which tool to use."
    )
    steps = parse_steps(plan)
    
    # Phase 2: Execute
    results = []
    for step in steps:
        print(f"Executing: {step}")
        result = execute_step(step, tools)
        results.append(result)
    
    # Phase 3: Synthesize
    final = llm.generate(
        f"Task: {task}\n" +
        f"Results: {results}\n" +
        "Synthesize a final answer."
    )
    return final
```

### 4.2 RePlan (动态重规划)

当某个子步骤失败或发现新信息时，Agent 需要动态调整计划。

```
function execute_with_replan(task, tools):
    plan = llm.generate(f"Plan for: {task}")
    
    for step in plan:
        result = execute_step(step, tools)
        
        if result indicates failure or new information:
            # RePlan: 基于当前状态重新规划
            plan = llm.generate(
                f"Original task: {task}\n" +
                f"Completed so far: {step_results}\n" +
                f"Latest result: {result}\n" +
                "Adjust the remaining plan."
            )
            # 继续执行调整后的计划
    
    return synthesize(task, step_results)
```

**何时需要 RePlan:**

| 场景 (Scenario) | RePlan 策略 |
|---|---|
| 工具返回空结果 | 换个搜索词或工具 |
| API 调用失败 | 尝试备用 API 或延迟重试 |
| 发现更优路径 | 更新计划采用新方案 |
| 信息不足以回答 | 增加更多信息收集步骤 |
| 用户中途改变需求 | 重新制定完整计划 |

### 4.3 任务规划策略对比

| 策略 (Strategy) | 适用场景 | 优点 | 缺点 |
|---|---|---|---|
| **顺序执行 (Sequential)** | 步骤依赖明确的任务 | 简单可靠 | 无法并行 |
| **Plan-and-Execute** | 复杂多步骤任务 | 结构化，可追踪 | 计划可能不准确 |
| **RePlan** | 不确定性高的任务 | 灵活适应变化 | 开销大 |
| **分层规划 (Hierarchical)** | 超复杂任务 | 可扩展 | 实现复杂 |

---

## 5. 框架对比 (Framework Comparison)

### 5.1 LangChain Agent

**定位:** 标准化工具使用的通用 Agent 框架。

```
Agent Executor
    │
    ├── LLM (推理引擎)
    ├── Tools (工具注册表)
    ├── Memory (记忆管理)
    └── Agent Type (策略选择: ReAct, Plan-Execute, ...)
```

**核心特点:**
- 丰富的内置工具和集成
- 多种 Agent 类型（ReAct, Structured Chat, Plan-Execute...）
- `AgentExecutor` 管理循环
- 支持自定义工具

```python
# LangChain Agent 示例 (概念)
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

tools = [
    Tool(name="search", func=search_function, description="Search the web"),
    Tool(name="calculator", func=calc_function, description="Do math"),
]

agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools)
result = agent_executor.invoke({"input": "What is 123 * 456?"})
```

### 5.2 LangGraph

**定位:** 基于图的 Agent 编排框架，支持循环、分支、并行。

```
          ┌─────────┐
          │  START  │
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │  NODE   │ ← 节点：LLM 调用、工具执行、条件判断
          └────┬────┘
               │
          ┌────▼────┐
          │  EDGE   │ ← 边：条件转移、循环、并行分支
          └────┬────┘
               │
               ▼
          ┌─────────┐
          │  END    │
          └─────────┘
```

**核心特点:**
- 将 Agent 逻辑建模为**有向图**
- 节点 (Node): LLM 调用、工具执行、人类审核
- 边 (Edge): 条件分支、循环、并行
- 比 LangChain Agent 更灵活

```python
# LangGraph 示例 (概念)
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)

graph.add_node("agent", call_llm)
graph.add_node("action", call_tool)

graph.add_conditional_edges(
    "agent",
    decide_next,  # 判断是继续还是结束
    {"continue": "action", "end": END}
)

graph.add_edge("action", "agent")
app = graph.compile()
```

### 5.3 AutoGen (Microsoft)

**定位:** 多 Agent 对话系统。

```
    User
     │
     ▼
┌──────────┐     ┌──────────┐
│  Agent A │◄───►│  Agent B │
│ (PM)     │     │ (Coder)  │
└──────────┘     └──────────┘
     ▲                │
     │                ▼
     │          ┌──────────┐
     └──────────┤  Agent C │
                │ (Review) │
                └──────────┘
```

**核心特点:**
- 多 Agent 通过**对话**协作
- 每个 Agent 有自己的角色和 LLM 配置
- Agent 之间可以互相发消息
- 支持人类参与（Human-in-the-loop）

```python
# AutoGen 示例 (概念)
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"},
)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
)

user_proxy.initiate_chat(
    assistant,
    message="Write a Python script to fetch stock data."
)
```

### 5.4 CrewAI

**定位:** 基于角色的多 Agent 协作框架。

```
┌─────────────────────────────────────────────────┐
│                    Crew                          │
│                                                   │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│   │  Researcher│    │  Writer  │    │  Editor  │  │
│   │ role=expert│    │ role=journalist          │  │
│   │ goal=find  │    │ goal=create article      │  │
│   │ backstory=PhD│   │ backstory=reporter       │  │
│   └──────────┘    └──────────┘    └──────────┘  │
│         │               │               │        │
│         └───────────────┼───────────────┘        │
│                         │                        │
│                   ┌─────▼─────┐                  │
│                   │   Task    │                  │
│                   │ Pipeline  │                  │
│                   └───────────┘                  │
└─────────────────────────────────────────────────┘
```

**核心特点:**
- 基于**角色**（Role）和**目标**（Goal）定义 Agent
- Agent 有 `backstory`（背景故事）和 `personality`
- 任务按流水线 (Pipeline) 组织
- 内置**委派** (Delegation) 机制

```python
# CrewAI 示例 (概念)
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Research Analyst",
    goal="Find latest AI breakthroughs",
    backstory="Expert in AI research",
)

writer = Agent(
    role="Tech Writer",
    goal="Write engaging summaries",
    backstory="Technology journalist",
)

task = Task(
    description="Summarize this week's AI news",
    agent=researcher,
)

crew = Crew(agents=[researcher, writer], tasks=[task])
result = crew.kickoff()
```

### 5.5 框架对比表 (Comparison Table)

| 维度 (Dimension) | LangChain Agent | LangGraph | AutoGen | CrewAI |
|---|---|---|---|---|
| **核心范式** | Agent + Tool | 有向图 | 多 Agent 对话 | 角色协作 |
| **循环支持** | ✅ 内置 | ✅ 原生 | ✅ 对话循环 | ✅ Pipeline |
| **多 Agent** | ❌ 单 Agent | ✅ 可组合 | ✅ 原生 | ✅ 原生 |
| **并行执行** | ❌ | ✅ 分支 | ⚠️ 间接 | ✅ 并行任务 |
| **人类参与** | ⚠️ 有限 | ✅ 节点控制 | ✅ 原生 | ⚠️ 有限 |
| **学习曲线** | 低 | 中-高 | 中 | 低 |
| **灵活性** | 中 | 高 | 中-高 | 中 |
| **Python 生态** | ✅ 丰富 | ✅ 基于 LC | ✅ 独立 | ✅ 独立 |
| **适用场景** | 快速原型 | 复杂流程 | 多角色讨论 | 内容创作 |
| **贡献者** | LangChain Inc. | LangChain Inc. | Microsoft | CrewAI Inc. |

### 5.6 选型建议 (Selection Guide)

```
你的任务是什么？
    │
    ├── 单个工具调用 → 直接用 Tool Calling (9.3节)
    │
    ├── 简单的多步任务 → LangChain Agent
    │
    ├── 复杂的工作流（分支/循环/并行） → LangGraph
    │
    ├── 多角色辩论/讨论 → AutoGen
    │
    └── 内容创作流水线 → CrewAI
```

> **建议 (Recommendation):** 从 LangChain Agent 开始，它足够应对大部分常见场景。当需要更复杂的控制流（条件分支、并行、循环嵌套）时，迁移到 LangGraph。如果需要多 Agent 协作，在 AutoGen 和 CrewAI 之间选择——看你是需要"自由对话"（AutoGen）还是"结构化分工"（CrewAI）。

---

## 总结 (Summary)

$$
\boxed{\text{Agent} = \text{LLM} + \text{Tools} + \text{Loop}}
$$

| 概念 (Concept) | 一句话总结 (One-line Summary) |
|---|---|
| **Agent 公式** | LLM 提供推理，Tools 提供能力，Loop 提供迭代 |
| **ReAct 循环** | 观察 → 思考 → 行动 → 观察结果 → 循环 |
| **短期记忆** | 对话历史，精确但有窗口限制 |
| **长期记忆** | 摘要或向量存储，容量大但有损 |
| **持久记忆** | 跨会话保存的状态和用户画像 |
| **Plan-and-Execute** | 先规划再执行，适合复杂任务 |
| **RePlan** | 失败时动态调整计划 |
| **LangChain Agent** | 标准化工具使用的通用框架 |
| **LangGraph** | 基于图的灵活编排 |
| **AutoGen** | 多 Agent 对话协作 |
| **CrewAI** | 基于角色的分工协作 |
