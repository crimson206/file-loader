import os
from cleo.commands.command import Command
from cleo.helpers import argument, option
from ..utils import export_files


class ExportFilesCommand(Command):
    name = "export-files"
    description = "Filter and copy files in one step (combines ls-files + copy-files)"

    arguments = [argument("output_dir", description="Directory to copy files to")]

    options = [
        option(
            "exclude-tot",
            "e",
            description="File containing list of exclude pattern files (default: .ignorely/exclude_tot)",
            flag=False,
            default=".ignorely/exclude_tot",
        ),
        option(
            "include-tot",
            "i",
            description="File containing list of include pattern files (default: .ignorely/include_tot)",
            flag=False,
            default=".ignorely/include_tot",
        ),
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
        exclude_tot_file = self.option("exclude-tot")
        include_tot_file = self.option("include-tot")
        dry_run = self.option("dry-run")
        flatten = self.option("flatten")
        divider = self.option("divider")
        clean = self.option("clean")

        try:
            # export_files 함수 호출 (필터링 + 복사 통합)
            filtered_files, copied_files = export_files(
                output_dir=output_dir,
                exclude_tot_file=exclude_tot_file,
                include_tot_file=include_tot_file,
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
            self.error(f"Failed to export files: {str(e)}")
            return 1

        return 0
