#!/usr/bin/env python3
"""Generate a markdown checkpoint skeleton for one iteration."""

from __future__ import annotations

import argparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_STOP_REASONS = SKILL_ROOT / "references" / "stop-reasons.md"


def sanitize(value: str) -> str:
    return value.replace("\r", " ").replace("\n", " ").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iteration", type=int, required=True, help="Iteration number")
    parser.add_argument(
        "--objective",
        default="",
        help="Optional short objective text to pre-fill",
    )
    parser.add_argument(
        "--stop-reason",
        default="",
        help="Optional stop reason code to pre-fill",
    )
    return parser.parse_args()


def load_stop_reason_codes(ref_path: Path) -> set[str]:
    codes: set[str] = set()
    for line in ref_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- `") and "`:" in stripped:
            code = stripped.split("`", 2)[1].strip().upper()
            if code:
                codes.add(code)
    return codes


def main() -> int:
    args = parse_args()
    if args.iteration <= 0:
        raise SystemExit("iteration must be > 0")

    objective = sanitize(args.objective)
    stop_reason = sanitize(args.stop_reason)
    if stop_reason:
        try:
            valid_codes = load_stop_reason_codes(DEFAULT_STOP_REASONS)
        except OSError as exc:
            raise SystemExit(f"failed to read stop reasons reference: {exc}")
        if stop_reason.upper() not in valid_codes:
            raise SystemExit(f"unknown stop reason: {stop_reason}")

    print(f"## Iteration {args.iteration}")
    print("")
    print(f"- Objective: {objective}".rstrip())
    print("- Files changed:")
    print("- Validation commands:")
    print("- Validation outcomes:")
    print("- Residual risk:")
    if stop_reason:
        print(f"- Stop reason: {stop_reason}")
    print("- Next action:")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
