#!/usr/bin/env python3
"""Run one autonomous self-heal iteration for the self-improve skill."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PYTHON = Path(__import__("sys").executable)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILLS_ROOT = SKILL_ROOT.parent
BASELINE_DIR = SKILL_ROOT / "references" / "self-heal-baseline"
QUICK_VALIDATE = (
    SKILLS_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
)

SCORE_SCRIPT = SCRIPT_DIR / "score_candidates.py"
RANK_SCRIPT = SCRIPT_DIR / "rank_candidates.py"
APPEND_SCRIPT = SCRIPT_DIR / "append_iteration_log.py"
VALIDATE_STOP_SCRIPT = SCRIPT_DIR / "validate_stop_reason.py"
SELF_TEST_SCRIPT = SCRIPT_DIR / "self_test.py"


@dataclass
class Result:
    code: int
    stdout: str
    stderr: str


@dataclass
class Diagnostic:
    name: str
    ok: bool
    details: str
    file_name: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    return parser.parse_args()


def run_cmd(args: list[str], cwd: Path | None = None) -> Result:
    proc = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    return Result(proc.returncode, proc.stdout.strip(), proc.stderr.strip())


def diag_score_reason() -> Diagnostic:
    res = run_cmd(
        [
            str(PYTHON),
            str(SCORE_SCRIPT),
            "--impact",
            "3",
            "--confidence",
            "2",
            "--effort",
            "1",
            "--risk",
            "4",
            "--explain",
        ]
    )
    combined = f"{res.stdout}\n{res.stderr}"
    ok = (
        res.code == 0
        and "eligible=false" in combined
        and "reason=fails confidence<3 and risk>2" in combined
    )
    return Diagnostic("score_reason", ok, combined.strip(), "score_candidates.py")


def diag_validate_relative_ref() -> Diagnostic:
    with tempfile.TemporaryDirectory(prefix="self-improve-diag-") as td:
        res = run_cmd(
            [
                str(PYTHON),
                str(VALIDATE_STOP_SCRIPT),
                "--code",
                "S1_NO_SAFE_TARGET",
                "--ref",
                str(Path("references") / "stop-reasons.md"),
            ],
            cwd=Path(td),
        )
    combined = f"{res.stdout}\n{res.stderr}"
    ok = res.code == 0 and "exists=true" in combined
    return Diagnostic(
        "validate_relative_ref",
        ok,
        combined.strip(),
        "validate_stop_reason.py",
    )


def diag_rank_csv_variants() -> Diagnostic:
    with tempfile.TemporaryDirectory(prefix="self-improve-diag-") as td:
        csv_path = Path(td) / "candidates.csv"
        csv_path.write_text(
            " name ; impact ; confidence ; effort ; risk \nfoo;4;4;2;2\n",
            encoding="utf-8",
        )
        res = run_cmd([str(PYTHON), str(RANK_SCRIPT), "--in", str(csv_path)])
    combined = f"{res.stdout}\n{res.stderr}"
    ok = res.code == 0 and "foo|12|true|4|4|2|2" in combined
    return Diagnostic("rank_csv_variants", ok, combined.strip(), "rank_candidates.py")


def diag_append_rejects_empty_target() -> Diagnostic:
    with tempfile.TemporaryDirectory(prefix="self-improve-diag-") as td:
        log_path = Path(td) / "iter.log"
        res = run_cmd(
            [
                str(PYTHON),
                str(APPEND_SCRIPT),
                "--log",
                str(log_path),
                "--iteration",
                "1",
                "--target",
                "   ",
                "--score",
                "1",
                "--commands",
                "quick_validate",
                "--result",
                "pass",
                "--risk",
                "low",
                "--note",
                "n",
            ]
        )
    combined = f"{res.stdout}\n{res.stderr}"
    ok = res.code != 0 and "target must not be empty" in combined
    return Diagnostic(
        "append_rejects_empty_target",
        ok,
        combined.strip(),
        "append_iteration_log.py",
    )


def run_quick_validate() -> Result:
    return run_cmd([str(PYTHON), str(QUICK_VALIDATE), str(SKILL_ROOT)])


def run_self_test() -> Result:
    return run_cmd([str(PYTHON), str(SELF_TEST_SCRIPT)], cwd=SKILL_ROOT)


def run_validation_suite() -> Result:
    quick = run_quick_validate()
    if quick.code != 0:
        return quick
    return run_self_test()


def restore_baseline(file_name: str) -> None:
    baseline = BASELINE_DIR / file_name
    target = SCRIPT_DIR / file_name
    if not baseline.exists():
        raise SystemExit(f"missing baseline file: {baseline}")
    shutil.copy2(baseline, target)


def run_diagnostics() -> list[Diagnostic]:
    return [
        diag_score_reason(),
        diag_validate_relative_ref(),
        diag_rank_csv_variants(),
        diag_append_rejects_empty_target(),
    ]


def print_diag(prefix: str, diag: Diagnostic) -> None:
    status = "PASS" if diag.ok else "FAIL"
    print(f"{prefix} {diag.name}={status}")
    if not diag.ok and diag.details:
        short = diag.details.splitlines()[0]
        print(f"{prefix} detail={short}")


def main() -> int:
    parse_args()
    print(f"timestamp={utc_now()}")
    diags = run_diagnostics()
    failed = [d for d in diags if not d.ok]
    for d in diags:
        print_diag("before", d)

    if not failed:
        validate = run_validation_suite()
        if validate.code != 0:
            print("status=validate_failed")
            print(validate.stdout or validate.stderr)
            return 1
        print("action=no_change")
        print("status=pass")
        return 0

    repaired_files = sorted({d.file_name for d in failed})
    for file_name in repaired_files:
        restore_baseline(file_name)
        print(f"action=restored file={file_name}")

    validate = run_validation_suite()
    if validate.code != 0:
        print("status=restore_validate_failed")
        print(validate.stdout or validate.stderr)
        return 1

    post_diags = run_diagnostics()
    post_failed = [d for d in post_diags if not d.ok]
    for d in post_diags:
        print_diag("after", d)

    if post_failed:
        print("status=heal_incomplete")
        return 1

    print("status=healed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
