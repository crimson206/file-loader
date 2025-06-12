from cleo.application import Application
from importlib.metadata import version
from ignorely.commands.ls_files import LsFilesCommand
from ignorely.commands.copy_files import CopyFilesCommand
from ignorely.commands.export_files import ExportFilesCommand
from ignorely.commands.init import InitCommand

try:
    app_version = version("ignorely")
except Exception:
    app_version = "unknown"

application = Application("ignorely", "3.0.0")
application.add(InitCommand())
application.add(LsFilesCommand())
application.add(CopyFilesCommand())
application.add(ExportFilesCommand())

def main():
    application.run()

if __name__ == "__main__":
    main()