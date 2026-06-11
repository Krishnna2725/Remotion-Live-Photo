#!/usr/bin/env python3
"""Initialize the reusable Remotion Live Photo workspace from the bundled template."""

import argparse
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target directory for the reusable workspace")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    template = skill_dir / "assets" / "remotion-workspace"
    target = Path(args.target).resolve()

    if not template.is_dir():
        print(f"Template not found: {template}", file=sys.stderr)
        return 1
    if target.exists() and any(target.iterdir()):
        print(f"Target already exists and is not empty: {target}", file=sys.stderr)
        return 2

    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target, dirs_exist_ok=True)
    print(f"Initialized reusable Remotion workspace: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
