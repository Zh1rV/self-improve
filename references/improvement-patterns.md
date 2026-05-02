# Improvement Patterns

Use this catalog when no obvious safe target appears.
Pick the smallest pattern that can be validated with existing project commands.

## Pattern 001

- Target: Failing unit test with stable local reproduction.
- Change: Isolate root cause and apply the smallest functional fix.
- Validation: Run the failing test directly, then run the closest related suite.


## Pattern 002

- Target: Intermittent failure around null input in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for null input.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 003

- Target: Intermittent failure around empty collection in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for empty collection.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 004

- Target: Intermittent failure around large payload in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for large payload.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 005

- Target: Intermittent failure around unicode text in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for unicode text.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 006

- Target: Intermittent failure around timeout path in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for timeout path.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 007

- Target: Intermittent failure around permission denied path in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for permission denied path.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 008

- Target: Intermittent failure around not found path in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for not found path.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 009

- Target: Intermittent failure around invalid format in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for invalid format.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 010

- Target: Intermittent failure around boundary value in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for boundary value.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 011

- Target: Intermittent failure around concurrency path in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for concurrency path.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 012

- Target: Intermittent failure around retry exhaustion in focused unit tests.
- Change: Replace brittle assertions with deterministic setup and explicit expectations for retry exhaustion.
- Validation: Run the focused unit test repeatedly, then run the nearest module test suite.

## Pattern 013

- Target: Flaky async behavior around null input in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for null input.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 014

- Target: Flaky async behavior around empty collection in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for empty collection.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 015

- Target: Flaky async behavior around large payload in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for large payload.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 016

- Target: Flaky async behavior around unicode text in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for unicode text.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 017

- Target: Flaky async behavior around timeout path in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for timeout path.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 018

- Target: Flaky async behavior around permission denied path in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for permission denied path.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 019

- Target: Flaky async behavior around not found path in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for not found path.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 020

- Target: Flaky async behavior around invalid format in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for invalid format.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 021

- Target: Flaky async behavior around boundary value in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for boundary value.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 022

- Target: Flaky async behavior around concurrency path in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for concurrency path.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 023

- Target: Flaky async behavior around retry exhaustion in integration-adjacent tests.
- Change: Remove race-prone timing assumptions and wait on observable completion signals for retry exhaustion.
- Validation: Run the flaky test several times, then run its parent integration subset.

## Pattern 024

- Target: Missing regression coverage for null input in active business logic.
- Change: Add a narrow regression test for null input before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 025

- Target: Missing regression coverage for empty collection in active business logic.
- Change: Add a narrow regression test for empty collection before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 026

- Target: Missing regression coverage for large payload in active business logic.
- Change: Add a narrow regression test for large payload before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 027

- Target: Missing regression coverage for unicode text in active business logic.
- Change: Add a narrow regression test for unicode text before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 028

- Target: Missing regression coverage for timeout path in active business logic.
- Change: Add a narrow regression test for timeout path before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 029

- Target: Missing regression coverage for permission denied path in active business logic.
- Change: Add a narrow regression test for permission denied path before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 030

- Target: Missing regression coverage for not found path in active business logic.
- Change: Add a narrow regression test for not found path before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 031

- Target: Missing regression coverage for invalid format in active business logic.
- Change: Add a narrow regression test for invalid format before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 032

- Target: Missing regression coverage for boundary value in active business logic.
- Change: Add a narrow regression test for boundary value before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 033

- Target: Missing regression coverage for concurrency path in active business logic.
- Change: Add a narrow regression test for concurrency path before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 034

- Target: Missing regression coverage for retry exhaustion in active business logic.
- Change: Add a narrow regression test for retry exhaustion before applying the minimal code fix.
- Validation: Run the new regression test, then run related tests in the touched component.

## Pattern 035

- Target: Type or lint drift triggered by null input paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing null input diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 036

- Target: Type or lint drift triggered by empty collection paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing empty collection diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 037

- Target: Type or lint drift triggered by large payload paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing large payload diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 038

