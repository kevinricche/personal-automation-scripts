#!/usr/bin/env python3
"""
find_duplicates.py
Finds duplicate files in a directory by comparing SHA-256 checksums.
"""

import os
import sys
import hashlib
from collections import defaultdict


def hash_file(filepath, chunk_size=8192):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                sha256.update(chunk)
    except (PermissionError, OSError) as e:
        print(f"  Warning: could not read {filepath} ({e})")
        return None
    return sha256.hexdigest()


def find_duplicates(target_dir, recursive=False):
    """Scan directory for duplicate files."""
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    # First pass: group files by size (quick filter)
    size_map = defaultdict(list)

    if recursive:
        for root, dirs, files in os.walk(target_dir):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    size = os.path.getsize(filepath)
                    size_map[size].append(filepath)
                except OSError:
                    continue
    else:
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            if os.path.isfile(filepath):
                try:
                    size = os.path.getsize(filepath)
                    size_map[size].append(filepath)
                except OSError:
                    continue

    # Second pass: hash files that share the same size
    hash_map = defaultdict(list)
    candidates = {size: paths for size, paths in size_map.items() if len(paths) > 1}

    total_to_check = sum(len(paths) for paths in candidates.values())
    print(f"Found {total_to_check} files with shared sizes. Checking hashes...\n")

    for size, paths in candidates.items():
        for filepath in paths:
            file_hash = hash_file(filepath)
            if file_hash:
                hash_map[file_hash].append(filepath)

    # Report
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    if not duplicates:
        print("No duplicate files found.")
        return

    total_wasted = 0
    for file_hash, paths in duplicates.items():
        size = os.path.getsize(paths[0])
        wasted = size * (len(paths) - 1)
        total_wasted += wasted

        print(f"Duplicate set ({format_size(size)} each):")
        for p in paths:
            print(f"  {p}")
        print()

    print(f"Total duplicate sets: {len(duplicates)}")
    print(f"Space that could be recovered: {format_size(total_wasted)}")


def format_size(size_bytes):
    """Human-readable file size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_duplicates.py <directory> [--recursive]")
        sys.exit(1)

    directory = sys.argv[1]
    recursive = "--recursive" in sys.argv

    print(f"Scanning {'recursively ' if recursive else ''}{directory} for duplicates...\n")
    find_duplicates(directory, recursive=recursive)
