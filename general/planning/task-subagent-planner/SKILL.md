---
name: task-subagent-planner
description: Use when the user marks a request with `【任务】`, starts with `task:` or `任务：`, or explicitly asks for subagent planning before execution. Return proposed `spawn_agent` commands for review and wait for approval before executing any subagents.
---

# Task Subagent Planner

Use this skill to turn a task-marked request into a review-first subagent plan.

## Triggers

Apply this skill when the user:

- explicitly includes `【任务】`
- starts the message with `task:` or `任务：`
- explicitly asks for subagent planning before execution

If a tool maps `/task` to the same workflow, treat it as equivalent. Do not assume slash-command support everywhere.

These triggers imply:

- return proposed subagent commands first
- do not execute subagents yet
- wait for explicit approval

## Workflow

1. Identify the deliverable, blockers, and parallelism opportunities.
2. Split the work into the smallest sensible independently executable subtasks.
3. Default to at most 3 proposed subagents unless the user asks for more.
4. Keep integration, cross-cutting decisions, and final verification with the main agent.
5. If the task is not meaningfully parallelizable, say so and return a reduced plan.

## Role Choice

- Use `explorer` for read-only codebase analysis or scoped investigation.
- Use `worker` for bounded implementation, tests, or verification with a clear write scope.
- Use `default` only when neither `explorer` nor `worker` is a better fit.

## Proposal Rules

- Do not call `spawn_agent` while producing the proposal.
- Return proposed command blocks only.
- For each proposed subagent include purpose, ownership boundary, and why it can run independently.
- Use `fork_context: true` when the subagent benefits from the current thread context.
- Prefer `gpt-5.4-mini` unless the task clearly needs a stronger model.
- Tell worker subagents they are not alone in the codebase, must not revert others' edits, and should adapt to concurrent changes.

## Output

Return the proposal in this order:

1. `任务拆分`
2. `建议的 subagent 命令`
3. `执行方式`
4. `确认语句`

## Command Template

```text
spawn_agent({
  "agent_type": "worker",
  "fork_context": true,
  "model": "gpt-5.4-mini",
  "reasoning_effort": "medium",
  "message": "..."
})
```

## Approval

Wait for explicit approval before execution. If the user revises the plan, regenerate it instead of executing the old one.
