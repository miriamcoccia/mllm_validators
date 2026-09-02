"""
dump_codebase.py: walks a project folder, finds every .py file, and
concatenates them into one big .txt file, each preceded by its folder
path as a comment. Use this to hand a whole codebase to Claude at once.

Usage:
    uv run python dump_codebase.py
    uv run python dump_codebase.py --root . --output codebase_dump.txt
"""

import argparse
from pathlib import Path

# Folders never worth including: virtual envs, caches, git internals,
# and generated data/results (large, and not code).
EXCLUDED_DIR_NAMES = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".pytest_cache",
    "node_modules",
    "runs",
    "data",
    ".mypy_cache",
    "egg-info",
}


def should_skip(path: Path) -> bool:
    """
    True if any part of this path's folders matches an excluded name.
    """
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def dump_codebase(root: Path, output_path: Path) -> None:
    python_files = sorted(
        p for p in root.rglob("*.py") if not should_skip(p.relative_to(root))
    )

    with open(output_path, "w", encoding="utf-8") as out:
        for file_path in python_files:
            relative_path = file_path.relative_to(root)

            # Folder path as a comment, right before the file's own content.
            out.write(f"# ===== {relative_path} =====\n")

            content = file_path.read_text(encoding="utf-8")
            out.write(content)

            if not content.endswith("\n"):
                out.write("\n")
            out.write("\n")

    print(f"Wrote {len(python_files)} files to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Project root to search from (default: current directory).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("codebase_dump.txt"),
        help="Output file path (default: codebase_dump.txt).",
    )
    args = parser.parse_args()

    dump_codebase(args.root, args.output)
