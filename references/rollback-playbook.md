# Rollback Playbook

Use this when an iteration fails and cannot be fixed within retry limits.

1. Identify files changed in the failed iteration.
2. Revert only failed-iteration changes.
3. Re-run the failed gate command.
4. Confirm repository returns to a known-good state.
5. Record rollback reason and next safer candidate.

Never perform destructive history rewrites unless explicitly requested.
