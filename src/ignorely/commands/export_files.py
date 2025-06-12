import os
from cleo.commands.command import Command
from cleo.helpers import argument, option
from ..utils import export_files


class ExportFilesCommand(Command):
    name = "export-files"
    description = "Filter and copy files in one step using ignorely directory structure"

    arguments = [argument("output_dir", description="Directory to copy files to", optional=True, default="output_dir")]

    options = [
        option(
            "ignorely-dir",
            'i',
            description="Directory containing ignorely configuration (default: .ignorely)",
            flag=False,
            default=".ignorely",
        ),
        option(
            "target-dir",
            't',
            description="Directory to scan for files (default: current directory)",
            flag=False,
            default=".",
        ),
        option(
            "dry-run",
            "d",
            description="Only show what would be copied without actually copying",
            flag=True,
        ),
        option(
            "flatten",
            'f',
            description="Flatten directory structure using divider in filenames",
            flag=True,
        ),
        option(
            "divider",
            'D',
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
        ignorely_dir = self.option("ignorely-dir")
        target_dir = self.option("target-dir")
        dry_run = self.option("dry-run")
        flatten = self.option("flatten")
        divider = self.option("divider")
        clean = self.option("clean")

        # target_dir 존재 확인
        if not os.path.exists(target_dir):
            self.line_error(f"Target directory does not exist: {target_dir}")
            return 1

        try:
            # export_files 함수 호출 (필터링 + 복사 통합)
            filtered_files, copied_files = export_files(
                output_dir=output_dir,
                ignorely_dir=ignorely_dir,
                target_dir=target_dir,
                dry_run=dry_run,
                flatten=flatten,
                divider=divider,
                clean=clean
            )

            # 결과 출력
            if not filtered_files:
                self.line("<comment>No files to export.</comment>")
                return 0

            # Clean 메시지
            if clean and os.path.exists(output_dir):
                if dry_run:
                    self.line(f"Would remove existing directory: {output_dir}")
                else:
                    self.info(f"Cleaned directory: {output_dir}")

            # 복사 결과 출력
            for file_path, dest_path in copied_files:
                if dry_run:
                    self.line(f"Would copy {file_path} to {dest_path}")
                else:
                    self.info(f"Copied {file_path} to {dest_path}")

            # 요약
            file_count = len(filtered_files)
            copied_count = len(copied_files)
            
            if dry_run:
                self.line(f"<comment>Found {file_count} files, would export {copied_count} to {output_dir}</comment>")
            else:
                self.line(f"<info>Found {file_count} files, exported {copied_count} to {output_dir}</info>")

        except Exception as e:
            self.line_error(f"Failed to export files: {str(e)}")
            return 1

        return 0