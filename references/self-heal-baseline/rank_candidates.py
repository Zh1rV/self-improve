#!/usr/bin/env python3
"""Rank improvement candidates from a CSV file using rubric scoring."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any, TextIO


REQUIRED = ("name", "impact", "confidence", "effort", "risk")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input_csv", required=True, help="Input CSV path")
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="If > 0, print only top N candidates",
    )
    return parser.parse_args()


def to_int(raw: str, field: str, row_name: str) -> int:
    if raw is None:
        raise ValueError(f"{row_name}: {field} is required")
    try:
        value = int(raw.strip())
    except ValueError as exc:
        raise ValueError(f"{row_name}: {field} must be an integer") from exc
    if not 1 <= value <= 5:
        raise ValueError(f"{row_name}: {field} must be in [1, 5]")
    return value


def score_row(row: dict[str, str], row_number: int) -> dict[str, Any]:
    raw_name = row.get("name")
    name = (raw_name or "").strip() or "<unnamed>"
    impact = to_int(row["impact"], "impact", name)
    confidence = to_int(row["confidence"], "confidence", name)
    effort = to_int(row["effort"], "effort", name)
    risk = to_int(row["risk"], "risk", name)
    score = (impact * confidence) - effort - risk
    eligible = confidence >= 3 and risk <= 2
    return {
        "name": name,
        "score": score,
        "eligible": eligible,
        "impact": impact,
        "confidence": confidence,
        "effort": effort,
        "risk": risk,
    }


def is_blank_row(row: dict[str, str | None]) -> bool:
    return all((value is None or str(value).strip() == "") for value in row.values())


def detect_dialect(sample: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        return csv.get_dialect("excel")


def normalize_row(row: dict[str, str | None]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in row.items():
        if key is None:
            continue
        normalized_key = key.strip().lower()
        if not normalized_key:
            continue
        normalized[normalized_key] = "" if value is None else value
    return normalized


def seek_first_non_blank_line(handle: TextIO) -> tuple[bool, int]:
    line_number = 0
    while True:
        position = handle.tell()
        line = handle.readline()
        line_number += 1
        if line == "":
            return False, 0
        if line.strip():
            handle.seek(position)
            return True, line_number


def main() -> int:
    args = parse_args()
    if args.top < 0:
        raise SystemExit("--top must be >= 0")
    in_path = Path(args.input_csv)
    if not in_path.exists():
        raise SystemExit(f"input file not found: {in_path}")
    if not in_path.is_file():
        raise SystemExit(f"input path is not a file: {in_path}")

    try:
        with in_path.open("r", encoding="utf-8-sig", newline="") as f:
            found_header, header_line = seek_first_non_blank_line(f)
            if not found_header:
                raise SystemExit(f"missing required columns: {', '.join(REQUIRED)}")
            header_pos = f.tell()
            sample = f.read(4096)
            f.seek(header_pos)
            dialect = detect_dialect(sample)
            reader = csv.DictReader(f, dialect=dialect)

            raw_headers = reader.fieldnames or []
            headers = [h.strip().lower() for h in raw_headers if h is not None]
            missing = [h for h in REQUIRED if h not in headers]
            if missing:
                raise SystemExit(f"missing required columns: {', '.join(missing)}")
            scored: list[dict[str, Any]] = []
            for row_number, row in enumerate(reader, start=header_line + 1):
                normalized_row = normalize_row(row)
                if is_blank_row(normalized_row):
                    continue
                try:
                    scored.append(score_row(normalized_row, row_number))
                except ValueError as exc:
                    raise SystemExit(f"row {row_number}: {exc}")
    except UnicodeDecodeError:
        raise SystemExit(f"failed to decode CSV as utf-8: {in_path}")
    except csv.Error as exc:
        raise SystemExit(f"failed to parse CSV: {exc}")
    except OSError as exc:
        raise SystemExit(f"failed to read input file: {exc}")

    scored.sort(
        key=lambda x: (
            0 if x["eligible"] else 1,
            -x["score"],
            x["risk"],
            x["effort"],
            x["name"].casefold(),
        )
    )
    limit = args.top if args.top > 0 else len(scored)

    print("name|score|eligible|impact|confidence|effort|risk")
    for row in scored[:limit]:
        print(
            f'{row["name"]}|{row["score"]}|{str(row["eligible"]).lower()}|'
            f'{row["impact"]}|{row["confidence"]}|{row["effort"]}|{row["risk"]}'
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
