# Branch Policy

Use a predictable branch strategy during unattended batches.

- Prefer a dedicated branch per autonomous run.
- Keep branch names stable and machine-friendly (for example: `codex/self-improve-YYYYMMDD-HHMM`).
- Avoid mixing unrelated objectives in one branch.
- Rebase or merge only after validations pass.
- Keep checkpoint summaries aligned with branch state.
