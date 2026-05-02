# Stop Reason Codes

Use one code when ending a batch early or on schedule.

- `S1_NO_SAFE_TARGET`: No candidate meets confidence and risk thresholds.
- `S2_GATE_FAILURE_LIMIT`: Reached retry limit on a target after gate failures.
- `S3_BUDGET_EXHAUSTED`: Iteration count or time budget exhausted.
- `S4_EXTERNAL_BLOCKER`: Required dependency or environment is unavailable.
- `S5_USER_ESCALATION`: Waiting for user decision on risky or ambiguous work.

Optional helper:

- Run `scripts/validate_stop_reason.py --code <CODE>` to validate code usage.
