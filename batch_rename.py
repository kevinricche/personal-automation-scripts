#!/usr/bin/env python3
"""
batch_rename.py
Batch rename files in a directory using a prefix and sequential numbering.
"""

import os
import sys
import argparse


def batch_rename(target_dir, prefix, start_num=1, padding=3, ext_filter=None, dry_run=False):
    """Rename files sequentially with a given prefix."""
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    files = sorted(os.listdir(target_dir))
    files = [f for f in files if os.path.isfile(os.path.join(target_dir, f))]

    # Filter by extension if specified
    if ext_filter:
        ext = ext_filter if ext_filter.startswith(".") else f".{ext_filter}"
        files = [f for f in files if f.lower().endswith(ext.lower())]

    if not files:
        print("No matching files found.")
        return

    renamed = 0
    for i, filename in enumerate(files, start=start_num):
        _, ext = os.path.splitext(filename)
        new_name = f"{prefix}{str(i).zfill(padding)}{ext}"

        old_path = os.path.join(target_dir, filename)
        new_path = os.path.join(target_dir, new_name)

        if dry_run:
            print(f"  [dry run] {filename} -> {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"  {filename} -> {new_name}")

        renamed += 1

    print(f"\nDone. {renamed} files {'would be ' if dry_run else ''}renamed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files with prefix and numbering.")
    parser.add_argument("directory", help="Target directory")
    parser.add_argument("--prefix", default="file_", help="Prefix for renamed files (default: file_)")
    parser.add_argument("--start", type=int, default=1, help="Starting number (default: 1)")
    parser.add_argument("--padding", type=int, default=3, help="Zero-padding width (default: 3)")
    parser.add_argument("--ext", default=None, help="Only rename files with this extension")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")

    args = parser.parse_args()

    batch_rename(
        args.directory,
        prefix=args.prefix,
        start_num=args.start,
        padding=args.padding,
        ext_filter=args.ext,
        dry_run=args.dry_run,
    )
