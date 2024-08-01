# src/crimson/file_loader/__init__.py
import os
from typing import List, Literal, Optional, overload, Union
from pathlib import Path
import re


def search(pattern: str, text: str, flags: Optional[List[re.RegexFlag]] = None):
    combined_flags = 0
    if flags:
        for flag in flags:
            combined_flags |= flag

    compiled_pattern = re.compile(pattern, flags=combined_flags)

    is_included = compiled_pattern.search(text) is not None

    return is_included


@overload
def filter(
    pattern: str,
    paths: List[str],
    mode: Literal["include", "exclude"] = "include",
    flags: Optional[List[re.RegexFlag]] = None,
) -> List[str]:
    """doc1"""
    ...


@overload
def filter(
    pattern: str,
    paths: List[Path],
    mode: Literal["include", "exclude"] = "include",
    flags: Optional[List[re.RegexFlag]] = None,
) -> List[str]:
    """doc2"""
    ...


def filter(
    pattern: str,
    paths: Union[List[str], List[Path]],
    mode: Literal["include", "exclude"] = "include",
    flags: Optional[List[re.RegexFlag]] = None,
) -> List[str]:

    if isinstance(paths[0], Path):
        paths = _convert_paths_to_texts(paths)
    paths = _filter_base(
        pattern,
        paths,
        mode,
        flags,
    )

    return paths


def _filter_base(
    pattern: str,
    paths: List[str],
    mode: Literal["include", "exclude"] = "include",
    flags: Optional[List[re.RegexFlag]] = None,
) -> List[str]:
    included = []
    for path in paths:
        is_included = search(pattern, path, flags)
        if mode == "exclude":
            is_included = not is_included
        if is_included:
            included.append(path)
    return included


def _convert_paths_to_texts(paths: List[Path]) -> List[str]:
    texts = [str(path) for path in paths]
    return texts


def get_paths(
    source: str,
):
    paths = []
    for root, _, files in os.walk(source):
        for file in files:
            file_path = Path(root) / file
            paths.append(str(file_path))
    return paths


def filter_paths(
    paths: List[str],
    includes: List[str] = [],
    excludes: List[str] = [],
):

    if len(includes) != 0:
        included_paths = []
        for pattern in includes:
            included_paths += filter(pattern, paths, mode="include")
        paths = included_paths

    for pattern in excludes:
        if len(paths) != 0:
            paths = filter(pattern, paths, mode="exclude")

    return paths


def filter_source(
    source: str,
    includes: List[str] = [],
    excludes: List[str] = [],
):
    paths = get_paths(source)
    paths = filter_paths(paths, includes, excludes)
    return paths


def transform_path(path: str, separator: str = "%") -> str:
    path = path.replace("/", separator)
    return path
