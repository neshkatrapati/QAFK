import argparse
from qafk.workers.project import ProjectWorker
class CommandParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='qafk')
        self.sub_parsers = {}
        self.subcommands = {
            'run' : {},
            'new-project' : {"args" : {'project_name' : "Name of the project"}, "callback":ProjectWorker.create_project}
        }

        self.add_args()
        
    def add_args (self):
        subparsers = self.parser.add_subparsers(help='sub-command help', dest="subcommand_name")
        for sub_command in self.subcommands:
            self.sub_parsers[sub_command] = subparsers.add_parser(sub_command,
                                                                  help='sub_command help'.format(sub_command=sub_command))
            if "args" in self.subcommands[sub_command]:
                for argument in self.subcommands[sub_command]["args"]:
                    self.sub_parsers[sub_command].add_argument(argument,
                                                               help = self.subcommands[sub_command]["args"][argument])
        
    def parse(self):
        return self.parser.parse_args()


    def run_commands(self, args):
        for subcommand in self.subcommands:
            if args.subcommand_name == subcommand:
                method = self.subcommands[subcommand]['callback']
                method (args)
                break
        
