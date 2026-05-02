# Improvement Rubric

Use this rubric to choose the next autonomous iteration target.

## Candidate Priority

1. Reproducible bugs with user-facing impact.
2. Missing or flaky tests around critical paths.
3. Type, lint, or build errors that block delivery.
4. Performance issues with measurable hotspots.
5. Maintainability problems that slow future changes.

## Scoring

Score each candidate with:

`score = (impact * confidence) - effort - risk`

- `impact`: `1-5` (benefit size)
- `confidence`: `1-5` (certainty about root cause and fix)
- `effort`: `1-5` (implementation + validation cost)
- `risk`: `1-5` (regression or side-effect chance)

Prefer the highest score with `confidence >= 3` and `risk <= 2`.

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
