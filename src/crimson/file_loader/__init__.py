# src/crimson/file_loader/__init__.py
import os
from typing import List, Callable, Optional
from pathlib import Path
import shutil
from .utils import (
    filter_source,
    transform_path,
)


def collect_files(
    source: str,
    out_dir: str,
    separator: str = "%",
    includes: List[str] = [],
    excludes: List[str] = [],
    path_editor: Optional[Callable[[str], str]] = None,
    overwrite: bool = True,
):
    out_dir_path = Path(out_dir)
    if overwrite and out_dir_path.exists():
        shutil.rmtree(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    source_paths = filter_source(source, includes, excludes)

    for src_path in source_paths:

        new_path = transform_path(src_path, separator)
        if path_editor:
            new_path = path_editor(new_path)
        new_path = str(Path(out_dir) / new_path)

        Path(new_path).parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src_path, new_path)

    print(f"Files collected from {source} to {out_dir}")


def reconstruct_folder_structure(
    source: str,
    out_dir: str,
    separator: str = "%",
    path_editor: Optional[Callable[[str], str]] = None,
    overwrite: bool = True,
):

    out_dir_path = Path(out_dir)

    if overwrite and out_dir_path.exists():
        shutil.rmtree(out_dir)

    out_dir_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(source):
        for file in files:

            src_file_path = os.path.join(root, file)

            if path_editor:
                file = path_editor(file)

            relative_path = file.replace(separator, os.path.sep)
            new_file_path = (out_dir + '/' + relative_path).replace('//', '/')

            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            shutil.copy2(src_file_path, new_file_path)

    print(f"Folder structure reconstructed from {source} to {out_dir}")
