#!/usr/bin/env python3
"""
agent_harness_demo.py — Mini Agent Harness from Scratch

A minimal but complete agent harness demonstrating the core architecture:
  - Scheduling: task decomposition → sub-agent dispatch → result collection
  - Tool system: Tool Calling + MCP-like protocol
  - Skill system: dynamic loading and injection
  - Memory: conversation history + file state
  - Permission: file operations sandboxing

Task: "Create a file with content"
All decisions are simulated (no LLM API required).
Uses only Python standard library + json + asyncio.

Usage:
    python agent_harness_demo.py
"""

import asyncio
import json
import os
import shutil
import tempfile
import textwrap
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# =============================================================================
# 1. Core Data Structures
# =============================================================================

class PermissionLevel(Enum):
    """Sandbox permission levels for tools."""
    READ_ONLY = "read_only"       # Can read, cannot write
    READ_WRITE = "read_write"     # Can read and write
    EXECUTE = "execute"           # Can execute shell commands


class ToolCallStatus(Enum):
    """Status of a tool call execution."""
    SUCCESS = "success"
    FAILURE = "failure"
    PERMISSION_DENIED = "permission_denied"


@dataclass
class ToolCall:
    """A single tool call request/response pair."""
    name: str
    args: dict[str, Any]
    result: Any = None
    status: ToolCallStatus = ToolCallStatus.SUCCESS
    error: str | None = None
    permission: PermissionLevel = PermissionLevel.READ_WRITE
    timestamp: float = 0.0

    def __post_init__(self):
        self.timestamp = time.time()


@dataclass
class Memory:
    """Agent memory: conversation history + file state + learned facts."""
    conversation: list[dict] = field(default_factory=list)
    file_state: dict[str, str] = field(default_factory=dict)  # path -> content
    facts: list[str] = field(default_factory=list)

    def add_message(self, role: str, content: str):
        self.conversation.append({"role": role, "content": content})

    def get_context(self) -> str:
        lines = []
        for msg in self.conversation[-10:]:  # sliding window
            lines.append(f"[{msg['role']}] {msg['content']}")
        return "\n".join(lines)

    def record_file(self, path: str, content: str):
        self.file_state[path] = content

    def add_fact(self, fact: str):
        if fact not in self.facts:
            self.facts.append(fact)


# =============================================================================
# 2. Sandbox / Permission System
# =============================================================================

class Sandbox:
    """
    File operations sandbox.
    Prevents dangerous operations outside allowed directories.
    """

    def __init__(self, workspace: str):
        self.workspace = os.path.abspath(workspace)
        self.allowed_dirs = {self.workspace}
        self._ensure_workspace()

    def _ensure_workspace(self):
        os.makedirs(self.workspace, exist_ok=True)

    def resolve_path(self, path: str) -> str:
        """Resolve a relative path to an absolute path within workspace."""
        if os.path.isabs(path):
            resolved = os.path.normpath(path)
        else:
            resolved = os.path.normpath(os.path.join(self.workspace, path))
        return resolved

    def check_permission(self, path: str, level: PermissionLevel) -> bool:
        """Check if a path is within the sandbox and allowed for the given level."""
        resolved = self.resolve_path(path)
        allowed = any(
            resolved.startswith(d) for d in self.allowed_dirs
        )
        if not allowed:
            return False
        if level == PermissionLevel.EXECUTE:
            return False  # execution not allowed in this demo
        return True

    def check_read(self, path: str) -> bool:
        return self.check_permission(path, PermissionLevel.READ_ONLY)

    def check_write(self, path: str) -> bool:
        return self.check_permission(path, PermissionLevel.READ_WRITE)


# =============================================================================
# 3. Tool System (MCP-like Protocol)
# =============================================================================

@dataclass
class ToolSpec:
    """Tool specification — name + description + input_schema (MCP style)."""
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable
    permission: PermissionLevel = PermissionLevel.READ_WRITE


