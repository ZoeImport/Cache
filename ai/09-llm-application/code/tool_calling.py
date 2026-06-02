#!/usr/bin/env python3
"""
Tool Calling（函数调用）完整演示

模拟 LLM 的 Tool Calling 流程，展示：
1. 工具定义（Tool Definition）
2. 单次工具调用
3. 多步串联调用
4. 并行工具调用
5. 错误处理

依赖：无（纯 Python 标准库）
运行：python tool_calling.py

Author: love-story AI
"""

import json
import re
import time
import datetime
from typing import Any, Callable

# ============================================================
# Step 1: 工具定义（Tool Definitions）
# ============================================================

# 工具 Schema —— 模拟 OpenAI 格式的工具定义
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式。当用户需要数值计算时使用，支持 + - * / ** // %% 和数学函数如 sqrt, abs。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，例如 '2+3*4' 或 'sqrt(16) + 5'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索互联网信息。当用户询问新闻、知识、事实性信息时使用。返回简要的模拟搜索结果。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，例如 '今天天气' 或 'AI 最新进展'",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "获取指定时区的当前时间。当用户询问时间、日期时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "时区名称，例如 'Asia/Shanghai'、'America/New_York'、'Europe/London'",
                    }
                },
                "required": ["timezone"],
            },
        },
    },
]


# ============================================================
# Step 2: 工具实现（Tool Implementations）
# ============================================================

def tool_calculator(expression: str) -> str:
    """执行数学计算。"""
    print(f"  🔧 [calculator] 计算表达式: {expression!r}")
    # 安全求值：只允许数字、运算符和 math 函数
    allowed_names = {
        k: v for k, v in __import__("math").__dict__.items()
        if not k.startswith("_")
    }
    allowed_names.update({"abs": abs, "round": round})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        print(f"  ✅ [calculator] 结果: {result}")
        return str(result)
    except ZeroDivisionError:
        return "Error: 除数不能为 0（Division by zero）"
    except Exception as e:
        return f"Error: 表达式无效 — {e}"


def tool_search(query: str) -> str:
    """模拟搜索引擎。"""
    print(f"  🔧 [search] 搜索关键词: {query!r}")
    mock_results = {
        "天气": "今天北京 25°C，晴转多云 ☀️",
        "python": "Python 是一种广泛使用的高级编程语言，最新版本为 3.14",
        "ai": "人工智能（AI）是计算机科学的重要分支，涵盖 ML、DL、NLP 等领域",
        "news": "今日新闻：AI 模型在医疗诊断领域取得重大突破",
    }
    for keyword, result in mock_results.items():
        if keyword in query.lower():
            print(f"  ✅ [search] 结果: {result}")
            return result
    fallback = f"关于 '{query}' 的搜索结果：未找到精确匹配，建议缩小搜索范围。"
    print(f"  ⚠️  [search] 结果: {fallback}")
    return fallback


def tool_get_time(timezone: str) -> str:
    """获取指定时区的时间。"""
    print(f"  🔧 [get_time] 查询时区: {timezone!r}")
    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo(timezone)
        now = datetime.datetime.now(tz)
        result = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        print(f"  ✅ [get_time] 结果: {result}")
        return result
    except KeyError:
        return f"Error: 未知时区 '{timezone}'，请使用 IANA 时区名，如 'Asia/Shanghai'"
    except Exception as e:
        return f"Error: 获取时间失败 — {e}"


TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    "calculator": tool_calculator,
    "search": tool_search,
    "get_time": tool_get_time,
}


# ============================================================
# Step 3: 模拟 LLM（Mock LLM）
# ============================================================

