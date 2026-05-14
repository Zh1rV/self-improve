#!/usr/bin/env python3
"""Run iterative command batches with stop-file control and failure guardrails."""

from __future__ import annotations

import argparse
import json
import math
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


STOP_REQUESTED = False


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def on_signal(_signum: int, _frame: object) -> None:
    global STOP_REQUESTED
    STOP_REQUESTED = True


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be > 0")
    return parsed


def non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")
    return parsed


def non_negative_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise argparse.ArgumentTypeError("value must be finite")
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--command",
        required=True,
        help="Command executed once per iteration.",
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="Working directory for command execution.",
    )
    parser.add_argument(
        "--batch-size",
        type=positive_int,
        default=5,
        help="Iterations per batch (default: 5).",
    )
    parser.add_argument(
        "--max-batches",
        type=non_negative_int,
        default=0,
        help="Maximum batches. 0 means unlimited.",
    )
    parser.add_argument(
        "--max-consecutive-failures",
        type=positive_int,
        default=2,
        help="Stop after this many consecutive failures.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=non_negative_float,
        default=0.0,
        help="Sleep duration after each iteration.",
    )
    parser.add_argument(
        "--retry-delay-seconds",
        type=non_negative_float,
        default=2.0,
        help="Extra delay before next iteration after failure.",
    )
    parser.add_argument(
        "--command-timeout-seconds",
        type=non_negative_float,
        default=0.0,
        help="Per-iteration timeout for --command. 0 disables timeout.",
    )
    parser.add_argument(
        "--stop-file",
        default=".self-improve.stop",
        help="Presence of this file stops the loop cleanly.",
    )
    parser.add_argument(
        "--state-file",
        default=".self-improve-loop-state.json",
        help="State output path written after each iteration.",
    )
    parser.add_argument(
        "--log-file",
        default=".self-improve-loop.log",
        help="Append-only execution log path.",
    )
    parser.add_argument(
        "--print-progress",
        action="store_true",
        help="Print loop progress lines to stdout in real time.",
    )
    return parser.parse_args()


def resolve_path(cwd: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    return path if path.is_absolute() else (cwd / path)


def append_log(log_path: Path, message: str) -> None:
    if log_path.exists() and log_path.is_dir():
        raise SystemExit(f"--log-file must be a file path, got directory: {log_path}")
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8", newline="") as f:
            f.write(f"{utc_now()} {message}\n")
    except OSError as exc:
        raise SystemExit(f"failed to write log file: {exc}") from exc


def write_state(state_path: Path, payload: dict[str, object]) -> None:
    if state_path.exists() and state_path.is_dir():
        raise SystemExit(
            f"--state-file must be a file path, got directory: {state_path}"
        )
    try:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"failed to write state file: {exc}") from exc


def emit_progress(enabled: bool, message: str) -> None:
    if enabled:
        print(message, flush=True)


