"""Deliver the finished page image to the grader's output folder.

The artwork ships in the repo as entry.png beside this script.  The
grader tells us where it wants the file through MAKEFUN_OUTPUT_DIR;
when that variable is absent we fall back to the conventional /output.
"""

from pathlib import Path
import os
import shutil
import sys

SOURCE_NAME = "entry.png"


def target_folder() -> Path:
    """Return the destination directory, honouring the env override."""
    raw = os.getenv("MAKEFUN_OUTPUT_DIR")
    return Path(raw) if raw else Path("/output")


def deliver() -> Path:
    origin = Path(__file__).resolve().parent / SOURCE_NAME
    folder = target_folder()
    folder.mkdir(parents=True, exist_ok=True)
    landing = folder / SOURCE_NAME
    shutil.copyfile(origin, landing)
    return landing


def run() -> int:
    placed = deliver()
    print(f"entry image delivered: {placed} ({placed.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
