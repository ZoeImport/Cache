#!/usr/bin/env python3
"""
custom_skill.py -- Skill System: Definition, Loading, Injection & Chaining

A self-contained demonstration of a skill-based prompt system, showing:
  1. Skill definition in YAML format (metadata, prompt, tools, permissions)
  2. Skill loader -- directory scanning, parsing, validation
  3. Prompt injection -- how a skill becomes part of the LLM prompt
  4. Skill chaining -- composing skills in a pipeline
  5. Context window token budgeting strategy

Skills defined:
  1. web_researcher -- Browse the web, fetch pages, extract information
  2. code_writer    -- Read/write files, run commands, review patches
  3. system_admin   -- Manage configs, monitor logs, restart services

Usage:
    python custom_skill.py

Uses only Python standard library + PyYAML (yaml).
"""

import json
import textwrap
from typing import Any


# =============================================================================
# 1. YAML Skill Definitions (embedded as strings for zero-dependency demo)
# =============================================================================

SKILL_YAML_DEFS = {
    "web_researcher": """
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
""",

    "code_writer": """
name: code_writer
version: 2.1.0
description: >
  Write, review, and refactor code across multiple languages.
  Can read existing files, run tests, and apply patches.

prompt: |
  You are a Code Writing specialist.
  - Read existing files before making changes.
  - Write clean, well-documented code following language idioms.
  - Run tests after making changes to verify correctness.
  - If tests fail, diagnose and fix before declaring success.

tools:
  - name: file_read
    description: Read contents of a file. Supports line ranges.
    permissions: [filesystem]
  - name: file_write
    description: Write content to a file. Creates directories if needed.
    permissions: [filesystem]
  - name: command_run
    description: Run a shell command. Has 30s timeout.
    permissions: [execution]

permissions:
  network: false
  filesystem: true
  execution: true

constraints:
  max_tokens: 8192
  timeout_ms: 60000
  allowed_paths: ["/home/zoe/CodeSpace"]
""",

    "system_admin": """
name: system_admin
version: 1.2.0
description: >
  Manage system configurations, monitor services, and
  perform administrative tasks on Linux servers.

prompt: |
  You are a System Administration specialist.
  - Always confirm before making destructive changes.
  - Use sudo sparingly and log all privileged actions.
  - Check service status before restarting.
  - Roll back configurations if something goes wrong.

tools:
  - name: service_status
    description: Check status of a systemd service.
    permissions: [execution]
  - name: config_edit
    description: Edit a configuration file with backup.
    permissions: [filesystem]
  - name: log_tail
    description: Tail the last N lines of a log file.
    permissions: [filesystem]

permissions:
  network: false
  filesystem: true
  execution: true

constraints:
  max_tokens: 4096
  timeout_ms: 120000
  require_confirmation: true
""",
}


# =============================================================================
# 2. Skill Data Structures
# =============================================================================

class ToolDef:
    """A tool that a skill can use."""
    def __init__(self, name: str, description: str, permissions: list[str]):
        self.name = name
        self.description = description
        self.permissions = permissions

    def __repr__(self) -> str:
        return f"Tool({self.name})"


class Skill:
    """A loaded skill with its prompt, tools, and constraints."""
    def __init__(self, raw: dict[str, Any]):
        self.name: str = raw["name"]
        self.version: str = raw.get("version", "0.0.1")
        self.description: str = raw.get("description", "").strip()
        self.prompt: str = textwrap.dedent(raw.get("prompt", "")).strip()
        self.tools: list[ToolDef] = [
            ToolDef(t["name"], t["description"], t.get("permissions", []))
            for t in raw.get("tools", [])
        ]
        self.permissions: dict[str, bool] = raw.get("permissions", {})
        self.constraints: dict[str, Any] = raw.get("constraints", {})

    @property
    def tool_list_text(self) -> str:
        """Format tool list for prompt injection."""
        lines = ["Available tools:"]
        for t in self.tools:
            lines.append(f"  - {t.name}: {t.description}")
        return "\n".join(lines)

    @property
    def constraint_text(self) -> str:
        """Format constraints for prompt injection."""
        return "\n".join(f"  {k}: {v}" for k, v in self.constraints.items())

    def __repr__(self) -> str:
        return f"Skill(name={self.name!r}, tools={len(self.tools)}, version={self.version})"


# =============================================================================
# 3. Skill Loader -- Parses YAML definitions into Skill objects
# =============================================================================

