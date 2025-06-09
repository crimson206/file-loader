import os
import unittest
import tempfile
import shutil
from unittest.mock import patch
from pathlib import Path

from ignorely.utils import (
    collect_patterns_from_files,
    get_all_files,
    filter_files_with_patterns,
    list_files,
)


class TestLsFiles(unittest.TestCase):
    def setUp(self):
        # 테스트용 임시 디렉토리 생성
        self.test_dir = tempfile.mkdtemp()
        self.old_dir = os.getcwd()
        os.chdir(self.test_dir)

        # 테스트 파일 구조 생성
        # 일반 파일들
        self.create_file("file1.txt", "content")
        self.create_file("file2.py", "print('hello')")
        self.create_file("file3.md", "# Heading")

        # 서브디렉토리와 파일들
        os.makedirs("subdir")
        self.create_file("subdir/subfile1.txt", "subcontent")
        self.create_file("subdir/subfile2.log", "log content")

        # 다른 서브디렉토리
        os.makedirs("node_modules/some_module")
        self.create_file("node_modules/some_module/index.js", "module.exports = {}")

        # gitignore 파일
        self.create_file(".gitignore", "*.log\nnode_modules/")

        # 커스텀 include/exclude 파일들
        self.create_file(".include", "*.py\n*.txt")
        self.create_file(".exclude", "*.md")

    def tearDown(self):
        # 임시 디렉토리 정리 및 원래 작업 디렉토리로 복귀
        os.chdir(self.old_dir)
        shutil.rmtree(self.test_dir)

    def create_file(self, path, content=""):
        # 편의를 위한 파일 생성 헬퍼 함수
        full_path = os.path.join(self.test_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

    def test_collect_patterns_from_files(self):
        # 패턴 수집 테스트
        patterns = collect_patterns_from_files([".gitignore"])
        self.assertEqual(patterns, ["*.log", "node_modules/"])

        patterns = collect_patterns_from_files([".include"])
        self.assertEqual(patterns, ["*.py", "*.txt"])

        patterns = collect_patterns_from_files([".exclude"])
        self.assertEqual(patterns, ["*.md"])

        # 존재하지 않는 파일 테스트
        patterns = collect_patterns_from_files(["nonexistent.ignore"])
        self.assertEqual(patterns, [])

    def test_get_all_files(self):
        # 모든 파일 수집 테스트
        files = get_all_files()
        expected_files = {
            "file1.txt",
            "file2.py",
            "file3.md",
            "subdir/subfile1.txt",
            "subdir/subfile2.log",
            "node_modules/some_module/index.js",
            ".gitignore",
            ".include",
            ".exclude",
        }
        self.assertEqual(set(files), expected_files)

    def test_filter_files_with_patterns(self):
        # 패턴으로 파일 필터링 테스트
        all_files = [
            "file1.txt",
            "file2.py",
            "file3.md",
            "subdir/subfile1.txt",
            "subdir/subfile2.log",
            "node_modules/some_module/index.js",
        ]

        # Include 패턴만 테스트
        filtered = filter_files_with_patterns(all_files, include_patterns=["*.py", "*.txt"])
        self.assertIn("file1.txt", filtered)
        self.assertIn("file2.py", filtered)
        self.assertIn("subdir/subfile1.txt", filtered)
        self.assertNotIn("file3.md", filtered)
        self.assertNotIn("subdir/subfile2.log", filtered)

        # Exclude 패턴만 테스트
        filtered = filter_files_with_patterns(all_files, exclude_patterns=["*.log", "node_modules/"])
        self.assertIn("file1.txt", filtered)
        self.assertNotIn("subdir/subfile2.log", filtered)
        self.assertNotIn("node_modules/some_module/index.js", filtered)

        # Include와 Exclude 패턴 함께 테스트
        filtered = filter_files_with_patterns(
            all_files,
            include_patterns=["*.py", "*.txt"],
            exclude_patterns=["subdir/*"],
        )
        self.assertIn("file1.txt", filtered)
        self.assertIn("file2.py", filtered)
        self.assertNotIn("subdir/subfile1.txt", filtered)
        self.assertNotIn("file3.md", filtered)

    def test_list_files(self):
        # 종합 기능 테스트
        # Include 패턴만 사용
        files = list_files(include_pattern_files=[".include"])
        self.assertIn("file1.txt", files)
        self.assertIn("file2.py", files)
        self.assertIn("subdir/subfile1.txt", files)
        self.assertNotIn("file3.md", files)

        # Exclude 패턴만 사용
        files = list_files(exclude_pattern_files=[".exclude"])
        self.assertIn("file1.txt", files)
        self.assertIn("file2.py", files)
        self.assertNotIn("file3.md", files)

        # Include와 Exclude 패턴 함께 사용
        files = list_files(
            include_pattern_files=[".include"],
            exclude_pattern_files=[".exclude"],
            ignore_files=[".gitignore"],
        )
        self.assertIn("file1.txt", files)
        self.assertIn("file2.py", files)
        self.assertNotIn("file3.md", files)
        self.assertNotIn("subdir/subfile2.log", files)
        self.assertNotIn("node_modules/some_module/index.js", files)


class TestLsFilesCommand(unittest.TestCase):
    def setUp(self):
        # 테스트용 임시 디렉토리 생성
        self.test_dir = tempfile.mkdtemp()
        self.old_dir = os.getcwd()
        os.chdir(self.test_dir)

        # 기본 파일 구조 생성
        Path("file1.txt").write_text("content")
        Path("file2.py").write_text("print('hello')")
        Path("node_modules/test.js").parent.mkdir(exist_ok=True, parents=True)
        Path("node_modules/test.js").write_text("console.log('test')")
        Path(".include").write_text("*.py\n*.txt")
        Path(".exclude").write_text("node_modules/")

    def tearDown(self):
        os.chdir(self.old_dir)
        shutil.rmtree(self.test_dir)

    @patch("sys.stdout")
    def test_ls_files_command(self, mock_stdout):
        from cleo.application import Application
        from cleo.testers.command_tester import CommandTester
        from ignorely.commands.ls_files import LsFilesCommand

        application = Application()
        command = LsFilesCommand()
        application.add(command)

        # CommandTester 사용
        command_tester = CommandTester(command)
        command_tester.execute("--inc-path .include --exc-path .exclude")

        # 실행 결과 검증
        output = command_tester.io.fetch_output()
        self.assertTrue(len(output) > 0)
        self.assertIn("file1.txt", output)
        self.assertIn("file2.py", output)
        self.assertNotIn("node_modules/test.js", output)


if __name__ == "__main__":
    unittest.main()
