# self-improve

[中文说明](./README.zh-CN.md)

`self-improve` is a Codex skill for running bounded, test-gated repository improvement loops.

It is designed to solve a common pain point in autonomous coding workflows: a model may be able to spot useful fixes, but without explicit guardrails it can drift, over-edit, skip validation, or make progress that is hard to inspect afterward.

This skill keeps the workflow simple and controlled:

1. Establish a baseline and identify candidate improvements.
2. Score and select a high-value, low-risk target.
3. Apply the smallest safe change.
4. Validate the result before continuing.
5. Repeat in short iterations until the budget is exhausted or no safe target remains.

## Core Logic Flow

The current version is built around a single-agent iterative loop rather than a multi-agent system.

- It favors short, repeated reasoning cycles instead of one very long chain-of-thought pass.
- Each round is expected to produce a bounded change with explicit validation evidence.
- The skill emphasizes observability and control over raw autonomy.

In other words, the loop is:

`baseline -> select target -> patch -> validate -> log -> continue or stop`

## Install

Install this skill into Codex from the repository root:

1. In Codex, ask it to install the skill from GitHub:
   `Use skill-installer to install this skill from GitHub: https://github.com/Zh1rV/self-improve.git`
2. Restart Codex after installation so the new skill is loaded.

Installed skill name:

- `self-improve`

## Repository Contents

- [`SKILL.md`](./SKILL.md): main skill definition and operating contract
- [`agents/openai.yaml`](./agents/openai.yaml): agent-facing metadata
- [`references/`](./references): operating references for scoring, validation order, checkpointing, rollback, and loop control
- [`scripts/`](./scripts): helper scripts for logging, checkpoint generation, candidate ranking, validation, and unattended loop execution

## Typical Use Case

Use this skill when you want Codex to improve a codebase continuously, but only through small, reviewable, test-backed iterations.
