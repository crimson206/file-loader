import os
from cleo.commands.command import Command
from cleo.helpers import argument, option
from ..utils import list_files


class LsFilesCommand(Command):
    name = "ls-files"
    description = "List files not ignored by specified ignore files"

    arguments = [
        argument(
            "ignore_files",
            description="Ignore files to use for filtering",
            multiple=True,
            optional=True,
        )
    ]

    options = [
        option(
            "from-file",
            "f",
            description="Read additional ignore files from file",
            flag=False,
            multiple=True,
        ),
        option(
            "output",
            "o",
            description="Save output to file instead of displaying",
            flag=False,
        ),
    ]

    def handle(self):
        # 받은 ignore 파일들
        ignore_files = self.argument("ignore_files")
        from_file_options = self.option("from-file")
        output_file = self.option("output")

        # --from-file 옵션으로 지정된 파일에서 ignore 파일 목록 추가
        additional_ignore_files = []
        if from_file_options:
            for file_path in from_file_options:
                if os.path.exists(file_path):
                    with open(file_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                additional_ignore_files.append(line)

        # 일반 함수 호출
        filtered_files = list_files(ignore_files, additional_ignore_files)

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