- Target: Type or lint drift triggered by unicode text paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing unicode text diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 039

- Target: Type or lint drift triggered by timeout paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing timeout path diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 040

- Target: Type or lint drift triggered by permission denied paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing permission denied path diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 041

- Target: Type or lint drift triggered by not found paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing not found path diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 042

- Target: Type or lint drift triggered by invalid format paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing invalid format diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 043

- Target: Type or lint drift triggered by boundary value paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing boundary value diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 044

- Target: Type or lint drift triggered by concurrency paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing concurrency path diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 045

- Target: Type or lint drift triggered by retry exhaustion paths in recently changed files.
- Change: Apply local type/lint-safe refactors that preserve behavior while fixing retry exhaustion diagnostics.
- Validation: Run targeted lint and type checks for changed files, then run project-level checks if cheap.

## Pattern 046

- Target: Input validation gap for null input at external or API boundaries.
- Change: Add explicit guards for null input and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 047

- Target: Input validation gap for empty collection at external or API boundaries.
- Change: Add explicit guards for empty collection and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 048

- Target: Input validation gap for large payload at external or API boundaries.
- Change: Add explicit guards for large payload and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 049

- Target: Input validation gap for unicode text at external or API boundaries.
- Change: Add explicit guards for unicode text and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 050

- Target: Input validation gap for timeout path at external or API boundaries.
- Change: Add explicit guards for timeout path and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 051

- Target: Input validation gap for permission denied path at external or API boundaries.
- Change: Add explicit guards for permission denied path and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 052

- Target: Input validation gap for not found path at external or API boundaries.
- Change: Add explicit guards for not found path and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 053

- Target: Input validation gap for invalid format at external or API boundaries.
- Change: Add explicit guards for invalid format and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 054

- Target: Input validation gap for boundary value at external or API boundaries.
- Change: Add explicit guards for boundary value and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 055

- Target: Input validation gap for concurrency path at external or API boundaries.
- Change: Add explicit guards for concurrency path and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 056

- Target: Input validation gap for retry exhaustion at external or API boundaries.
- Change: Add explicit guards for retry exhaustion and return stable errors without widening side effects.
- Validation: Run boundary-focused unit tests for input handling, then run route or handler tests.

## Pattern 057

- Target: Error handling blind spot for null input in a shared execution path.
- Change: Capture and handle null input explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 058

- Target: Error handling blind spot for empty collection in a shared execution path.
- Change: Capture and handle empty collection explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 059

- Target: Error handling blind spot for large payload in a shared execution path.
- Change: Capture and handle large payload explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 060

- Target: Error handling blind spot for unicode text in a shared execution path.
- Change: Capture and handle unicode text explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 061

- Target: Error handling blind spot for timeout path in a shared execution path.
- Change: Capture and handle timeout path explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 062

- Target: Error handling blind spot for permission denied path in a shared execution path.
- Change: Capture and handle permission denied path explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 063

- Target: Error handling blind spot for not found path in a shared execution path.
- Change: Capture and handle not found path explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 064

- Target: Error handling blind spot for invalid format in a shared execution path.
- Change: Capture and handle invalid format explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 065

- Target: Error handling blind spot for boundary value in a shared execution path.
- Change: Capture and handle boundary value explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 066

- Target: Error handling blind spot for concurrency path in a shared execution path.
- Change: Capture and handle concurrency path explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 067

- Target: Error handling blind spot for retry exhaustion in a shared execution path.
- Change: Capture and handle retry exhaustion explicitly with clear control flow and consistent error mapping.
- Validation: Run failing-path tests for error mapping, then execute nearby success-path tests.

## Pattern 068

- Target: Duplicate logic around null input across nearby modules.
- Change: Extract a tiny shared helper for null input while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 069

- Target: Duplicate logic around empty collection across nearby modules.
- Change: Extract a tiny shared helper for empty collection while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 070

- Target: Duplicate logic around large payload across nearby modules.
- Change: Extract a tiny shared helper for large payload while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 071

