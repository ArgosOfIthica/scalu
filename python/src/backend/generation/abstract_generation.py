import src.backend.model.universe as model
import src.backend.instructions.instruction as instr_handler
import src.model.structure as structure



def compile(global_object):
	build_services(global_object)
	build_events(global_object)
	header = build_bindings(global_object)
	return header


def build_services(global_object):
	uni = global_object.universe
	for sandbox in global_object.sandbox:
		for service in sandbox.service:
			service_compute = build_service(global_object, service)
			uni.constructs[service] = service_compute


def build_bindings(global_object):
	uni = global_object.universe
	header = uni.add_computation('header')
	for key in global_object.bind:
		bind_compute = uni.extend_add_computation(header, 'bind')
		exclusive_event = uni.constructs[global_object.bind[key]]
		new_bind = model.bind(key.value, exclusive_event)
		bind_compute.extend(new_bind)
	return header

def build_events(global_object):
	uni = global_object.universe
	for event in global_object.map:
		event_compute = uni.add_computation('event')
		uni.constructs[event] = event_compute
		for service_call in global_object.map[event]:
			if structure.is_source_call(service_call):
				new_commands = create_source_command(uni, service_call)
				event_compute.extend(new_commands)
			else:
				event_compute.extend(uni.constructs[service_call.identifier])

def create_source_command(uni, source_call):
	source_computation = uni.add_computation('source')
	new_source_command = model.source_command(source_call.arg[0])
	source_computation.extend(new_source_command)
	return source_computation


def build_service(global_object, service):
	uni = global_object.universe
	service_compute = uni.add_computation('service')
	for statement in service.sequence:
		instr_handler.handle_instruction(global_object, service_compute, statement)
	return service_compute


def unwrap_compute(compute, indentation):
	if model.is_computation(compute):
		print(indentation + compute.alias.string + ' : ' + compute.alias.type)
		for command in compute.commands:
			unwrap_compute(command, indentation + ' ')
	elif model.is_alias(compute):
		print(indentation + 'ALIAS -> ' + compute.string + ' : ' + compute.type)
	else:
		print(indentation + str(compute))



