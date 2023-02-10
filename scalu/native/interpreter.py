
import re

class native_console():
    
    def __init__(self):
        self.aliases = dict()
        self.output_buffer = str()
        self.assignment_count = 0
        self.execution_count = 0

    def parse_input(self, program):
        lines = re.split('\n',program)
        for line in lines:
            self.parse_line(line, True)
        return self

    def pop_output_buffer(self):
        temp = self.output_buffer
        self.output_buffer = str()
        return temp

    def clean_commands(self, commands):
        stripped_commands = list()
        for command in commands:
            if not command.isspace() and not command == '':
                stripped_commands.append(command)
        commands = list()
        for command in stripped_commands:
            if command[0] == '"' and command[-1] == '"':
                commands.append(command[1:-1])
            else:
                commands.append(command)
        return commands

    def parse_line(self, line, is_outer=False):
        commands = re.split('(".*"|\s)',line)
        commands = self.clean_commands(commands)
        if len(commands) == 0:
            return
        if commands[0] == 'alias' and is_outer:
            key = commands[1]
            value = commands[2]
            self.aliases[key] = value
            self.assignment_count += 1
        elif commands[0] == 'alias' and not is_outer:
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
            self.execute(line)
            self.execution_count += 1
    
    def execute(self, custom_command):
        value = self.aliases[custom_command]
        subcommands = re.split(';', value)
        for command in subcommands:
            self.parse_line(command)

    def stats(self):
        counts = '\nAliases : ' + str(len(self.aliases))
        counts += '\nAssignments : ' + str(self.assignment_count)
        counts += '\nExecutions : ' + str(self.execution_count)
        return counts


                



            



