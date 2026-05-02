#!/usr/bin/env python3
"""Append one iteration record to a pipe-delimited iteration log."""

from __future__ import annotations

import argparse
from pathlib import Path

ALLOWED_RISKS = {"low", "medium", "high"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", required=True, help="Path to iteration log file")
    parser.add_argument("--iteration", type=int, required=True, help="Iteration number")
    parser.add_argument("--target", required=True, help="Short target description")
    parser.add_argument("--score", required=True, help="Score value")
    parser.add_argument("--commands", required=True, help="Validation commands summary")
    parser.add_argument("--result", required=True, help="Result, e.g. pass/fail")
    parser.add_argument("--risk", required=True, help="Risk level, e.g. low/medium/high")
    parser.add_argument("--note", default="", help="Optional short note")
    return parser.parse_args()


def sanitize(value: str) -> str:
    return value.replace("|", "/").replace("\r", " ").replace("\n", " ").strip()


def main() -> int:
    args = parse_args()
    if args.iteration <= 0:
        raise SystemExit("iteration must be > 0")
    try:
        score_value = int(str(args.score).strip())
    except ValueError as exc:
        raise SystemExit("score must be an integer") from exc

    target = sanitize(args.target)
    score = str(score_value)
    commands = sanitize(args.commands)
    result = sanitize(args.result)
    risk = sanitize(args.risk).lower()
    note = sanitize(args.note)

    required_values = {
        "target": target,
        "score": score,
        "commands": commands,
        "result": result,
        "risk": risk,
    }
    for field, value in required_values.items():
        if not value:
            raise SystemExit(f"{field} must not be empty")
    if risk not in ALLOWED_RISKS:
        allowed = ", ".join(sorted(ALLOWED_RISKS))
        raise SystemExit(f"risk must be one of: {allowed}")

    row = "|".join(
        [
            str(args.iteration),
            target,
            score,
            commands,
            result,
            risk,
            note,
        ]
    )

    log_path = Path(args.log)
    if log_path.exists() and log_path.is_dir():
        raise SystemExit(f"log path is a directory, expected a file: {log_path}")
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise SystemExit(f"failed to create parent directory: {exc}")
    needs_newline = False
    try:
        if log_path.exists() and log_path.stat().st_size > 0:
            with log_path.open("rb") as check:
                check.seek(-1, 2)
                last_byte = check.read(1)
            needs_newline = last_byte not in (b"\n", b"\r")

        with log_path.open("a", encoding="utf-8", newline="") as f:
            if needs_newline:
                f.write("\n")
            f.write(row)
    except OSError as exc:
        raise SystemExit(f"failed to write log: {exc}")
    print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
