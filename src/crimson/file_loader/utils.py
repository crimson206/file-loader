# src/crimson/file_loader/__init__.py
import os
from typing import List, Literal, overload, Union, Callable, TypeVar, Generic
from crimson.intelli_type import IntelliType
from pathlib import Path
import re

T = TypeVar("T")


class Search_(IntelliType[Callable[[str, str], bool]], Generic[T]):
    """
    A function to check if a text contains a pattern.\n
    The default search function is accessible by via:\n
    ```
    Search\_.default
    ```
    """

    @staticmethod
    def default(pattern: str, text: str):
        compiled_pattern = re.compile(pattern)
        is_included = compiled_pattern.search(text) is not None
        return is_included


class Includes_(IntelliType[List[str]], Generic[T]):
    """
    Patterns to include.\n
    The exact algorithm to search pattern can be customized via `Search_`.\n
    Shortcut for the reference : `Includes_.reference`
    """

    reference = {"search": Search_}


class Excludes_(IntelliType[List[str]], Generic[T]):
    """
    Patterns to exclude.\n
    The exact algorithm to search pattern can be customized via `Search_`.\n
    Shortcut for the reference : `Excludes_.reference`
    """

    reference = {"search": Search_}


class Mode_(IntelliType[Literal["include", "exclude"]], Generic[T]):
    """
    - If `mode` is `include`,
        - filter based functions
            - returns only the paths `matched` with patterns.
    - If `mode` is `exclude`,
        - filter based functions
            - returns only the paths `not matched` with patterns.
    """


class Paths_(IntelliType[Union[List[str], List[Path]]], Generic[T]):
    """
    Paths extracted from a source, and filtered by `filter`-based functions.
    """


class Source_(IntelliType[str], Generic[T]):
    """
    The base directory to extract the paths under it.\n
    All the paths under it will be extracted initially,\n
    and then, they will be filtered by additional processes.
    """


class Separator_(IntelliType[str], Generic[T]):
    """
    This module was initially planned to flatten paths.\n
    Some chatbot services allow us to upload files.\n
    In some cases, we can only drag files from one folder.\n
    Therefore, we want to collect necessary files in one folder keeping the structure information.\n
    We will add the directory information to the file name, and `/` is not ideal because your IDE can automatically use the pattern to construct the structure.\n
    The default `separator` is `%`. See the example:

    **Original**
        root/a/b/c.py
        root/a/d/e.py

    **Collected**
        out_dir/a\%b\%c.py
        out_dir/a\%d\%e.py

    We must also be able to recover the structure from the flatten files.\n
    The same `separator` must be used to recover it.
    """


@overload
def filter(
    pattern: str,
    paths: List[str],
    mode: Literal["include", "exclude"] = "include",
    search: Search_.annotation = Search_.default,
) -> List[str]:
    """
    Filter a list of string paths based on a pattern.
    """
    ...


@overload
def filter(
    pattern: str,
    paths: List[Path],
    mode: Literal["include", "exclude"] = "include",
    search: Search_.annotation = Search_.default,
) -> List[str]:
    """
    Filter a list of Path objects based on a pattern.
    """
    ...


def filter(
    pattern: str,
    paths: Paths_.annotation,
    mode: Mode_.annotation = "include",
    search: Search_.annotation = Search_.default,
) -> List[str]:
    """
    Filter paths based on a pattern, mode, and search function.
    """
    if isinstance(paths[0], Path):
        paths = _convert_paths_to_texts(paths)
    paths = _filter_base(
        pattern,
        paths,
        mode,
        search,
    )

    return paths


def _filter_base(
    pattern: str,
    paths: List[str],
    mode: Mode_.annotation = "include",
    search: Search_.annotation = Search_.default,
) -> List[str]:
    """
    Base filtering function used internally.
    """
    included = []
    for path in paths:
        is_included = search(pattern=pattern, text=path)
        if mode == "exclude":
            is_included = not is_included
        if is_included:
            included.append(path)
    return included


def _convert_paths_to_texts(paths: List[Path]) -> List[str]:
    """
    Convert a list of Path objects to a list of string paths.
    """
    texts = [str(path) for path in paths]
    return texts


def get_paths(
    source: Source_.annotation,
) -> List[str]:
    """
    Retrieve all file paths from the given source directory.
    """
    paths = []
    for root, _, files in os.walk(source):
        for file in files:
            file_path = Path(root) / file
            paths.append(str(file_path))
    return paths


##
def filter_paths(
    paths: Paths_.annotation,
    includes: Includes_.annotation = [],
    excludes: Excludes_.annotation = [],
    search: Search_.annotation = Search_.default,
):
    """
    Apply include and exclude filters to a list of paths.

    The function works as follows:
    1. If 'includes' is not empty:
       - Keeps only paths that match at least one pattern in 'includes'.
       - A path is included if it matches any of the include patterns.
    2. If 'includes' is empty:
       - All paths are initially kept.
    3. Then, for all remaining paths:
       - Removes any path that matches any pattern in 'excludes'.

    This approach allows for flexible filtering where you can first specify
    what to include, then exclude specific items from that included set.
    """
    if len(includes) != 0:
        included_paths = []
        for pattern in includes:
            included_paths += filter(pattern, paths, mode="include", search=search)
        paths = included_paths

    for pattern in excludes:
        if len(paths) != 0:
            paths = filter(pattern, paths, mode="exclude", search=search)

    return paths


def filter_source(
    source: Source_.annotation,
    includes: Includes_.annotation = [],
    excludes: Excludes_.annotation = [],
    search: Search_.annotation = Search_.default,
):
    """
    Filter paths from a source directory using include and exclude patterns.

    This function works in two steps:
    1. Retrieve all paths from the source directory using `get_paths()`.
    2. Apply filtering to these paths using `filter_paths()`.

    The filtering process is as follows:
    - If 'includes' is not empty:
      - Keeps only paths that match at least one pattern in 'includes'.
    - If 'includes' is empty:
      - All paths are initially kept.
    - Then, for all remaining paths:
      - Removes any path that matches any pattern in 'excludes'.

    This allows for flexible path filtering directly from a source directory,
    first specifying what to include, then excluding specific items from that set.
    """
    paths = get_paths(source)
    paths = filter_paths(paths, includes, excludes, search=search)
    return paths


def transform_path(path: str, separator: Separator_.annotation = "%") -> str:
    """
    Transform a path by replacing forward slashes with a specified separator.
    """
    path = path.replace("/", separator)
    return path
