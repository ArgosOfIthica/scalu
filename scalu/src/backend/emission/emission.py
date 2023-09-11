import scalu.src.model.structure as model
import scalu.src.model.universe as universe

class emission_queue_obj():

    def __init__(self):
        self.queue = []
        self.index = 0

    def append(self, element):
        if not universe.is_alias(element):
            raise Exception('invalid emission alias')
        if element not in self.queue:
            self.queue.append(element)

    def look(self):
        output = self.queue[self.index]
        self.index += 1
        return output

    def is_exhausted(self):
        return self.index == len(self.queue)


def emission(uni):
    emission_queue = emission_queue_obj()
    output = ''
    for construct in uni.constructs.values():
        if universe.is_definition(construct) and construct.alias.type == 'event':
            output += emit_aliased_computation(construct, uni, emission_queue)
    output = emit_aliased_computation(uni.root, uni, emission_queue) + output
    while not emission_queue.is_exhausted():
        compute = emission_queue.look()
        if compute not in uni.vars:
            compute = uni.alias_to_def[compute]
            output += emit_aliased_computation(compute, uni, emission_queue)
    output += uni.root.alias.identity
    return output

def emit_aliased_computation(computation_target, uni, emission_queue):
    if not universe.is_computation(computation_target):
        raise Exception('invalid aliased computation')
    emit_string = 'alias ' + computation_target.alias.identity + ' "'
    emit_string += emit_computation(computation_target, uni, emission_queue) + '"\n'
    return emit_string

def emit_computation(command, uni, emission_queue):
    emit_string = ''
    if universe.is_var(command):
        if len(command.commands) > 1:
            raise Exception('malformed variable definition')
        emit_string += 'alias ' + command.alias.identity + ' ' + command.commands[0].identity + ';'
        emission_queue.append(command.commands[0])
    elif universe.is_alias(command) and command in uni.vars:
        emit_string += command.identity + ';'
    elif universe.is_source_command(command):
        emit_string += command.string + ';'
    elif universe.is_bind(command):
        emit_string += 'bind ' + command.key + ' ' + command.compute.alias.identity + ';'
    elif universe.is_alias(command) and (command.type == 'service' or command.type == 'event'):
        emit_string += command.identity + ';'
        emission_queue.append(command)
    elif universe.is_alias(command):
        emit_string += emit_computation(uni.alias_to_def[command], uni, emission_queue)
    elif universe.is_definition(command):
        for subcommand in command.commands:
            emit_string += emit_computation(subcommand, uni, emission_queue)
    else:
        raise Exception('unknowable command type')
    return emit_string