class SkillLoader:
    """
    Scans a directory for .yaml/.yml skill definitions and loads them.
    In production, this reads from the filesystem. Here we use embedded YAML.
    """
    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def load_from_dict(self, yaml_defs: dict[str, str]) -> dict[str, Skill]:
        """Parse YAML strings into Skill objects."""
        import yaml
        for name, yaml_text in yaml_defs.items():
            raw: dict[str, Any] = yaml.safe_load(yaml_text)
            skill = Skill(raw)
            self._skills[skill.name] = skill
        return self._skills

    def get(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def list_skills(self) -> list[Skill]:
        return list(self._skills.values())


# =============================================================================
# 4. Prompt Injector -- Embeds skill context into a system prompt
# =============================================================================

class PromptInjector:
    """
    Injects skill definitions into an LLM system prompt.
    Demonstrates the 4-level prompt hierarchy:
      Engine-level -> Skill-level -> Task-level -> User input
    """

    ENGINE_PROMPT = textwrap.dedent("""\
    You are an AI assistant with dynamic skill injection.
    Your core capabilities include: reasoning, planning, and tool use.
    Always follow the active skill's instructions.
    """)

    @staticmethod
    def build_system_prompt(skill: Skill, task_instruction: str = "") -> str:
        """Assemble the full system prompt by layering skill on top of engine."""

        sections = {
            "engine": PromptInjector.ENGINE_PROMPT,
            "skill_header": f"--- Active Skill: {skill.name} v{skill.version} ---",
            "skill_description": skill.description,
            "skill_prompt": skill.prompt,
            "skill_tools": skill.tool_list_text,
            "skill_constraints": "Constraints:\n" + skill.constraint_text,
            "task": f"--- Task Instruction ---\n{task_instruction}".strip(),
        }

        # Layered assembly: engine <- skill <- task
        layers = [
            sections["engine"],
            "# Skill Context",
            sections["skill_header"],
            sections["skill_description"],
            sections["skill_prompt"],
            sections["skill_tools"],
            sections["skill_constraints"],
        ]
        if task_instruction:
            layers.append(sections["task"])

        return "\n\n".join(layers)

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Rough token estimation (4 chars ~= 1 token)."""
        return len(text) // 4


# =============================================================================
# 5. Skill Chainer -- Composes multiple skills in a pipeline
# =============================================================================

class SkillChainer:
    """
    Chains multiple skills together for complex workflows.
    Patterns:
      - Sequential: Skill A -> Skill B -> Skill C
      - Supervisor: Orchestrator delegates to sub-skills
      - Ensemble: Run skills in parallel, vote on results
    """

    def __init__(self, skills: dict[str, Skill]):
        self.skills = skills

    def chain_sequential(self, skill_names: list[str], task: str) -> list[dict]:
        """Execute skills one after another, each building on previous output."""
        results = []
        context_so_far = task

        for i, name in enumerate(skill_names, 1):
            skill = self.skills.get(name)
            if not skill:
                results.append({"skill": name, "error": "Skill not found"})
                continue

            prompt = PromptInjector.build_system_prompt(
                skill, f"Step {i}: {context_so_far}"
            )
            token_cost = PromptInjector.estimate_tokens(prompt)

            results.append({
                "step": i,
                "skill": name,
                "prompt_length": len(prompt),
                "tokens_estimate": token_cost,
                "prompt_preview": prompt[:300] + "...",
            })

            # Simulate passing context to next skill
            context_so_far = f"[Completed: {name}] {task}"

        return results

    def chain_supervisor(self, task: str, sub_skills: list[str]) -> dict:
        """Orchestrator skill delegates sub-tasks to specialist skills."""
        orchestrator = self.skills.get("system_admin")
        if not orchestrator:
            return {"error": "Orchestrator skill not found"}

        system_prompt = PromptInjector.build_system_prompt(
            orchestrator,
            f"Orchestrate the following task using available specialist skills.\n"
            f"Task: {task}\n"
            f"Available specialists: {', '.join(sub_skills)}"
        )

        sub_plans = []
        for sub in sub_skills:
            skill = self.skills.get(sub)
            if skill:
                sub_plans.append({
                    "specialist": sub,
                    "prompt": skill.prompt[:100] + "...",
                })

        return {
            "orchestrator": orchestrator.name,
            "system_prompt_tokens": PromptInjector.estimate_tokens(system_prompt),
            "delegated_to": sub_plans,
        }

    def chain_ensemble(self, skill_names: list[str], task: str) -> dict:
        """Run multiple skills on the same task and compare results."""
        votes = []
        for name in skill_names:
            skill = self.skills.get(name)
            if not skill:
                continue
            prompt = PromptInjector.build_system_prompt(skill, task)
            votes.append({
                "skill": name,
                "perspective": skill.description[:80] + "...",
                "prompt_tokens": PromptInjector.estimate_tokens(prompt),
            })

        return {
            "task": task,
            "ensemble_size": len(votes),
            "votes": votes,
            "strategy": "Majority vote on best approach",
        }


# =============================================================================
# 6. Context Window Budget Manager
# =============================================================================

class TokenBudget:
    """Simulates context window management with token budgets."""

    # Typical context windows
    WINDOW_SIZES = {
        "small": 4096,
        "medium": 8192,
        "large": 32768,
        "xlarge": 131072,
    }

    # Budget allocation percentages
    DEFAULT_BUDGET = {
        "system_prompt": 0.20,
        "skill_context": 0.15,
        "conversation_history": 0.35,
        "tool_results": 0.20,
        "reserved": 0.10,
    }

    @classmethod
    def plan(cls, window: str = "medium") -> dict:
        """Create a token budget plan for a given context window."""
        total = cls.WINDOW_SIZES.get(window, 8192)
        budget = {}
        for category, pct in cls.DEFAULT_BUDGET.items():
            budget[category] = int(total * pct)

        budget["total"] = total
        budget["window_label"] = window
        budget["used"] = sum(v for k, v in budget.items()
                            if k not in ("total", "window_label", "used"))
        budget["headroom"] = total - budget["used"]

        return budget

    @classmethod
    def optimize_for_skill(cls, skill: Skill, window: str = "medium") -> dict:
        """Adjust budget based on skill characteristics."""
        plan = cls.plan(window)

        # Skills with more tools need more tool_result space
        if len(skill.tools) > 3:
            plan["tool_results"] += int(plan["total"] * 0.05)
            plan["system_prompt"] -= int(plan["total"] * 0.05)

        # Skills with execution permissions may produce large outputs
        if skill.permissions.get("execution"):
            plan["tool_results"] += int(plan["total"] * 0.05)
            plan["conversation_history"] -= int(plan["total"] * 0.05)

        plan["used"] = sum(v for k, v in plan.items()
                           if k not in ("total", "window_label", "used", "headroom"))
        plan["headroom"] = plan["total"] - plan["used"]

        return plan


# =============================================================================
# 7. Main Demonstration
# =============================================================================

SEPARATOR = "=" * 72

def print_header(title: str):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def main():
    print("  Skill & Prompt System Demonstration")
    print("  技能与提示词系统演示")
    print(f"  Python: {__import__('sys').version}")
    print(SEPARATOR)

    # ---------------------------------------------------------------
    # Phase 1: Load skills from YAML definitions
    # ---------------------------------------------------------------
    print_header("Phase 1: Loading Skill Definitions from YAML")

    loader = SkillLoader()
    skills = loader.load_from_dict(SKILL_YAML_DEFS)

    print(f"Loaded {len(skills)} skills:")
    for skill in skills.values():
        print(f"  [{skill.name:16s}] v{skill.version:5s}  |  "
              f"{len(skill.tools)} tools  |  "
              f"permissions: {', '.join(k for k,v in skill.permissions.items() if v)}")

    # ---------------------------------------------------------------
    # Phase 2: Show a complete YAML skill definition
    # ---------------------------------------------------------------
    print_header("Phase 2: Complete Skill Definition (web_researcher)")

    print(SKILL_YAML_DEFS["web_researcher"])

    # ---------------------------------------------------------------
    # Phase 3: Prompt Injection -- build system prompt from skill
    # ---------------------------------------------------------------
    print_header("Phase 3: Prompt Injection")

    researcher = skills["web_researcher"]
    system_prompt = PromptInjector.build_system_prompt(
        researcher,
        task_instruction="Search for the latest AI research papers on multi-agent systems."
    )
    print("Assembled System Prompt:")
    print("-" * 72)
    print(system_prompt)
    print("-" * 72)
    print(f"Prompt length: {len(system_prompt)} chars")
    print(f"Estimated tokens: {PromptInjector.estimate_tokens(system_prompt)}")

    # ---------------------------------------------------------------
    # Phase 4: Skill Chaining -- Sequential workflow
    # ---------------------------------------------------------------
    print_header("Phase 4: Skill Chaining (Sequential)")

    chainer = SkillChainer(skills)
    chain_result = chainer.chain_sequential(
        ["web_researcher", "code_writer"],
        "Research the latest Python async patterns and write a code example."
    )

    for step in chain_result:
        print(f"\nStep {step['step']}: {step['skill']}")
        print(f"  Prompt tokens : {step['tokens_estimate']}")
        print(f"  Prompt preview: {step['prompt_preview'][:120]}...")

    # ---------------------------------------------------------------
    # Phase 5: Skill Chaining -- Supervisor pattern
    # ---------------------------------------------------------------
    print_header("Phase 5: Skill Chaining (Supervisor Pattern)")

    supervisor_plan = chainer.chain_supervisor(
        "Deploy the web application to production",
        ["code_writer", "system_admin"]
    )
    print(f"Orchestrator    : {supervisor_plan['orchestrator']}")
    print(f"Prompt tokens   : {supervisor_plan['system_prompt_tokens']}")
    print(f"Delegated to    :")
    for sub in supervisor_plan["delegated_to"]:
        print(f"  - {sub['specialist']}: {sub['prompt']}")

    # ---------------------------------------------------------------
    # Phase 6: Skill Chaining -- Ensemble pattern
    # ---------------------------------------------------------------
    print_header("Phase 6: Skill Chaining (Ensemble Pattern)")

    ensemble = chainer.chain_ensemble(
        ["web_researcher", "code_writer", "system_admin"],
        "What is the best approach to deploy a Python web app?"
    )
    print(f"Task            : {ensemble['task']}")
    print(f"Ensemble size   : {ensemble['ensemble_size']}")
    print(f"Verdict strategy: {ensemble['strategy']}")
    for v in ensemble["votes"]:
        print(f"  [{v['skill']:16s}] tokens={v['prompt_tokens']:5d}  |  {v['perspective']}")

    # ---------------------------------------------------------------
    # Phase 7: Context Window Token Budgeting
    # ---------------------------------------------------------------
    print_header("Phase 7: Token Budget Planning")

    for window in ["small", "medium", "large", "xlarge"]:
        plan = TokenBudget.plan(window)
        print(f"\nContext window: {plan['window_label']:6s} ({plan['total']:6d} tokens)")
        for cat in ["system_prompt", "skill_context", "conversation_history",
                     "tool_results", "reserved"]:
            bar = "█" * (plan[cat] // 100)
            print(f"  {cat:22s}: {plan[cat]:5d} tokens {bar}")
        print(f"  {'headroom':22s}: {plan['headroom']:5d} tokens (available)")

    # Optimized budget for a code_writer skill
    print_header("Phase 7b: Optimized Budget for code_writer")

    optimized = TokenBudget.optimize_for_skill(skills["code_writer"], "large")
    print(f"Context window : {optimized['window_label']:6s} ({optimized['total']:6d} total)")
    print(f"(Adjusted for code_writer: 4 tools + execution permissions)")
    for cat in ["system_prompt", "skill_context", "conversation_history",
                 "tool_results", "reserved", "headroom"]:
        print(f"  {cat:22s}: {optimized[cat]:5d} tokens")

    # ---------------------------------------------------------------
    # Phase 8: Prompt Hierarchy Visualization
    # ---------------------------------------------------------------
    print_header("Phase 8: Prompt Hierarchy (4-Level Model)")

    print("""
    Level 0: Engine Prompt
    +----------------------------------------------------+
    | You are an AI assistant with dynamic skill...      |  <-- Core identity, rarely changes
    +----------------------------------------------------+
                              |
    Level 1: Skill Prompt (injected)
    +----------------------------------------------------+
    | --- Active Skill: web_researcher v1.0.0 ---        |  <-- Skill name & version
    | Research any topic by searching the web...          |  <-- Skill description
    | You are a Web Research specialist.                  |  <-- Behavioral prompt
    | Available tools:                                    |
    |   - web_search: Search the web for a query...       |  <-- Tool definitions
    |   - web_fetch: Fetch the full content of a URL...   |  <-- Tool definitions
    | Constraints:                                        |
    |   max_tokens: 4096                                  |  <-- Guardrails
    +----------------------------------------------------+
                              |
    Level 2: Task Prompt
    +----------------------------------------------------+
    | --- Task Instruction ---                            |  <-- Specific task
    | Search for the latest AI research papers...         |  <-- User's request
    +----------------------------------------------------+
                              |
    Level 3: User Input (conversation turns)
    +----------------------------------------------------+
    | User: Can you find papers about multi-agent...      |  <-- Actual dialogue
    | Assistant: Here are the latest papers...            |  <-- Model response
    +----------------------------------------------------+
    """)

    print(f"\n{SEPARATOR}")
    print("  Demonstration Complete")
    print(f"{SEPARATOR}")


if __name__ == "__main__":
    main()
