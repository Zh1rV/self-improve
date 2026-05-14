#!/usr/bin/env python3
"""Run one model-driven self-improvement iteration for the self-improve skill."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SKILLS_ROOT = SKILL_ROOT.parent
QUICK_VALIDATE = (
    SKILLS_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
)
SELF_TEST = SCRIPT_DIR / "self_test.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("timeout-seconds must be > 0")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-bin",
        default=str(Path(tempfile.gettempdir()) / "codex-copy.exe"),
        help="Path to executable Codex CLI binary copy.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=positive_int,
        default=600,
        help="Timeout for one model iteration.",
    )
    parser.add_argument(
        "--no-timeout",
        action="store_true",
        help="Disable model iteration timeout (run until completion).",
    )
    parser.add_argument(
        "--model",
        default="",
        help="Optional model override, e.g. gpt-5.4.",
    )
    return parser.parse_args()


def discover_windowsapps_codex() -> list[Path]:
    candidates: list[Path] = []
    try:
        proc = subprocess.run(
            ["where.exe", "codex.exe"],
            capture_output=True,
            text=True,
            check=False,
        )
        for raw in proc.stdout.splitlines():
            p = Path(raw.strip())
            if p and p.exists():
                candidates.append(p)
    except OSError:
        pass
    return candidates


def is_executable_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if os.name == "nt":
        pathext = {
            ext.strip().lower()
            for ext in os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").split(";")
            if ext.strip()
        }
        if path.suffix.lower() not in pathext:
            return False
        # Filter out fake ".exe" text files that later fail with WinError 216.
        if path.suffix.lower() == ".exe":
            try:
                with path.open("rb") as f:
                    return f.read(2) == b"MZ"
            except OSError:
                return False
        return True
    return os.access(path, os.X_OK)


def ensure_executable_codex(copy_path: Path) -> Path:
    if copy_path.exists():
        if not copy_path.is_file():
            raise SystemExit(f"--codex-bin must reference a file: {copy_path}")
        if not is_executable_file(copy_path):
            if os.name == "nt":
                raise SystemExit(
                    f"--codex-bin must reference a Windows executable file: {copy_path}"
                )
            raise SystemExit(f"--codex-bin must reference an executable file: {copy_path}")
        return copy_path

    for source in discover_windowsapps_codex():
        try:
            copy_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, copy_path)
            return copy_path
        except OSError:
            continue

    raise SystemExit(
        "failed to prepare codex executable copy; ensure codex is installed and runnable"
    )


def build_prompt() -> str:
    return (
        "Run exactly one self-improvement iteration.\n"
        f"Only modify files under: {SKILL_ROOT}\n"
        "Task:\n"
        "1) Find one real bug in the self-improve skill scripts/docs.\n"
        "2) Apply the smallest safe fix.\n"
        f"3) Run validation: python {QUICK_VALIDATE} {SKILL_ROOT}\n"
        f"4) Run regression checks: python {SELF_TEST}\n"
        "5) If no real bug is found, make no file changes and report no_change.\n"
        "Final response format (plain text, exactly 3 lines):\n"
        "bug: <one sentence>\n"
        "files: <comma separated absolute paths or none>\n"
        "validation: <pass/fail + key output, including self_test result>\n"
    )


def summarize_output(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "empty"
    return lines[0]


def strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if not stripped.startswith("```"):
        return text

    lines = stripped.splitlines()
    if len(lines) < 2:
        return text
    if not lines[0].startswith("```"):
        return text
    if lines[-1].strip() != "```":
        return text
    return "\n".join(lines[1:-1]).strip()


def snapshot_outside_files(root: Path, allowed_root: Path) -> dict[Path, tuple[int, int]]:
    snapshot: dict[Path, tuple[int, int]] = {}
    for path in root.rglob("*"):
        try:
            if not path.is_file():
                continue
            resolved = path.resolve()
            if resolved.is_relative_to(allowed_root):
                continue
            stat = path.stat()
        except OSError:
            continue
        snapshot[resolved] = (stat.st_mtime_ns, stat.st_size)
    return snapshot


def diff_outside_files(
    before: dict[Path, tuple[int, int]],
    after: dict[Path, tuple[int, int]],
) -> list[Path]:
    changed: list[Path] = []
    before_keys = set(before)
    after_keys = set(after)

    for path in sorted(before_keys ^ after_keys):
        changed.append(path)
    for path in sorted(before_keys & after_keys):
        if before[path] != after[path]:
            changed.append(path)
    return changed


def parse_final_fields(message: str) -> tuple[dict[str, str], str]:
    cleaned = strip_code_fence(message)
    lines = [raw.strip() for raw in cleaned.splitlines() if raw.strip()]
    if len(lines) != 3:
        return {}, f"invalid_final_line_count:{len(lines)}"

    fields: dict[str, str] = {}
    for index, key in enumerate(("bug", "files", "validation"), start=1):
        prefix = f"{key}:"
        line = lines[index - 1]
        if not line.lower().startswith(prefix):
            return {}, f"invalid_final_line_{index}"
        value = line[len(prefix) :].strip()
        if not value:
            return {}, f"empty_{key}_field"
        fields[key] = value
    return fields, ""


def validate_reported_files(files_value: str, allowed_root: Path) -> tuple[bool, str]:
    if files_value.lower() == "none":
        return True, ""

    items = [item.strip() for item in files_value.split(",") if item.strip()]
    if not items:
        return False, "files field is empty"

    for item in items:
        normalized_item = item.strip().strip("`")
        candidate = Path(normalized_item)
        if not candidate.is_absolute():
            return False, f"reported file is not absolute: {normalized_item}"
        resolved = candidate.resolve(strict=False)
        if not resolved.is_relative_to(allowed_root):
            return False, f"reported file is outside allowed scope: {resolved}"
    return True, ""


def main() -> int:
    args = parse_args()
    codex_bin = ensure_executable_codex(Path(args.codex_bin))
    last_message = SKILL_ROOT / ".self-improve-model-last.txt"
    allowed_root = SKILL_ROOT.resolve()
    outside_before = snapshot_outside_files(SKILLS_ROOT.resolve(), allowed_root)
    try:
        if last_message.exists():
            last_message.unlink()
    except OSError as exc:
        print(f"result=runner_error error=failed_to_reset_last_message:{exc}")
        return 1

    cmd = [
        str(codex_bin),
        "exec",
        "-C",
        str(SKILL_ROOT),
        "--skip-git-repo-check",
        "--dangerously-bypass-approvals-and-sandbox",
        "--output-last-message",
        str(last_message),
    ]
    if args.model:
        cmd.extend(["--model", args.model])
    cmd.append(build_prompt())

    print(f"timestamp={utc_now()}")
    print(f"runner=model")
    if args.no_timeout:
        print("timeout=disabled")
    else:
        print(f"timeout={args.timeout_seconds}s")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=None if args.no_timeout else args.timeout_seconds,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
    except subprocess.TimeoutExpired:
        print("result=timeout")
        return 1
    except OSError as exc:
        print(f"result=runner_error error={exc}")
        return 1

    if proc.returncode != 0:
        err = summarize_output(proc.stderr or proc.stdout)
        print(f"result=codex_failed code={proc.returncode} detail={err}")
        return proc.returncode

    outside_after = snapshot_outside_files(SKILLS_ROOT.resolve(), allowed_root)
    outside_changed = diff_outside_files(outside_before, outside_after)
    if outside_changed:
        first = outside_changed[0]
        print(
            f"result=runner_error error=outside_scope_change count={len(outside_changed)} first={first}"
        )
        return 1

    if not last_message.exists():
        print("result=runner_error error=missing_last_message")
        return 1
    try:
        message = last_message.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"result=runner_error error=failed_to_read_last_message:{exc}")
        return 1
    if not message.strip():
        print("result=runner_error error=empty_last_message")
        return 1

    fields, parse_err = parse_final_fields(message)
    if parse_err:
        print(f"result=runner_error error={parse_err}")
        return 1

    files_ok, files_err = validate_reported_files(fields["files"], allowed_root)
    if not files_ok:
        print(f"result=runner_error error={files_err}")
        return 1

    validation = fields["validation"].strip().lower()
    if not validation.startswith("pass"):
        print(f"result=iteration_failed detail=validation_not_pass:{fields['validation']}")
        return 1
    if "self_test" not in validation:
        print("result=runner_error error=missing_self_test_validation")
        return 1

    summary = fields["bug"] or summarize_output(message)
    print(f"result=ok summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
