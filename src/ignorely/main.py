from cleo.application import Application
from ignorely.commands.ls_files import LsFilesCommand
from ignorely.commands.copy_files import CopyFilesCommand

application = Application("ignorely", "1.0.0")
application.add(LsFilesCommand())
application.add(CopyFilesCommand())


def main():
    application.run()


if __name__ == "__main__":
    main()
