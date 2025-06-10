import os
import sys
from cleo.commands.command import Command
from cleo.helpers import argument, option
from ..utils import copy_files


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
        option(
            "clean",
            "c",
            description="Clean (remove) output directory before copying",
            flag=True,
        ),
    ]

    def handle(self):
        output_dir = self.argument("output_dir")
        list_file = self.option("list-file")
        dry_run = self.option("dry-run")
        flatten = self.option("flatten")
        divider = self.option("divider")
        clean = self.option("clean")

        # 파일 목록 가져오기
        files = []

        # 파일에서 목록 읽기
        if list_file:
            if os.path.exists(list_file):
                with open(list_file, "r") as f:
                    files = [line.strip() for line in f if line.strip()]
            else:
                self.line_error(f"File not found: {list_file}")
                return 1
        # 표준 입력에서 목록 읽기
        else:
            # 표준 입력이 파이프에서 오는지 확인
            if not os.isatty(sys.stdin.fileno()):
                files = [line.strip() for line in sys.stdin if line.strip()]
            else:
                self.line_error(
                    "No file list provided. Use --list-file or pipe from another command."
                )
                return 1

        if not files:
            self.line("<comment>No files to copy.</comment>")
            return 0

        # 복사 수행 (utils 함수 사용)
        try:
            copied_files = copy_files(
                files=files,
                output_dir=output_dir,
                dry_run=dry_run,
                flatten=flatten,
                divider=divider,
                clean=clean
            )
            
            # 결과 출력
            if clean and os.path.exists(output_dir):
                if dry_run:
                    self.line(f"Would remove existing directory: {output_dir}")
                else:
                    self.info(f"Cleaned directory: {output_dir}")
            
            for file_path, dest_path in copied_files:
                if dry_run:
                    self.line(f"Would copy {file_path} to {dest_path}")
                else:
                    self.info(f"Copied {file_path} to {dest_path}")
            
            copied_count = len(copied_files)
            if dry_run:
                self.line(f"<comment>Would copy {copied_count} files to {output_dir}</comment>")
            else:
                self.line(f"<info>Copied {copied_count} files to {output_dir}</info>")
                
        except Exception as e:
            self.line_error(f"Failed to copy files: {str(e)}")
            return 1

        return 0