def last_non_empty_line(text: str) -> str:
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def to_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def main() -> int:
    args = parse_args()
    args.command = args.command.strip()
    if not args.command:
        raise SystemExit("--command must not be empty")
    cwd = Path(args.cwd).resolve()
    if not cwd.exists() or not cwd.is_dir():
        raise SystemExit(f"invalid --cwd directory: {cwd}")
    command_timeout = (
        args.command_timeout_seconds if args.command_timeout_seconds > 0 else None
    )

    stop_file = resolve_path(cwd, args.stop_file)
    state_file = resolve_path(cwd, args.state_file)
    log_file = resolve_path(cwd, args.log_file)
    if stop_file.exists() and stop_file.is_dir():
        raise SystemExit(f"--stop-file must be a file path, got directory: {stop_file}")
    initial_stop_file_present = stop_file.exists()

    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)

    total_iterations = 0
    batch_number = 1
    last_started_batch = 0
    consecutive_failures = 0
    stop_reason = ""
    internal_error = ""
    last_return_code: int | None = None
    last_timed_out = False
    last_run_error = ""
    last_stderr_line = ""
    last_stdout_line = ""

    append_log(log_file, f"loop_start command={args.command!r} cwd={str(cwd)!r}")
    emit_progress(
        args.print_progress,
        f"{utc_now()} loop_start cwd={cwd} command={args.command}",
    )
    write_state(
        state_file,
        {
            "updated_at": utc_now(),
            "cwd": str(cwd),
            "command": args.command,
            "batch": 0,
            "iteration_in_batch": 0,
            "total_iterations": 0,
            "status": "running",
            "return_code": None,
            "consecutive_failures": 0,
            "stop_reason": "",
            "timed_out": False,
            "last_error": "",
        },
    )

    try:
        while True:
            if STOP_REQUESTED:
                stop_reason = "signal_received"
                break
            if stop_file.exists():
                stop_reason = (
                    "initial_stop_file_present"
                    if initial_stop_file_present and total_iterations == 0
                    else "stop_file_present"
                )
                break
            if args.max_batches > 0 and batch_number > args.max_batches:
                stop_reason = "max_batches_reached"
                break

            append_log(log_file, f"batch_start batch={batch_number}")
            emit_progress(
                args.print_progress, f"{utc_now()} batch_start batch={batch_number}"
            )
            last_started_batch = batch_number
            for iter_in_batch in range(1, args.batch_size + 1):
                if STOP_REQUESTED:
                    stop_reason = "signal_received"
                    break
                if stop_file.exists():
                    stop_reason = "stop_file_present"
                    break

                total_iterations += 1
                started = time.perf_counter()
                run_error = ""
                timed_out = False
                return_code = 0
                stdout = ""
                stderr = ""
                try:
                    proc = subprocess.run(
                        args.command,
                        cwd=str(cwd),
                        shell=True,
                        capture_output=True,
                        text=True,
                        errors="replace",
                        timeout=command_timeout,
                    )
                    return_code = proc.returncode
                    stdout = (proc.stdout or "").strip()
                    stderr = (proc.stderr or "").strip()
                except subprocess.TimeoutExpired as exc:
                    timed_out = True
                    return_code = 124
                    stdout = to_text(exc.stdout).strip()
                    stderr = to_text(exc.stderr).strip()
                    run_error = f"timeout_after={args.command_timeout_seconds}s"
                except OSError as exc:
                    return_code = 127
                    run_error = f"launch_error={exc}"
                elapsed = round(time.perf_counter() - started, 3)

                stdout_line = last_non_empty_line(stdout)
                stderr_line = last_non_empty_line(stderr)
                if run_error and not stderr_line:
                    stderr_line = run_error

                if return_code == 0:
                    status = "pass"
                    consecutive_failures = 0
                else:
                    status = "fail"
                    consecutive_failures += 1
                last_return_code = return_code
                last_timed_out = timed_out
                last_run_error = run_error
                last_stderr_line = stderr_line
                last_stdout_line = stdout_line

                append_log(
                    log_file,
                    (
                        f"iter={total_iterations} batch={batch_number} in_batch={iter_in_batch} "
                        f"status={status} code={return_code} elapsed={elapsed}s "
                        f"stdout={stdout_line!r} stderr={stderr_line!r}"
                    ),
                )
                emit_progress(
                    args.print_progress,
                    (
                        f"{utc_now()} iter={total_iterations} batch={batch_number} "
                        f"in_batch={iter_in_batch} status={status} code={return_code} "
                        f"elapsed={elapsed}s"
                    ),
                )

                state_payload = {
                    "updated_at": utc_now(),
                    "cwd": str(cwd),
                    "command": args.command,
                    "batch": batch_number,
                    "iteration_in_batch": iter_in_batch,
                    "total_iterations": total_iterations,
                    "status": status,
                    "return_code": return_code,
                    "consecutive_failures": consecutive_failures,
                    "stop_reason": "",
                    "timed_out": timed_out,
                    "last_error": run_error,
                }
                write_state(state_file, state_payload)

                if (
                    return_code != 0
                    and consecutive_failures >= args.max_consecutive_failures
                ):
                    if timed_out:
                        stop_reason = "command_timeout"
                    else:
                        stop_reason = "max_consecutive_failures_reached"
                    break

                has_follow_up_iteration = (
                    not STOP_REQUESTED
                    and not stop_file.exists()
                    and (
                        iter_in_batch < args.batch_size
                        or args.max_batches == 0
                        or batch_number < args.max_batches
                    )
                )

                if args.sleep_seconds > 0:
                    time.sleep(args.sleep_seconds)
                if (
                    return_code != 0
                    and args.retry_delay_seconds > 0
                    and has_follow_up_iteration
                ):
                    time.sleep(args.retry_delay_seconds)

            append_log(log_file, f"batch_end batch={batch_number}")
            emit_progress(
                args.print_progress, f"{utc_now()} batch_end batch={batch_number}"
            )
            if stop_reason:
                break
            batch_number += 1
    except Exception as exc:  # pragma: no cover - defensive guard
        stop_reason = stop_reason or "internal_error"
        internal_error = f"{type(exc).__name__}: {exc}"
        try:
            append_log(log_file, f"loop_internal_error detail={internal_error!r}")
        except SystemExit:
            pass
        emit_progress(args.print_progress, f"{utc_now()} internal_error {internal_error}")

    final_stop_reason = stop_reason or "completed"
    final_state = {
        "updated_at": utc_now(),
        "cwd": str(cwd),
        "command": args.command,
        "batch": last_started_batch,
        "total_iterations": total_iterations,
        "consecutive_failures": consecutive_failures,
        "stop_reason": final_stop_reason,
        "status": "stopped",
        "last_return_code": last_return_code,
        "last_timed_out": last_timed_out,
        "last_error": last_run_error,
        "last_stdout": last_stdout_line,
        "last_stderr": last_stderr_line,
    }
    if internal_error:
        final_state["last_error"] = internal_error
    write_state(state_file, final_state)
    append_log(log_file, f"loop_stop reason={final_state['stop_reason']}")
    emit_progress(
        args.print_progress,
        f"{utc_now()} loop_stop reason={final_state['stop_reason']} total_iterations={total_iterations}",
    )

    print(f"stop_reason={final_state['stop_reason']}")
    print(f"total_iterations={total_iterations}")
    print(f"state_file={state_file}")
    print(f"log_file={log_file}")
    if final_state["stop_reason"] in {
        "command_timeout",
        "initial_stop_file_present",
        "max_consecutive_failures_reached",
        "internal_error",
    }:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
