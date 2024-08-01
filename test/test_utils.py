import pytest
import re
from pathlib import Path
from typing import List
from crimson.file_loader.utils import (
    filter,
    get_paths,
    filter_source,
    transform_path,
    filter_paths,
)



def test_filter():
    paths = ["file1.txt", "file2.py", "file3.jpg"]
    assert filter("\.txt$", paths) == ["file1.txt"]
    assert filter("\.py$", paths, mode="include") == ["file2.py"]
    assert filter("\.py$", paths, mode="exclude") == ["file1.txt", "file3.jpg"]
    paths_in_Path: List[Path] = [Path(path) for path in paths]
    assert filter("\.txt$", paths_in_Path) == ["file1.txt"]


def test_get_paths(tmp_path):
    # 임시 디렉토리 구조 생성
    d = tmp_path / "sub"
    d.mkdir()
    (d / "file1.txt").touch()
    (tmp_path / "file2.py").touch()

    paths = get_paths(str(tmp_path))
    assert len(paths) == 2
    assert str(tmp_path / "sub" / "file1.txt") in paths
    assert str(tmp_path / "file2.py") in paths


def test_filter_source(tmp_path):
    # 임시 디렉토리 구조 생성
    d = tmp_path / "sub"
    d.mkdir()
    (d / "file1.txt").touch()
    (tmp_path / "file2.py").touch()
    (tmp_path / "file3.jpg").touch()

    paths = filter_source(tmp_path, includes=["\.txt$", "\.py$"], excludes=["sub"])
    assert len(paths) == 1
    assert str(tmp_path / "file2.py") in paths


def test_transform_path():
    assert transform_path("/path/to/file.txt") == "%path%to%file.txt"
    assert transform_path("/path/to/file.txt", separator="-") == "-path-to-file.txt"


def test_filter_paths():
    paths = [
        "/home/user/docs/file1.txt",
        "/home/user/docs/file2.pdf",
        "/home/user/images/pic1.jpg",
        "/home/user/images/pic2.png",
        "/home/user/code/script.py",
    ]

    # Test with only includes
    result = filter_paths(paths, includes=[r"\.txt$", r"\.pdf$"])
    assert result == ["/home/user/docs/file1.txt", "/home/user/docs/file2.pdf"]

    # Test with only excludes
    result = filter_paths(paths, excludes=[r"\.jpg$", r"\.png$"])
    assert result == [
        "/home/user/docs/file1.txt",
        "/home/user/docs/file2.pdf",
        "/home/user/code/script.py",
    ]

    # Test with both includes and excludes
    result = filter_paths(
        paths, includes=[r"/docs/", r"/images/"], excludes=[r"\.pdf$"]
    )
    assert result == [
        "/home/user/docs/file1.txt",
        "/home/user/images/pic1.jpg",
        "/home/user/images/pic2.png",
    ]

    # Test with no matches in includes
    result = filter_paths(paths, includes=[r"\.mp3$"])
    assert result == []

    # Test with excludes that match everything
    result = filter_paths(paths, excludes=[r".*"])
    assert result == []

    # Test with empty includes and excludes
    result = filter_paths(paths)
    assert result == paths

    # Test with multiple include patterns
    result = filter_paths(paths, includes=[r"\.txt$", r"\.py$"])
    assert result == ["/home/user/docs/file1.txt", "/home/user/code/script.py"]

    # Test with overlapping includes and excludes
    result = filter_paths(
        paths, includes=[r"/docs/", r"/images/"], excludes=[r"\.jpg$", r"/docs/"]
    )
    assert result == ["/home/user/images/pic2.png"]
