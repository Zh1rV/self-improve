#!/usr/bin/env python3
"""Run fast regression checks for the self-improve skill."""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILLS_ROOT = SKILL_ROOT.parent
QUICK_VALIDATE = (
    SKILLS_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str = ""


def run_cmd(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        errors="replace",
    )


def first_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def check_quick_validate() -> Check:
    if not QUICK_VALIDATE.exists():
        return Check("quick_validate", False, f"missing {QUICK_VALIDATE}")
    proc = run_cmd([sys.executable, str(QUICK_VALIDATE), str(SKILL_ROOT)])
    detail = first_line(proc.stdout) or first_line(proc.stderr)
    return Check("quick_validate", proc.returncode == 0, detail)


def check_py_compile() -> Check:
    files = list((SKILL_ROOT / "scripts").glob("*.py"))
    files.extend((SKILL_ROOT / "references" / "self-heal-baseline").glob("*.py"))
    try:
        for path in files:
            py_compile.compile(str(path), doraise=True)
    except py_compile.PyCompileError as exc:
        return Check("py_compile", False, str(exc))
    return Check("py_compile", True, f"compiled={len(files)}")


def check_score_candidates() -> Check:
    proc = run_cmd(
        [
            sys.executable,
            str(SCRIPT_DIR / "score_candidates.py"),
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
    combined = f"{proc.stdout}\n{proc.stderr}"
    ok = (
        proc.returncode == 0
        and "eligible=false" in combined
        and "reason=fails confidence<3 and risk>2" in combined
    )
    return Check("score_candidates", ok, first_line(combined))


def check_score_rejects_bad_range() -> Check:
    proc = run_cmd(
        [
            sys.executable,
            str(SCRIPT_DIR / "score_candidates.py"),
            "--impact",
            "6",
            "--confidence",
            "3",
            "--effort",
            "1",
            "--risk",
            "1",
        ]
    )
    combined = f"{proc.stdout}\n{proc.stderr}"
    ok = proc.returncode != 0 and "must be in [1, 5]" in combined
    return Check("score_rejects_bad_range", ok, first_line(combined))


def check_rank_candidates() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        csv_path = Path(td) / "candidates.csv"
        csv_path.write_text(
            "\n name ; impact ; confidence ; effort ; risk \n"
            "later;3;3;2;2\n"
            "first;5;5;1;1\n",
            encoding="utf-8",
        )
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "rank_candidates.py"),
                "--in",
                str(csv_path),
                "--top",
                "1",
            ]
        )
    ok = proc.returncode == 0 and "first|23|true|5|5|1|1" in proc.stdout
    return Check("rank_candidates", ok, first_line(proc.stdout or proc.stderr))


def check_rank_rejects_duplicate_headers() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        csv_path = Path(td) / "candidates.csv"
        csv_path.write_text(
            "name,impact,confidence,effort,risk,risk\nfoo,4,4,2,1,2\n",
            encoding="utf-8",
        )
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "rank_candidates.py"),
                "--in",
                str(csv_path),
            ]
        )
    combined = f"{proc.stdout}\n{proc.stderr}"
    ok = proc.returncode != 0 and "duplicate columns: risk" in combined
    return Check("rank_rejects_duplicate_headers", ok, first_line(combined))


def check_append_iteration_log() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        log_path = Path(td) / "iter.log"
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "append_iteration_log.py"),
                "--log",
                str(log_path),
                "--with-header",
                "--iteration",
                "1",
                "--target",
                "target|name",
                "--score",
                "8",
                "--commands",
                "python test",
                "--result",
                "pass",
                "--risk",
                "LOW",
                "--note",
                "line one\nline two",
            ]
        )
        content = log_path.read_text(encoding="utf-8")
    ok = (
        proc.returncode == 0
        and content.startswith("iteration|target|score|commands|result|risk|note\n")
        and "1|target/name|8|python test|pass|low|line one line two" in content
    )
    return Check("append_iteration_log", ok, first_line(proc.stdout or proc.stderr))


def check_validate_stop_reason() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "validate_stop_reason.py"),
                "--code",
                "`s3_budget_exhausted`",
                "--ref",
                str(Path("references") / "stop-reasons.md"),
            ],
            cwd=Path(td),
        )
    ok = proc.returncode == 0 and "exists=true" in proc.stdout
    return Check("validate_stop_reason", ok, first_line(proc.stdout or proc.stderr))


