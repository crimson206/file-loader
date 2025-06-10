from cleo.commands.command import Command
from cleo.helpers import argument

from ignorely.utils import initialize_ignorely_directory


class InitCommand(Command):
    name = "init"
    description = "Initialize .ignorely directory with required files"
    arguments = [
        argument(
            "directory",
            description="Target directory to initialize (defaults to current directory)",
            optional=True,
            default="."
        )
    ]
    
    def handle(self):
        directory = self.argument("directory")
        
        success = initialize_ignorely_directory(directory)
        
        if success:
            self.line(f"<info>Successfully initialized .ignorely directory in {directory}</info>")
        else:
            self.line("<error>.ignorely directory already exists</error>")
            return 1
        
        return 0 