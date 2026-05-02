# Candidate Types

Prioritize these unattended-safe improvement types:

- Failing tests with clear root cause.
- Missing tests for recently changed critical logic.
- Lint and type errors in active modules.
- Small performance fixes backed by before/after measurements.
- Repeated code paths that can be simplified without behavior change.

Deprioritize:

- Broad renames across many modules without strong tests.
- Large dependency upgrades during the same iteration batch.
- Multi-service protocol or contract changes.
