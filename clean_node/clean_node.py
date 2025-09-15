#!/usr/bin/env python3
"""
Find and optionally delete npm module folders.

- Recursively searches for directories named "node_modules" or "npm_modules"
  under a given root (default: current directory).
- Prints all matches with index numbers.
- Prompts once: move all to Recycle Bin (preferred) or delete permanently.
- Use --permanent to skip Recycle Bin and delete immediately.

Tip: install send2trash for safe deletion:
    pip install send2trash
"""

import argparse
import os
import sys
import shutil
import stat
from pathlib import Path
from typing import List

# Try to import send2trash for reversible deletions
try:
    from send2trash import send2trash  # type: ignore
    HAS_SEND2TRASH = True
except Exception:
    HAS_SEND2TRASH = False

TARGET_NAMES = {"node_modules", "npm_modules"}

def on_rm_error(func, path, exc_info):
    # Make read-only files writable then retry
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass  # let shutil.rmtree surface the original error

def find_module_dirs(root: Path, target_names: set[str]) -> List[Path]:
    matches: List[Path] = []
    # Use os.walk for pruning so we don't traverse into node_modules (speed!)
    for dirpath, dirnames, _ in os.walk(root):
        # Normalize names (case-insensitive on Windows)
        to_remove = []
        for name in dirnames:
            if name.lower() in target_names:
                p = Path(dirpath) / name
                matches.append(p)
                # prune so we don't descend into huge folders
                to_remove.append(name)
        # Remove after iterating to avoid modifying while iterating
        for name in to_remove:
            try:
                dirnames.remove(name)
            except ValueError:
                pass
    return matches

def delete_dir(path: Path, use_recycle: bool):
    if use_recycle:
        send2trash(str(path))
    else:
        shutil.rmtree(path, onerror=on_rm_error)

def main():
    parser = argparse.ArgumentParser(
        description="List and optionally delete node/npm modules directories."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--permanent",
        action="store_true",
        help="Delete permanently (skip Recycle Bin even if available).",
    )
    parser.add_argument(
        "--name",
        choices=sorted(TARGET_NAMES),
        action="append",
        help="Limit to a specific folder name (can be used multiple times).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Error: '{root}' is not a directory.", file=sys.stderr)
        sys.exit(1)

        # Narrow target names if --name provided
    if args.name:
        # use a local variable instead of touching the global directly
        target_names = set(args.name)
    else:
        target_names = TARGET_NAMES

    print(f"\nScanning under: {root}\nThis may take a moment...\n")
    matches = find_module_dirs(root, target_names)


    if not matches:
        print("No matching module folders found.")
        return

    # Pretty print results
    print("Found the following module folders:\n")
    for i, p in enumerate(matches, start=1):
        try:
            # Show parent project folder for context
            proj = p.parent
            print(f"{i:3d}. {p}    (project: {proj.name})")
        except Exception:
            print(f"{i:3d}. {p}")

    # Decide deletion mode
    can_recycle = HAS_SEND2TRASH and not args.permanent
    if not HAS_SEND2TRASH and not args.permanent:
        print(
            "\nNote: 'send2trash' is not installed. "
            "Deletion will be PERMANENT unless you install it:\n"
            "    pip install send2trash\n"
        )

    # Prompt
    yn = input(
        f"\nMove ALL {len(matches)} folder(s) "
        f"{'to the Recycle Bin' if can_recycle else 'to PERMANENT deletion'}? [y/N]: "
    ).strip().lower()

    if yn != "y":
        print("Aborted. No changes made.")
        return

    # Delete
    errors = []
    for p in matches:
        try:
            delete_dir(p, use_recycle=can_recycle)
            print(f"✓ Removed: {p}")
        except Exception as e:
            errors.append((p, e))
            print(f"✗ Failed:  {p}  ({e})", file=sys.stderr)

    if errors:
        print(
            f"\nCompleted with {len(errors)} error(s). "
            "Some folders could not be removed. Try running with elevated permissions."
        )
    else:
        print("\nAll selected folders removed.")

if __name__ == "__main__":
    main()
