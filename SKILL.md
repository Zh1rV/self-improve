---
name: self-improve
description: >-
  Autonomous codebase improvement loop that repeatedly identifies, implements,
  and validates high-impact low-risk changes with minimal supervision. Use when
  users ask for self-improvement or unattended iteration (for example: "self
  improve", "zidong youhua", "ziwo gaijin", "buyong dingzhe"), or want Codex to keep improving
  quality, tests, performance, and maintainability on its own.
---

# Self Improve

## Goal

Run short autonomous improvement cycles that ship safe, validated progress without waiting for user direction between each change.

## Default Profile

- Work in batches of `3-5` iterations.
- Keep each iteration scoped to one clearly bounded improvement.
- Prefer low-risk, high-signal changes first.
- Validate every iteration before moving to the next.
- Stop early when no safe, meaningful win is available.

## Cycle

1. Establish baseline.
- Check repository state, available test and lint commands, and known failures.
- Record a short baseline note before editing.

2. Select one target.
- Score candidates with `references/improvement-rubric.md`.
- Pick the top candidate with a clear validation path.

3. Implement minimal patch.
- Touch the fewest files needed.
- Preserve existing behavior unless explicitly fixing a bug.

4. Validate.
- Run the narrowest relevant checks first.
- Run broader checks when cost is low.
- If validation fails, fix immediately or revert that iteration.

5. Log and continue.
- Record what changed, why it matters, and validation evidence.
- Start the next iteration from the updated repository state.

## Communication Contract

At each checkpoint, report:
- Iteration objective
- Files changed
- Validation commands and key outcomes
- Residual risk

In the final report, include:
- Completed improvements in execution order
- Remaining high-value opportunities
- Recommended next actions

## Guardrails

- Never run destructive commands that can lose user data.
- Never rewrite git history unless explicitly requested.
- Ask before risky or irreversible operations (schema or data migrations, mass deletes, production credentials, external side effects).
- Avoid speculative refactors with weak validation coverage.
- Prefer stopping with a clear risk note over shipping uncertain changes.

## Quick Start Prompt

Use `$self-improve` to autonomously improve this repository in bounded, test-gated iterations and return a final change summary with evidence.
