---
name: self-improve
description: >-
  Autonomous codebase improvement loop that repeatedly identifies, implements,
  and validates high-impact, low-risk changes with minimal supervision. Use
  when users ask for self-improvement or unattended iteration (for example:
  "self improve", "auto optimize", "improve this repo continuously"), or
  when they want Codex to keep improving quality, tests, performance, and
  maintainability on its own.
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

## Execution Inputs

Capture these inputs before iteration starts:

- Repository path and working branch
- Iteration budget (count and optional timebox)
- Risk profile (`conservative`, `balanced`, or `aggressive`)
- Validation budget (fast-only vs full gates when needed)

See `references/profiles.md` for profile-specific defaults.
Use `references/branch-policy.md` for unattended branch hygiene.

## Autonomy Modes

- `unattended`: run the full batch automatically and escalate only on blocked or risky operations.
- `attended`: pause after each checkpoint and wait for user approval before the next iteration.

Default to `unattended` when the user explicitly asks for autonomous improvement.

## Cycle

1. Establish baseline.
- Check repository state, available test and lint commands, and known failures.
- Record a short baseline note before editing.
- Run `references/preflight-checklist.md` before unattended batches.

2. Select one target.
- Score candidates with `references/improvement-rubric.md`.
- Pick the top candidate with a clear validation path.
- Build candidates from failing checks, high-churn files, and critical TODO/FIXME markers.
- Use `references/improvement-patterns.md` when candidate quality is low and a safe seed target is needed.

3. Implement minimal patch.
- Touch the fewest files needed.
- Preserve existing behavior unless explicitly fixing a bug.

Patch size defaults:
- Prefer `<= 3` files changed per iteration.
- Prefer `<= 120` changed lines (excluding generated lockfiles).
- Split larger work into multiple iterations with separate validation.

4. Validate.
- Run the narrowest relevant checks first.
- Run broader checks when cost is low.
- If validation fails, fix immediately or revert that iteration.

5. Log and continue.
- Record what changed, why it matters, and validation evidence.
- Start the next iteration from the updated repository state.
- Keep a compact per-iteration line using `references/iteration-log.md`.

## Test Gate Ladder

Use this order unless project-specific constraints require otherwise:

If test commands are unknown, follow `references/command-discovery.md` first.
Use `references/validation-order.md` to choose depth by risk and blast radius.

1. Run the narrowest checks tied to changed files.
- Examples: focused unit tests, targeted type checks, local lint scopes.

2. Run project-level quality gates that are cheap enough.
- Examples: full lint, full type check, medium-cost test suites.

3. Run expensive full-suite checks only when risk justifies cost.
- Examples: end-to-end suites, integration stacks, heavy benchmarks.

If any gate fails, fix in-place and re-run from the failed gate onward.

## Failure Handling

- Allow at most `2` fix attempts for one iteration target.
- If attempts fail, revert the target change set with `references/rollback-playbook.md` and log why it failed.
- Do not retry the same target in the same batch unless new evidence appears.
- Move to the next candidate that satisfies the rubric constraints.

## Escalation Triggers

Pause and ask the user when any trigger appears:

- Required command for validation is unknown and cannot be discovered safely.
- Candidate change impacts security-sensitive or billing-critical paths.
- Fix requires external service changes outside the local repository.

## Communication Contract

At each checkpoint, report:
- Iteration objective
- Files changed
- Validation commands and key outcomes
- Residual risk

Use `references/checkpoint-template.md` as the default structure when reporting.
Optionally generate a checkpoint skeleton with `scripts/checkpoint_report.py`.

For each validation command, include:
- Exact command text
- Pass/fail status
- One key output line when available

Include a stop reason in checkpoints only when an iteration or batch stops.

In the final report, include:
- Completed improvements in execution order
- Remaining high-value opportunities
- Recommended next actions
- Stop reason code from `references/stop-reasons.md` when the batch ends early

## Guardrails

- Never run destructive commands that can lose user data.
- Never rewrite git history unless explicitly requested.
- Ask before risky or irreversible operations (schema or data migrations, mass deletes, production credentials, external side effects).
- Avoid speculative refactors with weak validation coverage.
- Prefer stopping with a clear risk note over shipping uncertain changes.

## Continuous Loop

For long-running unattended execution, use `scripts/run_loop.py`.
For one-round autonomous bug-hunt and self-heal, use `scripts/self_iterate_once.py`.
For a conservative long-run preset, use `scripts/stable_loop_profile.ps1`.
See `references/loop-mode.md` for start, stop, state, and log usage.

## Fast Self Test

Before and after changing this skill, run:

`python scripts/self_test.py`

This covers skill metadata validation, Python compilation, helper CLI behavior,
loop stop reasons, and the self-heal validation contract.

## Quick Start Prompt

Use `$self-improve` to autonomously improve this repository in bounded, test-gated iterations and return a final change summary with evidence.
