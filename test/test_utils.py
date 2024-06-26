import pytest
import re
from pathlib import Path
from typing import List
from crimson.file_loader.utils import (
    search,
    filter,
    get_paths,
    filter_paths,
    transform_path,
)


def test_search():
    assert search("test", "This is a test string")
    assert not search("python", "This is a test string")
    assert search("TEST", "This is a test string", flags=[re.IGNORECASE])


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


def test_filter_paths(tmp_path):
    # 임시 디렉토리 구조 생성
    d = tmp_path / "sub"
    d.mkdir()
    (d / "file1.txt").touch()
    (tmp_path / "file2.py").touch()
    (tmp_path / "file3.jpg").touch()

    paths = filter_paths(tmp_path, includes=["\.txt$", "\.py$"], excludes=["sub"])
    assert len(paths) == 1
    assert str(tmp_path / "file2.py") in paths


def test_transform_path():
    assert transform_path("/path/to/file.txt") == "%path%to%file.txt"
    assert transform_path("/path/to/file.txt", separator="-") == "-path-to-file.txt"


# 추가 테스트 케이스를 여기에 작성할 수 있습니다.