- Target: Duplicate logic around unicode text across nearby modules.
- Change: Extract a tiny shared helper for unicode text while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 072

- Target: Duplicate logic around timeout path across nearby modules.
- Change: Extract a tiny shared helper for timeout path while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 073

- Target: Duplicate logic around permission denied path across nearby modules.
- Change: Extract a tiny shared helper for permission denied path while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 074

- Target: Duplicate logic around not found path across nearby modules.
- Change: Extract a tiny shared helper for not found path while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 075

- Target: Duplicate logic around invalid format across nearby modules.
- Change: Extract a tiny shared helper for invalid format while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 076

- Target: Duplicate logic around boundary value across nearby modules.
- Change: Extract a tiny shared helper for boundary value while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 077

- Target: Duplicate logic around concurrency path across nearby modules.
- Change: Extract a tiny shared helper for concurrency path while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 078

- Target: Duplicate logic around retry exhaustion across nearby modules.
- Change: Extract a tiny shared helper for retry exhaustion while keeping call sites behavior-identical.
- Validation: Run tests for each touched caller and any helper-focused unit tests.

## Pattern 079

- Target: Small performance hotspot caused by repeated work on null input.
- Change: Cache or reuse invariant computation for null input without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 080

- Target: Small performance hotspot caused by repeated work on empty collection.
- Change: Cache or reuse invariant computation for empty collection without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 081

- Target: Small performance hotspot caused by repeated work on large payload.
- Change: Cache or reuse invariant computation for large payload without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 082

- Target: Small performance hotspot caused by repeated work on unicode text.
- Change: Cache or reuse invariant computation for unicode text without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 083

- Target: Small performance hotspot caused by repeated work on timeout path.
- Change: Cache or reuse invariant computation for timeout path without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 084

- Target: Small performance hotspot caused by repeated work on permission denied path.
- Change: Cache or reuse invariant computation for permission denied path without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 085

- Target: Small performance hotspot caused by repeated work on not found path.
- Change: Cache or reuse invariant computation for not found path without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 086

- Target: Small performance hotspot caused by repeated work on invalid format.
- Change: Cache or reuse invariant computation for invalid format without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 087

- Target: Small performance hotspot caused by repeated work on boundary value.
- Change: Cache or reuse invariant computation for boundary value without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 088

- Target: Small performance hotspot caused by repeated work on concurrency path.
- Change: Cache or reuse invariant computation for concurrency path without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 089

- Target: Small performance hotspot caused by repeated work on retry exhaustion.
- Change: Cache or reuse invariant computation for retry exhaustion without changing public behavior.
- Validation: Run existing performance-affected tests and compare a quick before/after timing sample.

## Pattern 090

- Target: Documentation or config mismatch around null input in active workflows.
- Change: Align docs/config for null input with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 091

- Target: Documentation or config mismatch around empty collection in active workflows.
- Change: Align docs/config for empty collection with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 092

- Target: Documentation or config mismatch around large payload in active workflows.
- Change: Align docs/config for large payload with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 093

- Target: Documentation or config mismatch around unicode text in active workflows.
- Change: Align docs/config for unicode text with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 094

- Target: Documentation or config mismatch around timeout path in active workflows.
- Change: Align docs/config for timeout path with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 095

- Target: Documentation or config mismatch around permission denied path in active workflows.
- Change: Align docs/config for permission denied path with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 096

- Target: Documentation or config mismatch around not found path in active workflows.
- Change: Align docs/config for not found path with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 097

- Target: Documentation or config mismatch around invalid format in active workflows.
- Change: Align docs/config for invalid format with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 098

- Target: Documentation or config mismatch around boundary value in active workflows.
- Change: Align docs/config for boundary value with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 099

- Target: Documentation or config mismatch around concurrency path in active workflows.
- Change: Align docs/config for concurrency path with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.

## Pattern 100

- Target: Documentation or config mismatch around retry exhaustion in active workflows.
- Change: Align docs/config for retry exhaustion with observed behavior and remove stale contradictory instructions.
- Validation: Run docs or config validation commands when available, then smoke-check referenced commands.
