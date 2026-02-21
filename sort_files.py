#!/usr/bin/env python3
"""
sort_files.py
Sorts files in a directory into subfolders based on file extension.
"""

import os
import shutil
import sys

# Extension-to-folder mapping
CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".pptx"],
    "audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
    "video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm"],
    "archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".h", ".json", ".xml", ".yaml", ".yml"],
}


def get_category(extension):
    """Return the folder name for a given file extension."""
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "other"


def sort_files(target_dir, dry_run=False):
    """Sort files in target_dir into categorized subfolders."""
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    moved = 0
    skipped = 0

    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)

        # Skip directories
        if os.path.isdir(filepath):
            continue

        _, ext = os.path.splitext(filename)
        if not ext:
            skipped += 1
            continue

        category = get_category(ext)
        dest_dir = os.path.join(target_dir, category)

        if dry_run:
            print(f"  [dry run] {filename} -> {category}/")
        else:
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)

            # Handle name conflicts
            if os.path.exists(dest_path):
                base, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_dir, f"{base}_{counter}{extension}")
                    counter += 1

            shutil.move(filepath, dest_path)
            print(f"  {filename} -> {category}/")

        moved += 1

    print(f"\nDone. {moved} files sorted, {skipped} skipped.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sort_files.py <directory> [--dry-run]")
        sys.exit(1)

    directory = sys.argv[1]
    dry = "--dry-run" in sys.argv

    if dry:
        print(f"Dry run — previewing sort for: {directory}\n")
    else:
        print(f"Sorting files in: {directory}\n")

    sort_files(directory, dry_run=dry)