def check_self_iterate_once_uses_self_test() -> Check:
    text = (SCRIPT_DIR / "self_iterate_once.py").read_text(encoding="utf-8")
    ok = "SELF_TEST_SCRIPT" in text and "run_validation_suite" in text
    return Check("self_iterate_once_uses_self_test", ok)


def check_model_iterate_requires_self_test() -> Check:
    text = (SCRIPT_DIR / "self_iterate_model_once.py").read_text(encoding="utf-8")
    ok = (
        "python {SELF_TEST}" in text
        and "including self_test result" in text
        and "missing_self_test_validation" in text
    )
    return Check("model_iterate_requires_self_test", ok)


def check_skill_documents_self_test() -> Check:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    ok = "python scripts/self_test.py" in text and "Fast Self Test" in text
    return Check("skill_documents_self_test", ok)


def check_checkpoint_report() -> Check:
    proc = run_cmd(
        [
            sys.executable,
            str(SCRIPT_DIR / "checkpoint_report.py"),
            "--iteration",
            "2",
            "--objective",
            "compact\nobjective",
            "--stop-reason",
            "`s1_no_safe_target`",
        ]
    )
    ok = (
        proc.returncode == 0
        and "## Iteration 2" in proc.stdout
        and "- Objective: compact objective" in proc.stdout
        and "- Stop reason: S1_NO_SAFE_TARGET" in proc.stdout
    )
    return Check("checkpoint_report", ok, first_line(proc.stdout or proc.stderr))


def check_run_loop() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        work = Path(td)
        command = f'"{sys.executable}" -c "print(\'ok\')"'
        state_file = work / "state.json"
        log_file = work / "loop.log"
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "run_loop.py"),
                "--cwd",
                str(work),
                "--command",
                command,
                "--batch-size",
                "2",
                "--max-batches",
                "1",
                "--state-file",
                str(state_file),
                "--log-file",
                str(log_file),
            ]
        )
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return Check("run_loop", False, str(exc))
    ok = (
        proc.returncode == 0
        and "stop_reason=max_batches_reached" in proc.stdout
        and state.get("total_iterations") == 2
    )
    return Check("run_loop", ok, first_line(proc.stdout or proc.stderr))


def check_run_loop_timeout_reason() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        work = Path(td)
        command = f'"{sys.executable}" -c "import time; time.sleep(2)"'
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "run_loop.py"),
                "--cwd",
                str(work),
                "--command",
                command,
                "--batch-size",
                "1",
                "--max-batches",
                "1",
                "--max-consecutive-failures",
                "1",
                "--command-timeout-seconds",
                "0.1",
                "--retry-delay-seconds",
                "0",
            ]
        )
    ok = proc.returncode == 1 and "stop_reason=command_timeout" in proc.stdout
    return Check("run_loop_timeout_reason", ok, first_line(proc.stdout or proc.stderr))


def check_run_loop_initial_stop_file() -> Check:
    with tempfile.TemporaryDirectory(prefix="self-improve-test-") as td:
        work = Path(td)
        (work / ".self-improve.stop").write_text("", encoding="utf-8")
        proc = run_cmd(
            [
                sys.executable,
                str(SCRIPT_DIR / "run_loop.py"),
                "--cwd",
                str(work),
                "--command",
                f'"{sys.executable}" -c "print(\'should_not_run\')"',
                "--batch-size",
                "1",
                "--max-batches",
                "1",
            ]
        )
    ok = (
        proc.returncode == 1
        and "stop_reason=initial_stop_file_present" in proc.stdout
        and "total_iterations=0" in proc.stdout
    )
    return Check("run_loop_initial_stop_file", ok, first_line(proc.stdout or proc.stderr))


def main() -> int:
    checks = [
        check_quick_validate(),
        check_py_compile(),
        check_score_candidates(),
        check_score_rejects_bad_range(),
        check_rank_candidates(),
        check_rank_rejects_duplicate_headers(),
        check_append_iteration_log(),
        check_validate_stop_reason(),
        check_self_iterate_once_uses_self_test(),
        check_model_iterate_requires_self_test(),
        check_skill_documents_self_test(),
        check_checkpoint_report(),
        check_run_loop(),
        check_run_loop_timeout_reason(),
        check_run_loop_initial_stop_file(),
    ]

    failed = False
    for check in checks:
        status = "PASS" if check.ok else "FAIL"
        print(f"{check.name}={status} {check.detail}".rstrip())
        failed = failed or not check.ok
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
