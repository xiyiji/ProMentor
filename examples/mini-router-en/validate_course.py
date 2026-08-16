#!/usr/bin/env python3
"""Validate the golden mini-router course.

A course is good only if:
  - the .promentor/ files match the published schema
  - empty student stubs fail the chapter tests
  - the reference implementation passes those same tests
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSE_DIR = ROOT / ".promentor"
CHAPTERS_DIR = COURSE_DIR / "chapters"
REFERENCE_ROUTER = ROOT / "mini_router" / "router.py"
REFERENCE_APP = ROOT / "reference" / "app.py"

REQUIRED_CHAPTER_FILES = ("lecture.md", "source.md", "lab.json", "lab_test.py")
DIFFICULTIES = {"easy", "mid", "hard"}
STATUSES = {"not_started", "in_progress", "completed"}


class CheckError(Exception):
    pass


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CheckError(f"missing {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise CheckError(f"invalid JSON {path.relative_to(ROOT)}: {exc}") from exc


def check_schema() -> list[str]:
    course = load_json(COURSE_DIR / "course.json")
    progress = load_json(COURSE_DIR / "progress.json")
    errors: list[str] = []

    if course.get("language") != "python":
        errors.append("course.json.language must be python")
    chapters = course.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        raise CheckError("course.json.chapters must be a non-empty list")

    progress_chapters = progress.get("chapters")
    if not isinstance(progress_chapters, dict):
        raise CheckError("progress.json.chapters must be an object")

    ids: list[str] = []
    for index, meta in enumerate(chapters):
        chapter_id = meta.get("id", "")
        ids.append(chapter_id)
        if not isinstance(chapter_id, str) or not chapter_id.startswith("ch"):
            errors.append(f"chapters[{index}].id is not chNN-slug: {chapter_id!r}")
            continue
        if meta.get("difficulty") not in DIFFICULTIES:
            errors.append(f"{chapter_id}.difficulty must be easy|mid|hard")
        chapter_dir = CHAPTERS_DIR / chapter_id
        if not chapter_dir.is_dir():
            errors.append(f"missing directory chapters/{chapter_id}")
            continue
        for name in REQUIRED_CHAPTER_FILES:
            if not (chapter_dir / name).is_file():
                errors.append(f"{chapter_id} missing {name}")
        lecture = chapter_dir / "lecture.md"
        if lecture.is_file():
            lines = lecture.read_text(encoding="utf-8").splitlines()
            if len(lines) > 300:
                errors.append(f"{chapter_id} lecture.md is {len(lines)} lines (max 300)")
        lab = chapter_dir / "lab.json"
        if lab.is_file():
            lab_json = load_json(lab)
            if lab_json.get("chapter_id") != chapter_id:
                errors.append(f"{chapter_id} lab.json.chapter_id mismatch")
            command = lab_json.get("test_command", "")
            if "{chapter_dir}" not in command:
                errors.append(f"{chapter_id} test_command must contain {{chapter_dir}}")
            if not lab_json.get("interface", {}).get("functions"):
                errors.append(f"{chapter_id} lab.json.interface.functions is empty")
        for spec in meta.get("source_files") or []:
            file_part = str(spec).split(":", 1)[0]
            if not (ROOT / file_part).is_file():
                errors.append(f"{chapter_id} source_files missing {file_part}")
        state = progress_chapters.get(chapter_id)
        if not isinstance(state, dict):
            errors.append(f"progress.json missing {chapter_id}")
        elif state.get("status") not in STATUSES:
            errors.append(f"progress.json {chapter_id}.status invalid")

    extra = set(progress_chapters) - set(ids)
    if extra:
        errors.append(f"progress.json has unknown chapters: {sorted(extra)}")
    if not (COURSE_DIR / "main.py").is_file():
        errors.append("missing .promentor/main.py (Final entry)")
    return errors


def test_command(chapter_dir: Path) -> list[str]:
    lab = load_json(chapter_dir / "lab.json")
    command = lab["test_command"].replace("{chapter_dir}", str(chapter_dir))
    return command.split()


def run_tests(chapter_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        test_command(chapter_dir),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def overlay_reference(chapter_id: str, dest: Path) -> None:
    if chapter_id == "ch05-assemble":
        shutil.copy2(REFERENCE_APP, dest / "app.py")
        return
    shutil.copy2(REFERENCE_ROUTER, dest / "router.py")


def check_tests() -> list[str]:
    course = load_json(COURSE_DIR / "course.json")
    errors: list[str] = []
    for meta in course["chapters"]:
        chapter_id = meta["id"]
        chapter_dir = CHAPTERS_DIR / chapter_id
        stub = run_tests(chapter_dir)
        if stub.returncode == 0:
            errors.append(f"{chapter_id}: stub implementation unexpectedly passed")
            continue

        with tempfile.TemporaryDirectory(prefix=f"prom-{chapter_id}-") as tmp:
            dest = Path(tmp) / chapter_id
            shutil.copytree(chapter_dir, dest)
            overlay_reference(chapter_id, dest)
            ref = run_tests(dest)
            if ref.returncode != 0:
                errors.append(
                    f"{chapter_id}: reference implementation failed\n"
                    f"{ref.stdout}{ref.stderr}"
                )
    return errors


def main() -> int:
    print("ProMentor golden course: mini-router")
    try:
        schema_errors = check_schema()
    except CheckError as exc:
        print(f"FAIL  schema: {exc}")
        return 1

    if schema_errors:
        print("FAIL  schema")
        for item in schema_errors:
            print(f"  - {item}")
        return 1
    print("PASS  schema / files / source_files")

    test_errors = check_tests()
    if test_errors:
        print("FAIL  tests")
        for item in test_errors:
            print(f"  - {item}")
        return 1
    print("PASS  stubs fail, reference passes")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
