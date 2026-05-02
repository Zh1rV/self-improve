# Risk Profiles

Use these profiles to tune unattended behavior.

## Conservative

- Max iterations: `3`
- Patch size: smallest possible
- Validation: run broader gates more often
- Skip performance refactors unless strong evidence exists

## Balanced

- Max iterations: `5`
- Patch size: small and bounded
- Validation: narrow-first, broad on medium/high risk
- Include maintainability fixes with clear validation

## Aggressive

- Max iterations: `8`
- Patch size: still bounded but can include medium-size fixes
- Validation: narrow-first with selective broad runs
- Allow more exploratory improvements with fallback rollback
