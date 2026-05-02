#!/usr/bin/env python3
"""Score one improvement candidate using the self-improve rubric."""

from __future__ import annotations

import argparse


def bounded(value: int, name: str) -> int:
    if value < 1 or value > 5:
        raise ValueError(f"{name} must be in [1, 5], got {value}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--impact", type=int, required=True, help="Impact score (1-5)")
    parser.add_argument(
        "--confidence", type=int, required=True, help="Confidence score (1-5)"
    )
    parser.add_argument("--effort", type=int, required=True, help="Effort score (1-5)")
    parser.add_argument("--risk", type=int, required=True, help="Risk score (1-5)")
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print one-line eligibility explanation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        impact = bounded(args.impact, "impact")
        confidence = bounded(args.confidence, "confidence")
        effort = bounded(args.effort, "effort")
        risk = bounded(args.risk, "risk")
    except ValueError as exc:
        raise SystemExit(str(exc))

    score = (impact * confidence) - effort - risk
    is_eligible = confidence >= 3 and risk <= 2

    print(f"score={score}")
    print(f"eligible={str(is_eligible).lower()}")
    if args.explain:
        if is_eligible:
            reason = "meets confidence>=3 and risk<=2"
        else:
            failures: list[str] = []
            if confidence < 3:
                failures.append("confidence<3")
            if risk > 2:
                failures.append("risk>2")
            reason = f"fails {' and '.join(failures)}"
        print(f"reason={reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
