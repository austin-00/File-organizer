import shutil
from pathlib import Path
from .categories import CATEGORIES

def build_extension_map():
    ext_map = {}
    for category, value in CATEGORIES.items():
        if isinstance(value, dict):
            for subcat, exts in value.items():
                for ext in exts:
                    ext_map[ext.lower()] = subcat
        else:
            for ext in value:
                ext_map[ext.lower()] = category
    return ext_map

def organize_files(source: str, destination: str, move=True, dry_run=False, progress_cb=None):
    ext_map = build_extension_map()
    source = Path(source)
    destination = Path(destination)

    if not source.is_dir():
        raise ValueError(f"Source folder does not exist: {source}")

    files = [f for f in source.iterdir() if f.is_file()]
    total = len(files)
    report = {"moved": 0, "skipped": 0, "errors": [], "by_category": {}}

    for i, file in enumerate(files, 1):
        ext = file.suffix.lower()
        category = ext_map.get(ext, "Other")
        target_dir = destination / category
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file.name

        if target_path.exists():
            stem, suffix = file.stem, file.suffix
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        try:
            if not dry_run:
                if move:
                    shutil.move(str(file), str(target_path))
                else:
                    shutil.copy2(str(file), str(target_path))
            report["moved"] += 1
            report["by_category"][category] = report["by_category"].get(category, 0) + 1
        except Exception as e:
            report["errors"].append((str(file), str(e)))
            report["skipped"] += 1

        if progress_cb:
            progress_cb(i, total, file.name)

    return report