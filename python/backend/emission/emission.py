
import backend.model.universe as model

def emit(computation_target, uni):
	emission_queue = list()
	emit_string = 'alias ' + computation_target.alias.string + computation_target.alias.type + ' "'
	for command in computation_target.commands:
		if model.is_computation(command):
			if is_normalized(command):
				emit_string += 'alias ' + command.alias.string + ' ' + command.commands[0].string
			else:
				emit_string += command.alias.string
				emission_queue.append(command)
		elif model.is_alias(command):
			emit_string += command.string
		elif model.is_source_command(command):
			emit_string += command.string
		elif model.is_bind(command):
			emit_string += 'bind ' + command.key + ' ' + command.compute.alias.string
			emission_queue.append(command.compute)
		emit_string += ';'
	emit_string += '"\n'
	for compute in emission_queue:
		emit_string += emit(compute, uni)
	return emit_string

def is_normalized(compute):
	return len(compute.commands) == 1 and model.is_alias(compute.commands[0])
