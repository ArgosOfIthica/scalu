import src.backend.model.universe as model
import src.backend.instructions.instruction as instr_handler
import src.model.structure as structure



def compile(global_object):
	build_services(global_object)
	build_events(global_object)
	uni = build_bindings(global_object)
	return uni


def build_services(global_object):
	uni = global_object.universe
	for sandbox in global_object.sandbox:
		for service in sandbox.service:
			prebuild_service(global_object, service)
		for service in sandbox.service:
			compute = uni.constructs[service]
			compute = build_service(global_object, service, compute)


def build_bindings(global_object):
	uni = global_object.universe
	for key in global_object.bind:
		bind_def = uni.new_def('bind')
		uni.constructs[key] = bind_def
		exclusive_event = uni.constructs[global_object.bind[key]]
		new_bind = model.bind(key.value, exclusive_event)
		bind_def.extend(new_bind)
		uni.root.extend(bind_def.alias)
	return uni

def build_events(global_object):
	uni = global_object.universe
	for event in global_object.map:
		event_def = uni.new_def('event')
		uni.constructs[event] = event_def
		for service_call in global_object.map[event]:
			if structure.is_source_call(service_call):
				new_source_command = model.source_command(service_call.arg[0])
				event_def.extend(new_source_command)
			else:
				event_def.extend(uni.constructs[service_call.identifier].alias)

def prebuild_service(global_object, service):
	uni = global_object.universe
	service_def = uni.new_def('service')
	uni.constructs[service] = service_def
	return service_def


def build_service(global_object, service, definition):
	uni = global_object.universe
	for statement in service.sequence:
		if structure.is_source_call(statement):
			new_source_command = model.source_command(statement.arg[0])
			definition.extend(new_source_command)
		elif structure.is_service_call(statement):
			call_compute = uni.constructs[statement.identifier]
			definition.extend(call_compute.alias)
		elif structure.is_operator(statement):
			instr_handler.handle_instruction(global_object, definition, statement)
		elif structure.is_if_statement(statement):
			instr_handler.handle_conditional(global_object, definition, statement)
		else:
			raise Exception('bad statement')
	return definition