class ToolRegistry:
    """
    Tool registry with MCP-like tool definition.
    Each tool has: name, description, input_schema, handler, permission.
    """

    def __init__(self):
        self._tools: dict[str, ToolSpec] = {}

    def register(self, tool: ToolSpec):
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """Return tool definitions in MCP format."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.input_schema,
                "permission": t.permission.value,
            }
            for t in self._tools.values()
        ]

    def execute(self, name: str, args: dict, sandbox: Sandbox,
                memory: Memory) -> ToolCall:
        """Execute a tool call with permission checking."""
        spec = self._tools.get(name)
        if spec is None:
            return ToolCall(name, args, status=ToolCallStatus.FAILURE,
                            error=f"Unknown tool: {name}")

        # Permission check
        if "path" in args:
            if not sandbox.check_permission(args["path"], spec.permission):
                return ToolCall(name, args, status=ToolCallStatus.PERMISSION_DENIED,
                                error=f"Permission denied: {args['path']} "
                                      f"requires {spec.permission.value}")

        # Execute
        try:
            result = spec.handler(**args, sandbox=sandbox, memory=memory)
            return ToolCall(name, args, result=result, status=ToolCallStatus.SUCCESS)
        except Exception as e:
            return ToolCall(name, args, status=ToolCallStatus.FAILURE,
                            error=str(e))


# =============================================================================
# 4. Tool Handlers (Simulated)
# =============================================================================

def handler_read_file(path: str, sandbox: Sandbox, **kwargs) -> str:
    """Read a file from the sandbox."""
    full_path = sandbox.resolve_path(path)
    if os.path.exists(full_path):
        with open(full_path, "r") as f:
            return f.read()
    return f"[ERROR] File not found: {path}"


def handler_write_file(path: str, content: str, sandbox: Sandbox,
                       memory: Memory) -> str:
    """Write content to a file in the sandbox."""
    full_path = sandbox.resolve_path(path)
    os.makedirs(os.path.dirname(full_path) or ".", exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)
    memory.record_file(path, content)
    return f"Written {len(content)} bytes to {path}"


def handler_list_files(sandbox: Sandbox, pattern: str = "*", **kwargs) -> str:
    """List files in the sandbox workspace."""
    import glob
    full_pattern = os.path.join(sandbox.workspace, pattern)
    files = glob.glob(full_pattern)
    if not files:
        return "(no files found)"
    return "\n".join(f"  - {os.path.relpath(f, sandbox.workspace)}" for f in files)


def handler_create_directory(path: str, sandbox: Sandbox, **kwargs) -> str:
    """Create a directory in the sandbox."""
    full_path = sandbox.resolve_path(path)
    os.makedirs(full_path, exist_ok=True)
    return f"Directory created: {path}"


def handler_search_text(pattern: str, sandbox: Sandbox, path: str = ".",
                        **kwargs) -> str:
    """Search for text in files within the sandbox."""
    full_path = sandbox.resolve_path(path)
    results = []
    for root, dirs, files in os.walk(full_path):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r") as f:
                    for i, line in enumerate(f, 1):
                        if pattern in line:
                            rel = os.path.relpath(fpath, sandbox.workspace)
                            results.append(f"  {rel}:{i}: {line.strip()[:80]}")
            except (UnicodeDecodeError, IsADirectoryError):
                continue
    return "\n".join(results[:20]) if results else "(no matches found)"


# =============================================================================
# 5. Skill System
# =============================================================================

@dataclass
class Skill:
    """
    A skill = prompt template + tool set + guardrails.
    Skills can be dynamically loaded and injected into the agent.
    """
    name: str
    description: str
    prompt_template: str
    required_tools: list[str]
    guardrails: list[str] = field(default_factory=list)


SKILLS_REGISTRY: dict[str, Skill] = {}


def register_skill(skill: Skill):
    SKILLS_REGISTRY[skill.name] = skill


def load_skill(name: str, registry: ToolRegistry) -> Skill | None:
    """Dynamically load a skill: read definition -> validate -> inject tools."""
    skill = SKILLS_REGISTRY.get(name)
    if skill is None:
        return None

    # Validate that required tools exist
    missing = [t for t in skill.required_tools if registry.get(t) is None]
    if missing:
        print(f"  [SKILL] Warning: missing tools for '{name}': {missing}")

    return skill


def inject_skill_prompt(skill: Skill) -> str:
    """Inject skill prompt into system prompt."""
    parts = [
        f"--- Skill: {skill.name} ---",
        skill.prompt_template,
        "",
        "Guardrails:",
    ]
    for g in skill.guardrails:
        parts.append(f"  - {g}")
    return "\n".join(parts)


# Register built-in skills
register_skill(Skill(
    name="file_operations",
    description="Create, read, update, and delete files",
    prompt_template=(
        "You are a file operations specialist. "
        "You can create files with content, read existing files, "
        "and organize directories."
    ),
    required_tools=["read_file", "write_file", "list_files", "create_directory"],
    guardrails=[
        "Never write to paths outside the workspace",
        "Always read before overwriting",
        "Create parent directories as needed",
    ],
))

register_skill(Skill(
    name="code_generator",
    description="Generate code files with proper structure",
    prompt_template=(
        "You are a code generation specialist. "
        "You write clean, well-documented code following best practices."
    ),
    required_tools=["read_file", "write_file", "search_text"],
    guardrails=[
        "Include docstrings and comments",
        "Follow PEP 8 style",
        "Never overwrite without reading first",
    ],
))


# =============================================================================
# 6. Scheduling / Agent Orchestration
# =============================================================================

class Agent:
    """
    Master agent with scheduling: receives high-level task →
    decomposes into sub-tasks → dispatches to sub-agents →
    collects results → verifies → merges.
    """

    def __init__(self, registry: ToolRegistry, sandbox: Sandbox):
        self.registry = registry
        self.sandbox = sandbox
        self.memory = Memory()
        self.active_skills: list[Skill] = []
        self.sub_agents: list["SubAgent"] = []

    def load_skill(self, name: str):
        """Dynamically load and inject a skill."""
        skill = load_skill(name, self.registry)
        if skill:
            self.active_skills.append(skill)
            prompt = inject_skill_prompt(skill)
            self.memory.add_message("system", prompt)
            print(f"  [SKILL] Loaded: {skill.name}")

    def _choose_skill(self, task: str) -> Skill | None:
        """Select the best skill for a given task (simulated)."""
        task_lower = task.lower()
        # Simple keyword-based skill selection
        if "file" in task_lower or "create" in task_lower:
            return SKILLS_REGISTRY.get("file_operations")
        if "code" in task_lower or "generate" in task_lower:
            return SKILLS_REGISTRY.get("code_generator")
        return None

    def decompose(self, task: str) -> list[dict]:
        """Decompose a high-level task into atomic sub-tasks (simulated)."""
        self.memory.add_message("system", f"Decomposing task: {task}")
        print(f"\n  [PLANNER] Decomposing: '{task}'")

        # Simulated task decomposition
        if "create" in task.lower() and "file" in task.lower():
            sub_tasks = [
                {"id": "st-1", "action": "check_workspace",
                 "description": "Verify workspace exists and is clean",
                 "tool": "list_files", "args": {"pattern": "*"}},
                {"id": "st-2", "action": "create_directories",
                 "description": "Create necessary directory structure",
                 "tool": "create_directory", "args": {"path": "output"}},
                {"id": "st-3", "action": "write_content",
                 "description": "Write the actual file content",
                 "tool": "write_file",
                 "args": {"path": "output/hello.txt",
                          "content": "Hello from Agent Harness!\n"
                                     "This file was created by an autonomous agent.\n"
                                     f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"}},
                {"id": "st-4", "action": "verify",
                 "description": "Verify the file was created correctly",
                 "tool": "read_file", "args": {"path": "output/hello.txt"}},
            ]
            print(f"  [PLANNER] Decomposed into {len(sub_tasks)} sub-tasks:")
            for st in sub_tasks:
                print(f"    {st['id']}: {st['description']} "
                      f"→ {st['tool']}(...{short_args(st['args'])}...)")
            return sub_tasks

        # Generic decomposition
        return [
            {"id": "st-1", "action": "plan",
             "description": "Understand the task and create a plan",
             "tool": "_internal_think", "args": {"task": task}},
            {"id": "st-2", "action": "execute",
             "description": "Execute the planned steps",
             "tool": "_internal_think", "args": {"task": task}},
        ]

    async def run(self, task: str) -> str:
        """Main agent loop."""
        print(f"\n{'='*70}")
        print(f"  AGENT HARNESS")
        print(f"  Task: {task}")
        print(f"{'='*70}")

        # 1. Choose and load skill
        skill = self._choose_skill(task)
        if skill:
            self.load_skill(skill.name)
        else:
            print("  [SKILL] No matching skill found, using defaults")

        print(f"\n  [STATE] Active skills: "
              f"{[s.name for s in self.active_skills]}")
        print(f"  [STATE] Available tools: "
              f"{[t['name'] for t in self.registry.list_tools()]}")

        # 2. Decompose task
        sub_tasks = self.decompose(task)
        self.memory.add_message("system",
                                f"Plan: {len(sub_tasks)} sub-tasks")

        # 3. Dispatch sub-tasks (simulated parallel execution)
        print(f"\n{'─'*70}")
        print(f"  EXECUTION PHASE")
        print(f"{'─'*70}")

        results = await self._execute_plan(sub_tasks)

        # 4. Verify and merge
        print(f"\n{'─'*70}")
        print(f"  VERIFICATION PHASE")
        print(f"{'─'*70}")
        final_result = self._verify_and_merge(results, task)

        # 5. Summary
        print(f"\n{'='*70}")
        print(f"  FINAL RESULT")
        print(f"{'='*70}")
        print(f"  {final_result[:500]}")

        self._print_summary()
        return final_result

    async def _execute_plan(self, sub_tasks: list[dict]) -> list[ToolCall]:
        """Execute sub-tasks, collecting results."""
        results = []
        for i, st in enumerate(sub_tasks):
            print(f"\n  >> Sub-task {i+1}/{len(sub_tasks)}: {st['id']}")
            print(f"     Action: {st['description']}")

            # Simulate thinking
            await asyncio.sleep(0.05)
            self.memory.add_message("agent",
                                    f"Executing {st['id']}: {st['description']}")

            # Execute tool call
            call = self.registry.execute(
                st["tool"], st["args"], self.sandbox, self.memory
            )

            # Record result
            self._print_tool_call(call)
            results.append(call)

            if call.status == ToolCallStatus.FAILURE:
                # Simulate retry logic
                print(f"     ⚠  Retrying once...")
                call = self.registry.execute(
                    st["tool"], st["args"], self.sandbox, self.memory
                )
                self._print_tool_call(call)
                results[-1] = call

        return results

    def _print_tool_call(self, call: ToolCall):
        """Pretty-print a tool call and its result."""
        status_icon = {
            ToolCallStatus.SUCCESS: "✓",
            ToolCallStatus.FAILURE: "✗",
            ToolCallStatus.PERMISSION_DENIED: "⛔",
        }.get(call.status, "?")

        print(f"     Tool: {call.name}({short_args(call.args)})")
        print(f"     Status: {status_icon} {call.status.value}")

        if call.result:
            result_str = str(call.result)[:200]
            print(f"     Result: {result_str}")
        if call.error:
            print(f"     Error: {call.error}")

    def _verify_and_merge(self, results: list[ToolCall],
                          task: str) -> str:
        """Verify results and produce final output."""
        successes = sum(1 for r in results if r.status == ToolCallStatus.SUCCESS)
        failures = sum(1 for r in results if r.status == ToolCallStatus.FAILURE)
        denied = sum(1 for r in results
                     if r.status == ToolCallStatus.PERMISSION_DENIED)

        print(f"  Results: {successes} success, "
              f"{failures} failure, {denied} denied")

        # Check file state
        if self.memory.file_state:
            print(f"  Files created/modified:")
            for path, content in self.memory.file_state.items():
                print(f"    - {path} ({len(content)} bytes)")

        # Learn facts
        self.memory.add_fact(f"Completed task: {task}")
        self.memory.add_fact(
            f"Created files: {list(self.memory.file_state.keys())}")

        # Build summary
        summary_parts = [
            f"Task completed: {task}",
            f"Sub-tasks: {len(results) - failures}/{len(results)} passed",
            f"Tools used: {len(set(r.name for r in results))} unique tools",
            f"Files modified: {len(self.memory.file_state)}",
            f"Facts learned: {len(self.memory.facts)}",
        ]
        if self.memory.file_state:
            summary_parts.append("\nCreated files:")
            for path, content in self.memory.file_state.items():
                summary_parts.append(f"  {path}: {len(content)} bytes")
        return "\n".join(summary_parts)

    def _print_summary(self):
        """Print final agent state summary."""
        print(f"\n{'─'*70}")
        print(f"  AGENT STATE SUMMARY")
        print(f"{'─'*70}")
        print(f"  Skills loaded: {len(self.active_skills)}")
        print(f"  Conversation turns: {len(self.memory.conversation)}")
        print(f"  Facts learned: {len(self.memory.facts)}")
        print(f"  Files tracked: {len(self.memory.file_state)}")
        print(f"  Sandbox workspace: {self.sandbox.workspace}")
        print(f"\n  Facts:")
        for f in self.memory.facts:
            print(f"    • {f}")


# =============================================================================
# 7. SubAgent (Simulated)
# =============================================================================

class SubAgent:
    """
    A simulated sub-agent that can be dispatched by the master agent.
    Each sub-agent has its own memory and tool access.
    """

    def __init__(self, name: str, role: str, registry: ToolRegistry,
                 sandbox: Sandbox):
        self.name = name
        self.role = role
        self.registry = registry
        self.sandbox = sandbox
        self.memory = Memory()

    async def execute(self, instruction: dict) -> ToolCall:
        """Execute a single instruction as a sub-agent."""
        print(f"    [SubAgent:{self.name}] Processing: {instruction.get('id', '?')}")
        self.memory.add_message("system", f"Role: {self.role}")
        self.memory.add_message("user", str(instruction))

        tool_name = instruction.get("tool", "")
        tool_args = instruction.get("args", {})
        call = self.registry.execute(tool_name, tool_args, self.sandbox,
                                     self.memory)
        return call


# =============================================================================
# 8. Main — Setup and Run
# =============================================================================

def short_args(args: dict) -> str:
    """Shorten argument display for printing."""
    parts = []
    for k, v in args.items():
        s = str(v)
        if len(s) > 40:
            s = s[:37] + "..."
        parts.append(f"{k}={s}")
    return ", ".join(parts)


async def main():
    """Setup sandbox, registry, and run the agent harness demo."""
    # Create temp workspace
    workspace = tempfile.mkdtemp(prefix="agent_harness_")
    print(f"Workspace: {workspace}")

    # Initialize sandbox
    sandbox = Sandbox(workspace)

    # Initialize tool registry
    registry = ToolRegistry()
    registry.register(ToolSpec(
        "read_file", "Read content from a file",
        {"type": "object", "properties": {"path": {"type": "string"}},
         "required": ["path"]},
        handler_read_file, PermissionLevel.READ_ONLY,
    ))
    registry.register(ToolSpec(
        "write_file", "Write content to a file",
        {"type": "object",
         "properties": {
             "path": {"type": "string"},
             "content": {"type": "string"},
         },
         "required": ["path", "content"]},
        handler_write_file, PermissionLevel.READ_WRITE,
    ))
    registry.register(ToolSpec(
        "list_files", "List files matching a pattern",
        {"type": "object",
         "properties": {"pattern": {"type": "string", "default": "*"}},
         "required": []},
        handler_list_files, PermissionLevel.READ_ONLY,
    ))
    registry.register(ToolSpec(
        "create_directory", "Create a new directory",
        {"type": "object", "properties": {"path": {"type": "string"}},
         "required": ["path"]},
        handler_create_directory, PermissionLevel.READ_WRITE,
    ))
    registry.register(ToolSpec(
        "search_text", "Search for text in files",
        {"type": "object",
         "properties": {
             "pattern": {"type": "string"},
             "path": {"type": "string", "default": "."},
         },
         "required": ["pattern"]},
        handler_search_text, PermissionLevel.READ_ONLY,
    ))

    # Run the agent
    agent = Agent(registry, sandbox)
    task = "Create a file with content: write 'Hello from Agent Harness!' to output/hello.txt"
    result = await agent.run(task)

    # Display created file content
    hello_path = os.path.join(workspace, "output", "hello.txt")
    if os.path.exists(hello_path):
        print(f"\n{'─'*70}")
        print(f"  VERIFICATION — File content:")
        print(f"{'─'*70}")
        with open(hello_path, "r") as f:
            print(textwrap.indent(f.read(), "    "))

    # Cleanup
    shutil.rmtree(workspace, ignore_errors=True)
    print(f"\n  (Workspace cleaned up: {workspace})")


if __name__ == "__main__":
    asyncio.run(main())
