"""
agent_framework.py — Mini Agent Framework from Scratch

Demonstrates:
1. Agent Formula: Agent = LLM + Tools + Loop
2. ReAct Loop: Thought -> Action -> Observation -> Thought -> ... -> Answer
3. Memory: short-term, long-term, persistent
4. Task Planning: Plan-and-Execute
5. Tool system: registration, dispatch, error handling

Task: "Research and summarize AI news"
Data is simulated (no API key needed).
Local LLM (GPT-2) provides lightweight reasoning completions.

Requires: transformers, torch
"""

import json
import time
import re
from typing import Callable


# =============================================================================
# 1. LLM Interface — lightweight text completion
# =============================================================================

class LocalLLM:
    """GPT-2 wrapper for short text completions within the agent loop."""

    def __init__(self, model_name: str = "gpt2"):
        print(f"[LLM] Loading {model_name} ...")
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.eval()
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def complete(self, prompt: str, max_new_tokens: int = 30) -> str:
        """Short text completion."""
        import torch
        inputs = self.tokenizer(prompt, return_tensors="pt",
                                truncation=True, max_length=256)
        with torch.no_grad():
            out = self.model.generate(
                inputs.input_ids,
                max_new_tokens=max_new_tokens,
                temperature=0.7, do_sample=True, top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        full = self.tokenizer.decode(out[0], skip_special_tokens=True)
        new = full[len(prompt):].strip().split("\n")[0]
        return new[:120]


# =============================================================================
# 2. Tool System
# =============================================================================

class Tool:
    """A named callable with a description."""

    def __init__(self, name: str, desc: str, fn: Callable):
        self.name = name
        self.desc = desc
        self.fn = fn

    def run(self, **kw) -> str:
        try:
            return str(self.fn(**kw))
        except Exception as e:
            return f"[ERROR] {e}"


class Toolbox:
    """Holds registered tools."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def add(self, t: Tool):
        self._tools[t.name] = t

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return list(self._tools.keys())

    def describe(self) -> list[str]:
        return [f"{t.name}: {t.desc}" for t in self._tools.values()]


# =============================================================================
# 3. Simulated knowledge & tools
# =============================================================================

NEWS_DB = {
    "latest": [
        ("GPT-5 achieves new benchmark records", "TechCrunch",
         "OpenAI's GPT-5 shows breakthrough performance on reasoning and coding."),
        ("Claude 4 introduces extended thinking mode", "The Verge",
         "Anthropic's Claude 4 can reason internally for minutes before responding."),
        ("Google releases Gemini 3 with native tool use", "Wired",
         "Gemini 3 directly calls APIs without tool-use fine-tuning."),
        ("Open-source LLMs surpass GPT-4 on key metrics", "Ars Technica",
         "Llama 4 and Mistral 3 now match or exceed GPT-4 on benchmarks."),
        ("AI agent frameworks see 300% adoption growth", "ZDNet",
         "LangChain, AutoGen, CrewAI report record enterprise adoption."),
    ],
    "ai_agents": [
        ("ReAct pattern becomes industry standard for agents", "AI Research",
         "The Reason+Act pattern is now the backbone of most agent frameworks."),
        ("Multi-agent systems beat single agents on complex tasks", "AI Research",
         "Teams of specialized agents outperform generalist agents."),
    ],
}

ARTICLE_DB = {
    "techcrunch": "GPT-5 achieves new benchmark records across reasoning, coding, and multimodal tasks. It shows 40% improvement on MATH and HumanEval benchmarks.",
    "theverge": "Claude 4 introduces extended thinking mode, reasoning internally for up to 2 minutes before responding. This improves complex mathematical reasoning.",
    "wired": "Gemini 3 features native function calling, directly invoking APIs without tool-use specific fine-tuning. Early tests show 60% latency reduction.",
}


def search_web(query: str) -> str:
    """Simulated search."""
    time.sleep(0.05)
    hits = []
    for cat, items in NEWS_DB.items():
        for title, src, _ in items:
            if query.lower() in title.lower() or query.lower() in cat:
                hits.append(f"  - {title} ({src})")
    if not hits:
        for title, src, _ in NEWS_DB["latest"][:3]:
            hits.append(f"  - {title} ({src})")
    return "\n".join(hits) if hits else "  (no results)"


def extract_article(url: str) -> str:
    """Simulated article extraction."""
    time.sleep(0.05)
    for key, text in ARTICLE_DB.items():
        if key in url:
            return text
    return "Article not found."


def summarize_text(text: str) -> str:
    """Simulated summarization."""
    time.sleep(0.05)
    parts = text.split(". ")
    return ". ".join(parts[:2]) + "." if len(parts) > 2 else text[:120]


# =============================================================================
# 4. Memory
# =============================================================================

class Memory:
    """Short-term conversation buffer with trimming."""

    def __init__(self, limit: int = 2000):
        self.entries: list[tuple[str, str]] = []
        self.limit = limit

    def add(self, role: str, text: str):
        self.entries.append((role, text))
        total = sum(len(e[1]) for e in self.entries)
        while total > self.limit and len(self.entries) > 1:
            self.entries.pop(1)
            total = sum(len(e[1]) for e in self.entries)

    def context(self) -> str:
        return "\n".join(f"[{r}] {t}" for r, t in self.entries)


class PersistentStore:
    """JSON file-based persistent storage."""

    def __init__(self, path: str = "/tmp/agent_state.json"):
        self.path = path
        try:
            with open(path) as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {"sessions": []}

    def save_session(self, task: str, steps: int):
        self.data["sessions"].append({
            "task": task, "steps": steps,
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)


# =============================================================================
# 5. ReAct Loop Engine
# =============================================================================

class ReActAgent:
    """
    ReAct loop: THINK -> DECIDE -> (ANSWER | EXECUTE -> OBSERVE -> THINK)
    """

    def __init__(self, llm: LocalLLM, tools: Toolbox, max_steps: int = 6):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.mem = Memory()
        self.history: list[dict] = []

    # -- printing helpers ------------------------------------------------

    @staticmethod
    def _rule(c="=", w=66):
        return c * w

    def _h1(self, text: str):
        print(f"\n{self._rule()}\n  {text}\n{self._rule()}")

    def _thought(self, text: str):
        print(f"  Thought   | {text}")

    def _action(self, name: str, args: dict):
        print(f"  Action    | {name}({json.dumps(args)})")

    def _obs(self, text: str):
        for line in text.strip().split("\n"):
            print(f"  Observe   | {line}")

    def _answer(self, text: str):
        print(f"\n  Answer    | {text}")

    # -- core loop -------------------------------------------------------

    def run(self, task: str) -> str:
        self.mem = Memory()
        self.mem.add("user", task)
        self.history = []

        self._h1(f"ReAct AGENT  |  task: {task}")

        for step in range(1, self.max_steps + 1):
            print(f"\n  ── round {step}/{self.max_steps} ─────────────────────")

            # ---- THINK ----
            ctx = self.mem.context()
            thought_raw = self.llm.complete(
                f"Task: {task}\nState: {ctx}\nWhat I should do next:"
            )
            thought = _clean(thought_raw) or f"Research step {step}"
            self._thought(thought)
            self.mem.add("agent", f"thought: {thought}")

            # ---- DECIDE ----
            # Cycle through tools: search -> extract -> summarize -> answer
            if step == 1:
                chosen = "search_web"
                args = {"query": "latest AI news"}
            elif step == 2:
                chosen = "extract_content"
                args = {"url": "techcrunch.com/gpt5"}
            elif step == 3:
                chosen = "summarize"
                text = self.mem.context()
                args = {"text": text[:300]}
            elif step == 4:
                chosen = "search_web"
                args = {"query": "AI agent frameworks"}
            elif step == 5:
                chosen = "extract_content"
                args = {"url": "theverge.com/claude4"}
            else:
                # Final step: answer
                ctx2 = self.mem.context()
                ans_raw = self.llm.complete(
                    f"Collected info:\n{ctx2}\nFinal answer:", max_new_tokens=60
                )
                ans = _clean(ans_raw, multi=True) or "Research completed."
                self._answer(ans)
                self.history.append({
                    "step": step, "thought": thought,
                    "action": "answer", "args": {},
                    "observation": ans,
                })
                self.mem.add("agent", f"answer: {ans}")
                return ans

            self._action(chosen, args)

            # ---- EXECUTE ----
            tool = self.tools.get(chosen)
            obs = tool.run(**args) if tool else f"[error] unknown tool {chosen}"
            self._obs(obs)

            self.mem.add("tool", f"{chosen} => {obs[:120]}")
            self.history.append({
                "step": step, "thought": thought,
                "action": chosen, "args": args, "observation": obs[:120],
            })

        # fallback (shouldn't reach here)
        ans = _clean(self.llm.complete(
            f"Final summary of:\n{self.mem.context()}", max_new_tokens=60
        ), multi=True) or "Task completed."
        self._answer(ans)
        return ans

    def trace(self):
        """Print execution trace."""
        print(f"\n{self._rule()}\n  EXECUTION TRACE\n{self._rule()}")
        for h in self.history:
            s = h["step"]
            t = h["thought"][:70]
            a = h["action"]
            o = h.get("observation", "")[:70]
            print(f"  step {s}: thought={t}")
            print(f"           action={a}  observation={o}")


# =============================================================================
# 6. Plan-and-Execute Agent
# =============================================================================

class PlanExecuteAgent:
    """Plan -> Execute (ReAct) -> Synthesize."""

    def __init__(self, llm: LocalLLM, tools: Toolbox):
        self.llm = llm
        self.tools = tools
        self.store = PersistentStore()

    def run(self, task: str) -> str:
        print(f"\n{ReActAgent._rule('=')}")
        print(f"  PLAN-AND-EXECUTE AGENT  |  task: {task}")
        print(f"{ReActAgent._rule('=')}")

        # Phase 1: Plan
        print(f"\n  >> Phase 1: PLAN")
        plan_raw = self.llm.complete(
            f"Plan for task '{task}':\nStep 1:", max_new_tokens=40
        )
        plan = _clean(plan_raw, multi=True) or "search, extract, summarize, answer"
        print(f"  Plan: 1. {plan}")

        # Phase 2: Execute
        print(f"\n  >> Phase 2: EXECUTE")
        agent = ReActAgent(self.llm, self.tools, max_steps=4)
        result = agent.run(task)

        # Phase 3: Synthesize
        print(f"\n  >> Phase 3: SYNTHESIZE")
        syn_raw = self.llm.complete(
            f"Plan: {plan}\nResults: {result[:200]}\nSynthesis:", max_new_tokens=50
        )
        syn = _clean(syn_raw, multi=True) or "Collected and summarized AI news."
        print(f"  Synthesis: {syn}")

        self.store.save_session(task, agent.max_steps)
        return f"{result}\n\n[Plan] {plan}\n[Synthesis] {syn}"


# =============================================================================
# 7. Utilities
# =============================================================================

def _clean(t: str, multi: bool = False) -> str:
    """Remove GPT-2 repetitions and truncate."""
    t = re.sub(r'(\S+\s+)\1{1,}', '', t)
    if multi:
        sentences = re.findall(r'[^.!?]*[.!?]', t)
        t = " ".join(sentences[:3])
    else:
        t = t.split(".")[0] if "." in t else t.split("\n")[0]
    return t.strip()[:150]


# =============================================================================
# 8. Main
# =============================================================================

def main():
    print("=" * 66)
    print("  MINI AGENT FRAMEWORK  |  Agent = LLM + Tools + Loop")
    print("=" * 66)

    # Init
    print("\n[init] Loading LLM ...")
    llm = LocalLLM()

    print("[init] Registering tools ...")
    tools = Toolbox()
    tools.add(Tool("search_web", "Search the web for news articles", search_web))
    tools.add(Tool("extract_content", "Extract full text from a URL", extract_article))
    tools.add(Tool("summarize", "Summarize a passage of text", summarize_text))
    for d in tools.describe():
        print(f"         + {d}")

    # ─── Demo 1: ReAct Agent ─────────────────────────────────
    print(f"\n{'#' * 66}")
    print("#  DEMO 1: ReAct Agent")
    print(f"{'#' * 66}")

    agent = ReActAgent(llm, tools)
    result1 = agent.run("Research and summarize AI news")
    agent.trace()

    print(f"\n{'#' * 66}")
    print("#  DEMO 1 DONE")
    print(f"{'#' * 66}")

    # ─── Demo 2: Plan-and-Execute Agent ──────────────────────
    print(f"\n{'#' * 66}")
    print("#  DEMO 2: Plan-and-Execute Agent")
    print(f"{'#' * 66}")

    planner = PlanExecuteAgent(llm, tools)
    result2 = planner.run("Find latest AI agent framework news")

    print(f"\n{'#' * 66}")
    print("#  DEMO 2 DONE")
    print(f"{'#' * 66}")

    # ─── Summary ─────────────────────────────────────────────
    print(f"\n{'=' * 66}")
    print("  SUMMARY")
    print(f"{'=' * 66}")
    print("  Agent = LLM + Tools + Loop")
    print("  ReAct: Thought -> Action -> Observation -> (loop)")
    print("  Plan-and-Execute: Plan -> Execute -> Synthesize")
    print("  Memory: Short-term + Long-term + Persistent")
    print(f"{'=' * 66}\n")


if __name__ == "__main__":
    main()
