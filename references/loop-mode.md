# Loop Mode

Use `scripts/run_loop.py` for long-running unattended batches.

## Start

Example (PowerShell):

`python scripts/run_loop.py --cwd . --command 'python ..\.system\skill-creator\scripts\quick_validate.py .' --batch-size 100 --max-batches 0 --print-progress`

Notes:

- `--max-batches 0` means unlimited batches.
- The loop stops on stop-file, signal, max batch limit, or max consecutive failures.
- `--command-timeout-seconds <N>` sets a hard timeout per iteration command. `0` disables it.

Self-iteration mode (bug-hunt + self-heal each round):

`python scripts/run_loop.py --cwd . --command 'python scripts/self_iterate_once.py' --batch-size 100 --max-batches 0 --print-progress`

Stable preset (prepared only, does not start):

`powershell -ExecutionPolicy Bypass -File .\scripts\stable_loop_profile.ps1`

Stable preset without iteration timeout (prepared only, does not start):

`powershell -ExecutionPolicy Bypass -File .\scripts\stable_loop_profile.ps1 -NoTimeout`

Stable preset (start explicitly):

`powershell -ExecutionPolicy Bypass -File .\scripts\stable_loop_profile.ps1 -Start`

If the loop runs in background, watch logs in real time:

`Get-Content .self-improve-loop.log -Wait -Tail 30`

For the stable preset (`stable_loop_profile.ps1`), use:

`Get-Content .self-improve-loop.stable.log -Wait -Tail 30`

## Stop

Create the stop file in the loop working directory:

`New-Item -ItemType File .self-improve.stop -Force`

Remove it before restarting:

`Remove-Item .self-improve.stop -Force`

## State and Logs

- State file: `.self-improve-loop-state.json`
- Log file: `.self-improve-loop.log`
- State includes `timed_out` and `last_error` on iteration updates.
- Final state includes `last_return_code`, `last_timed_out`, and `last_error` for quick post-stop diagnosis.

Both paths can be overridden with `--state-file` and `--log-file`.
