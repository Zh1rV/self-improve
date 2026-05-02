#!/usr/bin/env python3
"""Validate whether a stop reason code exists in stop-reasons.md."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REF = SKILL_ROOT / "references" / "stop-reasons.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--code", required=True, help="Stop reason code to validate")
    parser.add_argument(
        "--ref",
        default=str(DEFAULT_REF),
        help="Path to stop-reasons markdown file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ref_path = Path(args.ref)
    if not ref_path.is_absolute():
        cwd_candidate = (Path.cwd() / ref_path).resolve()
        if cwd_candidate.exists():
            ref_path = cwd_candidate
        else:
            skill_candidate = (SKILL_ROOT / ref_path).resolve()
            ref_path = skill_candidate
    if not ref_path.exists():
        print("exists=false")
        print(f"error=reference file not found: {ref_path}")
        return 1
    if not ref_path.is_file():
        print("exists=false")
        print(f"error=reference path is not a file: {ref_path}")
        return 1
    try:
        content = ref_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("exists=false")
        print(f"error=failed to decode utf-8 file: {ref_path}")
        return 1
    except OSError as exc:
        print("exists=false")
        print(f"error=failed to read reference file: {exc}")
        return 1

    codes = {
        code.upper()
        for code in re.findall(r"^\s*-\s+`([A-Za-z0-9_]+)`\s*:", content, flags=re.MULTILINE)
    }
    if not codes:
        print("exists=false")
        print(f"error=no stop reason codes found in reference file: {ref_path}")
        return 1
    normalized = args.code.strip().strip("`").upper()

    exists = normalized in codes
    print(f"exists={str(exists).lower()}")
    if not exists:
        print(f"available={','.join(sorted(codes))}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
