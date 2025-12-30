import csv
from pathlib import Path
import shutil
from typing import Tuple, List


def move_files_from_csv(csv_path: str, dest_dir: str, preserve_structure: bool = False, dry_run: bool = False) -> Tuple[int, List[str]]:
    """Move files listed in a CSV to a destination directory.

    CSV is expected to contain one file path per row (first column used).
    Returns tuple (moved_count, errors).
    """
    csv_path = Path(csv_path)
    dest_dir = Path(dest_dir)
    moved = 0
    errors: List[str] = []

    if not csv_path.exists():
        errors.append(f"CSV file not found: {csv_path}")
        return moved, errors

    if not dry_run:
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Could not create destination dir {dest_dir}: {e}")
            return moved, errors

    with csv_path.open(newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            src = Path(row[0]).expanduser()
            if not src.exists():
                errors.append(f"Source not found: {src}")
                continue
            try:
                if preserve_structure:
                    # replicate the source's parent structure under dest_dir
                    rel_parent = src.parent
                    # if absolute, strip root (/)
                    if rel_parent.anchor:
                        rel_parent = Path('/').joinpath(*rel_parent.parts[1:])
                    target_dir = dest_dir.joinpath(rel_parent)
                else:
                    target_dir = dest_dir

                target = target_dir.joinpath(src.name)

                if dry_run:
                    print(f"DRY RUN: move {src} -> {target}")
                    moved += 1
                else:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(target))
                    moved += 1
            except Exception as e:
                errors.append(f"Error moving {src} -> {target}: {e}")

    return moved, errors
