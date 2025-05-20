import os
import unittest
import tempfile
import shutil
from unittest.mock import patch
from pathlib import Path

from ignorely.utils import (
    collect_ignore_patterns,
    get_all_files,
    filter_files,
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

        # 커스텀 ignore 파일
        self.create_file(".customignore", "*.md")

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

    def test_collect_ignore_patterns(self):
        # ignore 파일로부터 패턴 수집 테스트
        patterns = collect_ignore_patterns([".gitignore"])
        self.assertEqual(patterns, ["*.log", "node_modules/"])

        patterns = collect_ignore_patterns([".customignore"])
        self.assertEqual(patterns, ["*.md"])

        patterns = collect_ignore_patterns([".gitignore", ".customignore"])
        self.assertEqual(patterns, ["*.log", "node_modules/", "*.md"])

        # 존재하지 않는 파일 테스트
        patterns = collect_ignore_patterns(["nonexistent.ignore"])
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
            ".customignore",
        }
        self.assertEqual(set(files), expected_files)

    def test_filter_files(self):
        # 패턴으로 파일 필터링 테스트
        all_files = [
            "file1.txt",
            "file2.py",
            "file3.md",
            "subdir/subfile1.txt",
            "subdir/subfile2.log",
            "node_modules/some_module/index.js",
        ]

        # *.log 패턴 테스트
        filtered = filter_files(all_files, ["*.log"])
        self.assertNotIn("subdir/subfile2.log", filtered)
        self.assertIn("file1.txt", filtered)

        # node_modules/ 패턴 테스트
        filtered = filter_files(all_files, ["node_modules/"])
        self.assertNotIn("node_modules/some_module/index.js", filtered)
        self.assertIn("file1.txt", filtered)

        # 여러 패턴 테스트
        filtered = filter_files(all_files, ["*.log", "*.md"])
        self.assertNotIn("subdir/subfile2.log", filtered)
        self.assertNotIn("file3.md", filtered)
        self.assertIn("file1.txt", filtered)

    def test_list_files(self):
        # 종합 기능 테스트
        files = list_files([".gitignore"])
        # .log 파일과 node_modules 안의 파일은 제외되어야 함
        self.assertNotIn("subdir/subfile2.log", files)
        self.assertNotIn("node_modules/some_module/index.js", files)
        # 다른 파일들은 포함되어야 함
        self.assertIn("file1.txt", files)
        self.assertIn("file2.py", files)
        self.assertIn("file3.md", files)

        # 여러 ignore 파일 테스트
        files = list_files([".gitignore", ".customignore"])
        # .md 파일도 제외되어야 함
        self.assertNotIn("file3.md", files)
        self.assertIn("file1.txt", files)

    def test_list_files_with_additional(self):
        # 추가 ignore 파일 테스트
        additional = [".customignore"]
        files = list_files([".gitignore"], additional)
        self.assertNotIn("file3.md", files)
        self.assertNotIn("subdir/subfile2.log", files)
        self.assertIn("file1.txt", files)


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
        Path(".gitignore").write_text("node_modules/")

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
        command_tester.execute(".gitignore")

        # 실행 결과 검증
        output = command_tester.io.fetch_output()
        self.assertTrue(len(output) > 0)


if __name__ == "__main__":
    unittest.main()
