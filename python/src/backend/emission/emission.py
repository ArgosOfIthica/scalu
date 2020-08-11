
import src.model.structure as model
import src.backend.model.universe as universe

def emission(uni):
	output = ''
	for ele in uni.constructs:
		if model.is_variable(ele):
			for computes in uni.constructs[ele].commands:
				for subcomputes in computes.commands:
					output += emit(subcomputes, uni)
		elif model.is_key(ele):
			output += emit(uni.constructs[ele], uni)
		if uni.constructs[ele].alias.type == 'service':
			output += emit(uni.constructs[ele], uni)
	output += emit(uni.root, uni)
	return output

def emit(computation_target, uni):
	emission_queue = list()
	emit_string = 'alias ' + computation_target.alias.identity + ' "'
	for command in computation_target.commands:
		if universe.is_computation(command):
			if is_normalized(command):
				emit_string += 'alias ' + command.alias.identity + ' ' + command.commands[0].string
				if is_alias_normalization(command):
					emit_string += command.commands[0].type
			else:
				emit_string += command.alias.identity
				emission_queue.append(command)
		elif universe.is_alias(command):
			emit_string += command.identity
		elif universe.is_source_command(command):
			emit_string += command.string
		elif universe.is_bind(command):
			emit_string += 'bind ' + command.key + ' ' + command.compute.alias.identity
			emission_queue.append(command.compute)
		emit_string += ';'
	emit_string += '"\n'
	for compute in emission_queue:
		emit_string += emit(compute, uni)
	return emit_string

def is_normalized(compute):
	return len(compute.commands) == 1 and (universe.is_alias(compute.commands[0]) or universe.is_source_command(compute.commands[0]))

def is_alias_normalization(compute):
	return len(compute.commands) == 1 and universe.is_alias(compute.commands[0])
