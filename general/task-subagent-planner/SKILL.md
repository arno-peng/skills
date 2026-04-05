---
name: task-subagent-planner
description: Use when the user explicitly labels a request with `【任务】`, starts the message with `task:` or `任务：`, or uses the project command `/task` in tools that support project-local slash commands. Any of these triggers means the assistant should decompose the work into independently executable subagent tasks, return proposed `spawn_agent` command blocks for review, and wait for confirmation before any subagent is executed.
---

# Task Subagent Planner

Use this skill to turn a user-marked task into a review-first subagent plan.

## Trigger

Apply this skill when either condition is true:

- The user explicitly includes `【任务】`
- The user starts the message with `task:`
- The user starts the message with `任务：`
- The user explicitly uses `/task`
- The user explicitly asks to split work into subagent tasks and wants to review the commands before execution

If the user includes `【任务】`, starts with `task:` or `任务：`, or uses `/task`, that trigger already implies:

- return proposed subagent commands first
- do not execute any subagent yet
- wait for explicit approval before execution

## Goal

Produce a subagent execution proposal without running any subagents yet.

## Workflow

1. Read the user task and identify the concrete deliverable, constraints, and likely blocking dependencies.
2. Split the work into independently executable subtasks with clear ownership.
3. Prefer parallelizable subtasks with disjoint file, module, or responsibility boundaries.
4. If the task is not meaningfully parallelizable, say so and return a reduced plan instead of inventing parallelism.
5. Choose the smallest sensible set of subagents. Default to at most 3 proposed subagents unless the user explicitly asks for more.
6. Keep critical-path orchestration, cross-cutting decisions, and final integration with the main agent unless the user asks otherwise.

## Role Selection

- Use `explorer` for read-only codebase analysis, dependency tracing, or scoped investigation.
- Use `worker` for bounded implementation, tests, or verification with a clear write scope.
- Use `default` only when neither `explorer` nor `worker` is a better fit.

## Proposal Rules

- Do not call `spawn_agent` while producing the proposal.
- Return proposed command blocks only.
- Each proposed subagent must include:
  - purpose
  - ownership boundary
  - why it can run independently
  - a ready-to-run `spawn_agent` block
- Use `fork_context: true` when the subagent benefits from the current thread context.
- Prefer `gpt-5.4-mini` for straightforward bounded subtasks and stronger models only when complexity justifies it.
- Tell worker subagents they are not alone in the codebase, they must not revert others' edits, and they should adapt to concurrent changes.

## Output Format

Return the proposal in this order:

1. `任务拆分`
   - A short list of subtasks with dependency notes
2. `建议的 subagent 命令`
   - One fenced `text` block per proposed `spawn_agent` call
3. `执行方式`
   - State whether the plan is parallel or partially serial
4. `确认语句`
   - Ask the user for explicit approval before any execution

## Command Template

Use this exact shape for each proposal:

```text
spawn_agent({
  "agent_type": "worker",
  "fork_context": true,
  "model": "gpt-5.4-mini",
  "reasoning_effort": "medium",
  "message": "..."
})
```

Adjust `agent_type`, `model`, and `message` to fit the subtask.

## Approval Gate

Wait for an explicit user confirmation such as:

- `执行`
- `按这个方案执行`
- `批准，开始`

If the user revises the plan, regenerate the proposal instead of executing the old one.
