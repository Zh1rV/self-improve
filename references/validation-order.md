# Validation Order Matrix

Pick validation depth by change risk and blast radius.

## Low Risk, Small Blast Radius

- Run narrow tests/lint/type checks for touched modules.
- Expand only if failures suggest broader impact.

## Medium Risk or Shared Utilities

- Run narrow checks first.
- Run full lint and type checks.
- Run broader test suite for dependent modules.

## High Risk (Allowed Only with Explicit Scope)

- Run narrow checks first.
- Run full lint, full type checks, and broad regression tests.
- Include targeted integration checks when available.
