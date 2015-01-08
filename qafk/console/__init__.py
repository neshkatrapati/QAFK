import sys

from command_parser import CommandParser

def qafk () :
    cmd_parser = CommandParser()
    
    args = cmd_parser.parse()
    cmd_parser.run_commands(args)
        