def simulate_llm_decision(user_input: str) -> list[dict] | None:
    """
    模拟 LLM 根据用户输入决定是否调用工具。
    """
    text_lower = user_input.lower()

    # ---- 并行调用场景 ----
    if "对比" in user_input or "比较" in user_input:
        locations = re.findall(r'[A-Za-z\u4e00-\u9fff]+', user_input.split("对比" if "对比" in user_input else "比较")[-1])
        locations = [loc for loc in locations if loc not in ("天气", "和", "与", "温度")]
        if len(locations) >= 2:
            return [
                {"name": "get_weather_placeholder", "arguments": json.dumps({"location": loc})}
                for loc in locations[:3]
            ]

    # ---- 计算器 ----
    calc_patterns = [
        r"计算\s*([\d\+\-\*/\s\(\)\.]+)\s*等于多少",
        r"计算\s*([\d\+\-\*/\s\(\)\.]+)",
        r"([\d\+\-\*/\s\(\)\.]+)\s*等于多少",
        r"(\d[\d\+\-\*/\s\(\)]+\d)",
        r"what's\s+(.+?)$",
        r"(\d+\s*[\+\-\*/]\s*\d+)",
    ]
    for pattern in calc_patterns:
        m = re.search(pattern, user_input)
        if m:
            expr = m.group(1).strip()
            return [{"name": "calculator", "arguments": json.dumps({"expression": expr})}]

    # ---- 时间查询 ----
    timezone_map = {
        "上海": "Asia/Shanghai",
        "北京": "Asia/Shanghai",
        "东京": "Asia/Tokyo",
        "伦敦": "Europe/London",
        "纽约": "America/New_York",
        "巴黎": "Europe/Paris",
        "旧金山": "America/Los_Angeles",
    }
    if any(w in text_lower for w in ("时间", "几点", "时区", "time", "日期")):
        for cn_name, tz in timezone_map.items():
            if cn_name in user_input:
                return [{"name": "get_time", "arguments": json.dumps({"timezone": tz})}]
        return [{"name": "get_time", "arguments": json.dumps({"timezone": "Asia/Shanghai"})}]

    # ---- 搜索 ----
    if any(w in text_lower for w in ("搜索", "查找", "什么是", "查询", "搜索一下", "search", "find", "what is")):
        for prefix in ("搜索", "查找", "搜索一下", "查询", "什么是", "what is", "find"):
            if prefix in text_lower:
                query = user_input.split(prefix, 1)[-1].strip()
                if query:
                    return [{"name": "search", "arguments": json.dumps({"query": query})}]

    return None


def simulate_llm_response(user_input: str, tool_results: list[tuple[dict, str]] | None = None) -> str:
    """模拟 LLM 根据工具结果生成最终回复。"""
    if tool_results is None:
        greetings = ["你好", "hi", "hello", "嗨", "您好"]
        if any(g in user_input.lower() for g in greetings):
            return "你好！有什么我可以帮你的吗？我可以计算、搜索信息、查询时间。"
        return f"你说的是：'{user_input}'。需要我帮你计算、搜索或查询时间吗？"

    replies = []
    for call, result in tool_results:
        name = call["name"]
        if name == "calculator":
            replies.append(f"计算结果：{result}")
        elif name == "search":
            replies.append(result)
        elif name == "get_time":
            replies.append(result)

    return "。".join(replies) + "。"


# ============================================================
# Step 4: 核心 Tool Calling 循环
# ============================================================

def execute_tool_call(tool_call: dict) -> str:
    """执行单个工具调用。"""
    name = tool_call["name"]
    args_raw = tool_call["arguments"]

    try:
        args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
    except json.JSONDecodeError as e:
        return f"Error: 参数解析失败 — {e}"

    if name not in TOOL_REGISTRY:
        return f"Error: 未知工具 '{name}'，可用工具：{', '.join(TOOL_REGISTRY.keys())}"

    func = TOOL_REGISTRY[name]
    try:
        return func(**args)
    except TypeError as e:
        return f"Error: 工具 '{name}' 参数错误 — {e}"
    except Exception as e:
        return f"Error: 工具 '{name}' 执行异常 — {e}"


def run_tool_calling_flow(user_input: str):
    """运行完整的 Tool Calling 流程。"""
    print(f"\n{'='*60}")
    print(f"📝 用户输入: {user_input}")
    print(f"{'='*60}")

    print(f"\n🤖 LLM 正在分析意图...")
    time.sleep(0.3)
    decision = simulate_llm_decision(user_input)

    if decision is None:
        print(f"  ℹ️  未触发工具调用，直接回复")
        response = simulate_llm_response(user_input)
        print(f"\n💬 回复: {response}")
        return

    print(f"\n📋 触发 {len(decision)} 个工具调用:")
    tool_results = []

    for i, call in enumerate(decision):
        name = call["name"]
        args = call["arguments"]
        args_pretty = json.loads(args) if isinstance(args, str) else args
        print(f"\n  [{i+1}] 工具调用: {name}({json.dumps(args_pretty, ensure_ascii=False)})")

        result = execute_tool_call(call)
        tool_results.append((call, result))

        display = result[:80] + '...' if len(result) > 80 else result
        print(f"      ↳ 结果: {display}")

    print(f"\n🤖 LLM 整合工具结果...")
    time.sleep(0.2)
    response = simulate_llm_response(user_input, tool_results)
    print(f"\n💬 回复: {response}")


