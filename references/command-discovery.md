# Command Discovery

Use this process to discover project validation commands safely.

1. Read top-level docs first: `README*`, `CONTRIBUTING*`, `Makefile`, `package.json`, `pyproject.toml`, CI configs.
2. Prefer existing scripts over ad-hoc command construction.
3. Run lightweight inspection commands before execution (`--help`, dry-run, or list modes).
4. Start with the narrowest relevant command and expand only when needed.

If command discovery remains ambiguous after these steps, escalate to the user.
