
from backend.alias import *

def emission(header, uni):
	return emit(header, uni)


def emit(computation_target, uni):
	emission_queue = list()
	emit_string = 'alias ' + computation_target.alias.string + computation_target.alias.type + ' "'
	for command in computation_target.commands:
		if isinstance(command, computation):
			if is_normalized(command):
				emit_string += 'alias ' + command.alias.string + ' ' + command.commands[0].string
			else:
				emit_string += command.alias.string
				emission_queue.append(command)
		elif isinstance(command, alias):
			emit_string += command.string
		elif isinstance(command, source_command):
			emit_string += command.string
		elif isinstance(command, bind):
			emit_string += 'bind ' + command.key + ' ' + command.compute.alias.string
			emission_queue.append(command.compute)
		emit_string += ';'
	emit_string += '"\n'
	for compute in emission_queue:
		emit_string += emit(compute, uni)
	return emit_string

def is_normalized(compute):
	return len(compute.commands) == 1 and isinstance(compute.commands[0], alias)
