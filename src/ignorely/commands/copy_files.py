import os
import shutil
import sys
from cleo.commands.command import Command
from cleo.helpers import argument, option


class CopyFilesCommand(Command):
    name = "copy-files"
    description = "Copy files to output directory based on provided file list"

    arguments = [argument("output_dir", description="Directory to copy files to")]

    options = [
        option("list-file", "l", description="Read file list from file", flag=False),
        option(
            "dry-run",
            "d",
            description="Only show what would be copied without actually copying",
            flag=True,
        ),
        option(
            "flatten",
            None,
            description="Flatten directory structure using divider in filenames",
            flag=True,
        ),
        option(
            "divider",
            None,
            description="Character to use as path divider when flattening (default: %)",
            flag=False,
            default="%",
        ),
    ]

    def handle(self):
        output_dir = self.argument("output_dir")
        list_file = self.option("list-file")
        dry_run = self.option("dry-run")
        flatten = self.option("flatten")
        divider = self.option("divider")

        # 파일 목록 가져오기
        files = []

        # 파일에서 목록 읽기
        if list_file:
            if os.path.exists(list_file):
                with open(list_file, "r") as f:
                    files = [line.strip() for line in f if line.strip()]
            else:
                self.error(f"File not found: {list_file}")
                return 1
        # 표준 입력에서 목록 읽기
        else:
            # 표준 입력이 파이프에서 오는지 확인
            if not os.isatty(sys.stdin.fileno()):
                files = [line.strip() for line in sys.stdin if line.strip()]
            else:
                self.error(
                    "No file list provided. Use --list-file or pipe from another command."
                )
                return 1

        if not files:
            self.line("<comment>No files to copy.</comment>")
            return 0

        # 복사 수행
        copied_count = 0
        for file in files:
            if not os.path.exists(file):
                self.line(f"<comment>File not found: {file}</comment>")
                continue

            if flatten:
                # 플래튼 모드: 디렉토리 구조를 평탄화하고 divider로 경로 구분
                flat_filename = file.replace(os.path.sep, divider)
                dest_path = os.path.join(output_dir, flat_filename)

                # 출력 디렉토리 생성
                if not os.path.exists(output_dir) and not dry_run:
                    os.makedirs(output_dir, exist_ok=True)
            else:
                # 일반 모드: 원본 디렉토리 구조 유지
                dest_path = os.path.join(output_dir, file)
                dest_dir = os.path.dirname(dest_path)

                # 하위 디렉토리 생성
                if not dry_run and not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)

            if dry_run:
                self.line(f"Would copy {file} to {dest_path}")
            else:
                try:
                    shutil.copy2(file, dest_path)
                    self.info(f"Copied {file} to {dest_path}")
                    copied_count += 1
                except Exception as e:
                    self.error(f"Failed to copy {file}: {str(e)}")

        if dry_run:
            self.line(f"Would copy {copied_count} files to {output_dir}")
        else:
            self.line(f"Copied {copied_count} files to {output_dir}")

        return 0
