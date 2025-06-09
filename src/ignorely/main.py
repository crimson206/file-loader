from cleo.application import Application
from ignorely.commands.ls_files import LsFilesCommand
from ignorely.commands.copy_files import CopyFilesCommand
from ignorely.commands.export_files import ExportFilesCommand

application = Application("ignorely", "1.0.0")
application.add(LsFilesCommand())
application.add(CopyFilesCommand())
application.add(ExportFilesCommand())

def main():
    application.run()


if __name__ == "__main__":
    main()
