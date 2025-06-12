import os
from cleo.commands.command import Command
from cleo.helpers import option
from ..utils import list_files


class LsFilesCommand(Command):
    name = "ls-files"
    description = "List files with include/exclude filtering using ignorely directory structure"

    options = [
        option(
            "output",
            "o",
            description="Save output to file instead of displaying",
            flag=False,
        ),
        option(
            "ignorely-dir",
            None,
            description="Directory containing ignorely configuration (default: .ignorely)",
            flag=False,
            default=".ignorely",
        ),
        option(
            "target-dir",
            None,
            description="Directory to scan for files (default: current directory)",
            flag=False,
            default=".",
        ),
    ]

    def handle(self):
        output_file = self.option("output")
        ignorely_dir = self.option("ignorely-dir")
        target_dir = self.option("target-dir")

        # target_dir 존재 확인
        if not os.path.exists(target_dir):
            self.line_error(f"Target directory does not exist: {target_dir}")
            return 1

        try:
            # 파일 필터링
            filtered_files = list_files(
                ignorely_dir=ignorely_dir,
                target_dir=target_dir
            )

            # 결과를 파일에 저장할지 콘솔에 출력할지 결정
            if output_file:
                try:
                    # 파일에 결과 저장
                    with open(output_file, "w") as f:
                        for file in filtered_files:
                            f.write(f"{file}\n")
                    self.info(f"Results saved to {output_file}")
                except Exception as e:
                    self.line_error(f"Failed to write to file {output_file}: {str(e)}")
                    return 1
            else:
                # 콘솔에 결과 출력
                for file in filtered_files:
                    self.line(file)

            # 요약 정보
            file_count = len(filtered_files)
            self.line(f"<comment>Found {file_count} files matching filters</comment>")

        except Exception as e:
            self.line_error(f"Failed to list files: {str(e)}")
            return 1

        return 0