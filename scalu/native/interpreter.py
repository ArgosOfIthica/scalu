
import re

class native_console():
    
    def __init__(self):
        self.aliases = {}
        self.output_buffer = ''
        self.assignment_count = 0
        self.execution_count = 0

    def parse_input(self, program):
        lines = program.split('\n')
        for line in lines:
            self.parse_line(line)
        return self

    def pop_output_buffer(self):
        temp = self.output_buffer
        self.output_buffer = ''
        return temp

    def clean_commands(self, commands):
        return tuple(command.strip('"') for command in commands if not command.isspace() and not command == '')

    def parse_line(self, line):
        commands = re.split('(".*"|\s)',line)
        commands = self.clean_commands(commands)
        if len(commands) == 0:
            return
        elif commands[0] == 'alias':
            key = commands[1]
            if len(commands) > 2:
                value = commands[2]
            else:
                value = ''
            self.aliases[key] = value
            self.assignment_count += 1
        elif commands[0] == 'echo':
            self.output_buffer += '\n' + ' '.join(commands[1:])
        else:
            value = self.aliases[line]
            subcommands = value.split(';')
            for command in subcommands:
                self.parse_line(command) 
            self.execution_count += 1
    
    def stats(self):
        counts = '\nAliases : ' + str(len(self.aliases))
        counts += '\nAssignments : ' + str(self.assignment_count)
        counts += '\nExecutions : ' + str(self.execution_count)
        return counts