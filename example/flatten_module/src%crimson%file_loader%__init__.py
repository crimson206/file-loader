import os
from typing import Callable, Optional, Generic, TypeVar, List, TypedDict
from pathlib import Path
from crimson.intelli_type import IntelliType
import shutil
from .utils import (
    filter_source,
    transform_path,
    Search_,
    Source_,
    Includes_,
    Excludes_,
    Separator_,
)

T = TypeVar("T")


class ByteSourceDict(TypedDict):
    path: str
    content: bytes


class PostPathEditor_(IntelliType[Optional[Callable[[str], str]]], Generic[T]):
    """
    Allows custom editing of file paths after they have been transformed.

    The file name is initially replaced by the transformed path to add structure information.
    You can then apply additional custom editing using a function of this type.

    I added an example function for the better understanding. See the example:

    **After `transform_path`:**
        path = useless\%path\%src\%module\%file.py

    **After `PostPathEditor_.example(path)`:**
        path = src\%module\%file.py

    Refer to `PostPathEditor_.reference` for related components and additional information.
    """

    reference = {"separator": Separator_, "transform_path": transform_path}

    @staticmethod
    def example(text: str) -> str:
        parts = text.split("%")
        src_index = parts.index("src")
        result = "%".join(parts[src_index:])
        return result


class Overwrite_(IntelliType[bool], Generic[T]):
    """
    Determines whether to overwrite the existing output directory.

    If True, the existing output directory will be removed before creating a new one.
    If False, the operation will use the existing directory, potentially merging new files with existing ones.
    """


class OutDir_(IntelliType[str], Generic[T]):
    """
    Specifies the output directory for collected or reconstructed files.
    """


def generate_file_contents(
    source: Source_.annotation,
    separator: Separator_.annotation = "%",
    includes: Includes_.annotation = [],
    excludes: Excludes_.annotation = [],
    post_path_editor: PostPathEditor_.annotation = None,
    search: Search_.annotation = Search_.default,
) -> List[ByteSourceDict]:
    """
    Prepares file information (path and content) from a source directory,
    applies filtering and structure-info-augmented filename.

    Returns a list of SourceDict, each containing the new file path and its content.
    """
    source_paths = filter_source(source, includes, excludes, search=search)
    file_contents = []

    for src_path in source_paths:
        new_path = transform_path(src_path, separator)
        if post_path_editor:
            new_path = post_path_editor(new_path)

        with open(src_path, "rb") as f:
            content = f.read()

        file_contents.append({"path": new_path, "content": content})

    return file_contents


def collect_files(
    source: Source_.annotation,
    out_dir: OutDir_.annotation,
    separator: Separator_.annotation = "%",
    includes: Includes_.annotation = [],
    excludes: Excludes_.annotation = [],
    post_path_editor: PostPathEditor_.annotation = None,
    overwrite: Overwrite_.annotation = True,
    search: Search_.annotation = Search_.default,
):
    """
    Collects files from a source directory, applies filtering and structure-info-augmented filename,
    and copies them to a specified output directory with a flattened structure.
    """
    out_dir_path = Path(out_dir)
    if overwrite and out_dir_path.exists():
        shutil.rmtree(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    file_contents = generate_file_contents(
        source, separator, includes, excludes, post_path_editor, search
    )

    for item in file_contents:
        full_path = out_dir_path / item["path"]
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(item["content"])

    print(f"Files collected from {source} to {out_dir}")


def reconstruct_folder_structure(
    source: Source_.annotation,
    out_dir: OutDir_.annotation,
    separator: Separator_.annotation = "%",
    path_editor: PostPathEditor_.annotation = None,
    overwrite: Overwrite_.annotation = True,
):
    """
    Reconstructs the folder structure from a source directory containing files with
    structure-info-augmented filenames to an output directory, restoring the original structure.
    """
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
            new_file_path = (out_dir + "/" + relative_path).replace("//", "/")

            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

            shutil.copy2(src_file_path, new_file_path)

    print(f"Folder structure reconstructed from {source} to {out_dir}")
