# Improvement Rubric

Use this rubric to choose the next autonomous iteration target.

For unattended-safe target classes, see `candidate-types.md`.

## Candidate Priority

1. Reproducible bugs with user-facing impact.
2. Missing or flaky tests around critical paths.
3. Type, lint, or build errors that block delivery.
4. Performance issues with measurable hotspots.
5. Maintainability problems that slow future changes.

## Candidate Discovery Checklist

- Review recent failures: test logs, lint output, type errors, build errors.
- Review high-churn files for repeated edits and regressions.
- Review TODO/FIXME markers in critical paths only.
- Prefer issues with a direct, automatable validation command.

## Scoring

Score each candidate with:

`score = (impact * confidence) - effort - risk`

Optional helper:

- Run `python scripts/score_candidates.py --impact <1-5> --confidence <1-5> --effort <1-5> --risk <1-5>` for deterministic scoring.
- Run `python scripts/rank_candidates.py --in <candidates.csv> --top <N>` to rank multiple candidates.

- `impact`: `1-5` (benefit size)
- `confidence`: `1-5` (certainty about root cause and fix)
- `effort`: `1-5` (implementation + validation cost)
- `risk`: `1-5` (regression or side-effect chance)

Prefer the highest score with `confidence >= 3` and `risk <= 2`.

Tie-breakers when scores are equal:

1. Pick the candidate with better validation coverage.
2. Pick the candidate with smaller blast radius.
3. Pick the candidate with lower estimated effort.

## Validation Minimum

- Bug fix: reproduce failure, then prove fix with a test or exact repro command.
- Refactor: run tests covering affected behavior and check for no behavior drift.
- Performance: capture before/after measurement on the same scenario.
- Cleanup: keep lint/type/test status clean in touched areas.

## Stop Conditions

Stop the autonomous loop when any condition is true:

- No remaining candidate meets confidence and risk thresholds.
- Two consecutive attempts fail on the same target.
- Iteration or time budget is exhausted.

## Exclusions

Skip a candidate in unattended mode when it requires:

- Production data mutation or live external side effects.
- Secret rotation or credential changes.
- Broad architecture rewrites without reliable regression coverage.
