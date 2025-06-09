import os
from cleo.commands.command import Command
from cleo.helpers import option
from ..utils import list_files


class LsFilesCommand(Command):
    name = "ls-files"
    description = "List files with include/exclude filtering (defaults: .ignorely/exclude_tot, .ignorely/include_tot)"

    options = [
        option(
            "output",
            "o",
            description="Save output to file instead of displaying",
            flag=False,
        ),
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
    ]

    def handle(self):
        output_file = self.option("output")
        exclude_tot_file = self.option("exclude-tot")
        include_tot_file = self.option("include-tot")

        # 새로운 방식으로 파일 필터링
        filtered_files = list_files(
            exclude_tot_file=exclude_tot_file,
            include_tot_file=include_tot_file
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
                self.error(f"Failed to write to file {output_file}: {str(e)}")
                return 1
        else:
            # 콘솔에 결과 출력
            for file in filtered_files:
                self.line(file)

        return 0