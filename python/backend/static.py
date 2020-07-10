from backend.definitions.vbuilder import build_variable
from backend.definitions.global_builder import *
from backend.alias import *
from backend.definitions.instruction import handle_instruction



def compile(global_object):
	header = build_header(global_object)
	build_bindings(global_object, header)
	unwrap_compute(header, '')
	'''
	for event in global_object.map:
		header += generate_mapping(event.value, global_object.map[event]) + '\n'
	for sandbox in global_object.sandbox:
		res = sandbox.resolution
		for var_name in res.variable_lookup:
			var = res.variable_lookup[var_name]
			header += build_variable(var.name, var.word_size, var.value)
		for const_name in res.constant_lookup:
			const = res.constant_lookup[const_name]
			header += build_variable(const.name, const.word_size, const.value)
		return header
		'''
	return header


def build_header(global_object):
	uni = global_object.universe
	header = uni.add_computation('header')
	for sandbox in global_object.sandbox:
		for service in sandbox.service:
			service_compute = build_service(global_object, service, header)
			find_event(global_object, service)
	return header


def find_event(global_object, service):
	for key in global_object.map:
		pass
		#if service.name in global_object:
		#	pass

def build_bindings(global_object, header):
	uni = global_object.universe
	for key in global_object.bind:
		new_event = uni.add_alias('event')
		new_bind = bind(key.value, new_event)
		header.extend(new_bind)


def build_events(global_object, header):
	for event in global_object.map:
		new_


def build_service(global_object, service, header):
	uni = global_object.universe
	service_compute = uni.extend_add_computation(header, 'service')
	for statement in service.sequence:
		handle_instruction(global_object, service_compute, statement)
	return service_compute


def unwrap_compute(compute, indentation):
	if isinstance(compute, computation):
		print(indentation + compute.alias.string + ' : ' + compute.alias.type)
		for command in compute.commands:
			unwrap_compute(command, indentation + ' ')
	elif isinstance(compute, alias):
		print(indentation + 'ALIAS -> ' + compute.string + ' : ' + compute.type)
	else:
		print(indentation + str(compute))



