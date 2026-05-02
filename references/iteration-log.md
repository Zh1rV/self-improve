# Iteration Log Schema

Keep one line per iteration in this pipe-delimited form:

`iteration|target|score|commands|result|risk|note`

Example:

`7|fix flaky auth test|11|pytest tests/auth -q|pass|low|stabilized fixture teardown`

Use concise values so the log can be scanned quickly.

Field expectations:

- `score` should be an integer value.
- `risk` should be one of `low`, `medium`, or `high`.

Optional helper:

- Use `scripts/append_iteration_log.py` to append a sanitized row.