def run_parallel_calling_demo():
    """演示并行工具调用。"""
    print(f"\n\n{'='*60}")
    print(f"  🚀 并行工具调用演示")
    print(f"{'='*60}")

    print(f"""
并行调用（Parallel Tool Calling）是指 LLM 在一次响应中
输出多个工具调用，这些调用之间无依赖关系，可以同时执行。

示例:
  用户: "对比一下东京和伦敦的天气"
  LLM 输出: [
    {{"name": "get_weather", "arguments": {{"location": "Tokyo"}}}},
    {{"name": "get_weather", "arguments": {{"location": "London"}}}}
  ]
  应用并行执行两个调用，合并结果后返回给 LLM。
""")

    print(f"\n📝 用户输入: 计算 2+3*4 和 15/3 的结果")
    print(f"🤖 LLM 决策: 需要调用 calculator 工具两次（并行）")

    parallel_calls = [
        {"name": "calculator", "arguments": '{"expression": "2+3*4"}'},
        {"name": "calculator", "arguments": '{"expression": "15/3"}'},
    ]

    print(f"\n📋 并行执行 {len(parallel_calls)} 个工具调用:")
    results = []
    for i, call in enumerate(parallel_calls):
        name = call["name"]
        args = json.loads(call["arguments"])
        print(f"\n  [{i+1}] 并行调用: {name}({json.dumps(args)})")
        result = execute_tool_call(call)
        results.append((call, result))

    print(f"\n💬 最终回复: 2+3*4=14, 15/3=5。两个计算已完成。")

    print(f"\n{'='*60}")
    print(f"  ✅ 并行调用演示完成")
    print(f"{'='*60}")


def run_error_handling_demo():
    """演示错误处理。"""
    print(f"\n\n{'='*60}")
    print(f"  ⚠️  错误处理演示")
    print(f"{'='*60}")

    print(f"""
工具调用中可能出现的错误类型：
  • 参数值错误（如除零）
  • 表达式语法错误
  • 调用不存在的工具
  • 参数格式错误
""")

    error_cases = [
        ("除数不能为0", {"name": "calculator", "arguments": '{"expression": "1/0"}'}),
        ("无效表达式", {"name": "calculator", "arguments": '{"expression": "abc+def"}'}),
        ("未知工具", {"name": "send_email", "arguments": '{"to": "user@example.com"}'}),
        ("参数缺失(get_time 需要 timezone)", {"name": "get_time", "arguments": '{}'}),
    ]

    for desc, call in error_cases:
        print(f"\n  场景: {desc}")
        args_pretty = json.loads(call["arguments"])
        print(f"  调用: {call['name']}({json.dumps(args_pretty, ensure_ascii=False)})")
        result = execute_tool_call(call)
        print(f"  结果: ❌ {result}")

    print(f"\n{'='*60}")
    print(f"  ✅ 错误处理演示完成")
    print(f"{'='*60}")


# ============================================================
# Step 5: 主程序
# ============================================================

def main():
    print(f"""
╔══════════════════════════════════════════════════╗
║     Tool Calling（函数调用）完整演示              ║
║     LLM Tool Calling Complete Demo               ║
╚══════════════════════════════════════════════════╝

可用工具 (Available Tools):
  • calculator  - 数学计算 (如 2+3*4, sqrt(16))
  • search      - 信息搜索 (如 天气, AI, Python)
  • get_time    - 时间查询 (如 上海, 东京, 伦敦)
""")

    # 1. 单次工具调用（计算器）
    print(f"\n{'#'*60}")
    print(f"  # 场景 1: 单次工具调用（计算器）")
    print(f"  # Scenario 1: Single Tool Call (Calculator)")
    print(f"{'#'*60}")
    run_tool_calling_flow("计算 2+3*4 等于多少")

    # 2. 搜索工具调用
    print(f"\n{'#'*60}")
    print(f"  # 场景 2: 信息搜索")
    print(f"  # Scenario 2: Information Search")
    print(f"{'#'*60}")
    run_tool_calling_flow("搜索一下今天天气怎么样")

    # 3. 时间查询
    print(f"\n{'#'*60}")
    print(f"  # 场景 3: 时区时间查询")
    print(f"  # Scenario 3: Timezone Query")
    print(f"{'#'*60}")
    run_tool_calling_flow("东京现在几点")

    # 4. 多步串联
    print(f"\n{'#'*60}")
    print(f"  # 场景 4: 多步串联调用")
    print(f"  # Scenario 4: Sequential Multi-step Calls")
    print(f"{'#'*60}")
    run_tool_calling_flow("搜索什么是 Python")

    # 5. 并行调用演示
    run_parallel_calling_demo()

    # 6. 错误处理演示
    run_error_handling_demo()

    print(f"""
{'='*60}
  🎉 演示完成！完整流程回顾：

  1. 用户输入自然语言
  2. LLM 解析意图 → 输出结构化工具调用
  3. 应用执行工具 → 返回结果
  4. LLM 整合结果 → 生成自然语言回复

  Key Takeaway:
  - 工具定义中 description 至关重要
  - 参数使用 JSON Schema 描述
  - 支持单次、多步、并行调用
  - 错误信息要结构化，便于 LLM 重试
{'='*60}
""")


if __name__ == "__main__":
    main()
