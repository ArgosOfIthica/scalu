from backend.definitions.vbuilder import build_variable
from backend.definitions.global_builder import *
from backend.alias import *



def compile(global_object):
	header = build_header(global_object)
	build_bindings(global_object, header)
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
	return global_object


def build_header(global_object):
	uni = global_object.universe
	header = uni.add_computation('header')
	for sandbox in global_object.sandbox:
		for service in sandbox.service:
			service_compute = build_service(global_object, service)
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


def build_service(global_object, service):
	uni = global_object.universe
	service_compute = uni.add_computation('service')
	for statement in service.sequence:
		build_statement(global_object, service_compute, statement)
	return service_compute



def build_statement(global_object, compute, statement):
	print(statement.identity)
	print('###' + statement.output.name)
	for arg in statement.arg:
		print(arg.name)







