#!/usr/bin/env python3
"""
clean_downloads.py
Removes files older than a specified number of days from a target directory.
Useful for keeping a Downloads folder from growing forever.
"""

import os
import sys
import time
import argparse


def clean_old_files(target_dir, max_age_days, dry_run=False, exclude_ext=None):
    """Delete files older than max_age_days in target_dir."""
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    cutoff = time.time() - (max_age_days * 86400)
    removed = 0
    freed = 0
    skipped = 0

    exclude = set()
    if exclude_ext:
        exclude = {e if e.startswith(".") else f".{e}" for e in exclude_ext}

    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)

        if os.path.isdir(filepath):
            continue

        _, ext = os.path.splitext(filename)
        if ext.lower() in exclude:
            skipped += 1
            continue

        try:
            mtime = os.path.getmtime(filepath)
        except OSError:
            continue

        if mtime < cutoff:
            size = os.path.getsize(filepath)
            age_days = int((time.time() - mtime) / 86400)

            if dry_run:
                print(f"  [dry run] Would delete: {filename} ({age_days} days old, {format_size(size)})")
            else:
                try:
                    os.remove(filepath)
                    print(f"  Deleted: {filename} ({age_days} days old, {format_size(size)})")
                except OSError as e:
                    print(f"  Error deleting {filename}: {e}")
                    continue

            removed += 1
            freed += size

    action = "would be deleted" if dry_run else "deleted"
    print(f"\nDone. {removed} files {action}, {format_size(freed)} freed. {skipped} skipped by filter.")


def format_size(size_bytes):
    """Human-readable file size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up old files from a directory.")
    parser.add_argument("directory", help="Target directory to clean")
    parser.add_argument("--days", type=int, default=30, help="Delete files older than this many days (default: 30)")
    parser.add_argument("--exclude", nargs="*", default=[], help="File extensions to exclude (e.g., .pdf .docx)")
    parser.add_argument("--dry-run", action="store_true", help="Preview deletions without removing files")

    args = parser.parse_args()

    mode = "Dry run" if args.dry_run else "Cleaning"
    print(f"{mode}: removing files older than {args.days} days from {args.directory}\n")

    clean_old_files(
        args.directory,
        max_age_days=args.days,
        dry_run=args.dry_run,
        exclude_ext=args.exclude,
    )
