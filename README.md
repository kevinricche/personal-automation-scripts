# personal-automation-scripts

A handful of utility scripts I use for routine file management and cleanup tasks.

## Scripts

- **sort_files.py** — Sorts files in a directory into subfolders by file type
- **batch_rename.py** — Batch rename files using pattern matching
- **find_duplicates.py** — Finds duplicate files by comparing checksums
- **clean_downloads.py** — Cleans up old files from a target folder based on age

## Usage

Each script runs standalone with Python 3.8+. No external dependencies required.

```
python sort_files.py /path/to/messy/folder
python batch_rename.py /path/to/folder --prefix "photo_" --start 1
python find_duplicates.py /path/to/folder
python clean_downloads.py /path/to/downloads --days 30
```

## Notes

These are personal tools — minimal error handling, built for my own use. Feel free to adapt.
