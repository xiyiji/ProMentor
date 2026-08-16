#!/usr/bin/env python3
"""Final entry: assemble the student app and start the stdlib HTTP server."""

from pathlib import Path
import sys

CHAPTER = Path(__file__).resolve().parent / "chapters" / "ch05-assemble"
sys.path.insert(0, str(CHAPTER))

from app import build_app, run  # noqa: E402

if __name__ == "__main__":
    run(build_app())
