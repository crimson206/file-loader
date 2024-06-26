# src/crimson/file_loader/__init__.py

import os
import shutil
from pathlib import Path
from typing import List, Optional

def transform_path(path: str, separator: str = "%") -> str:
    return path.replace(os.path.sep, separator)

def restore_path(transformed: str, separator: str = "%") -> str:
    return transformed.replace(separator, os.path.sep)

def load_files(
    source_dir: str,
    target_dir: str,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    separator: str = "%"
) -> List[str]:
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    loaded_files = []

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            relative_path = file_path.relative_to(source_path)

            if include_patterns and not any(relative_path.match(pattern) for pattern in include_patterns):
                continue
            if exclude_patterns and any(relative_path.match(pattern) for pattern in exclude_patterns):
                continue

            transformed_name = transform_path(str(relative_path), separator)
            target_file = target_path / transformed_name

            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, target_file)
            loaded_files.append(str(relative_path))

    return loaded_files

# Usage example
if __name__ == "__main__":
    source_directory = "path/to/source"
    target_directory = "path/to/target"
    include = ["*.py", "*.json"]
    exclude = ["*test*", "*__pycache__*"]

    loaded = load_files(source_directory, target_directory, include, exclude)
    print(f"Loaded {len(loaded)} files:")
    for file in loaded:
        print(file)