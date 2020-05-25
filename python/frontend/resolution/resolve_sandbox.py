
from frontend.utility.utility import *
import model.structure as s
import frontend.service_definitions.service as core


def resolve(sandbox):
	for service in sandbox.service:
		resolve_service(sandbox, service)
	return sandbox

def resolution_error():
	raise Exception("Resolution error")


def resolve_service(sandbox, service):
	for statement in service.sequence:
		if s.is_assignment(statement):
			pass
		elif s.is_service_call(statement):
			resolve_service_call(sandbox, statement)
		else:
			resolution_error()

def resolve_service_call(sandbox, call):
	call.identifier = resolve_service_call_write(sandbox, call.identifier)
	resolve_operator(call)

def resolve_service_call_write(sandbox, call_identifier):
	if call_identifier in core.core_service_list():
		return core.get_service_object(call_identifier)
	else:
		resolution_error()

def resolve_assignment(sandbox, assignment):
	assignment.identifier = resolve_assignment_identifier(sandbox, assignment.identifier)
	resolve_operator(assignment)

def resolve_assignment_identifier(sandbox, identifier):
	if identifier in sandbox.resolution.variable_lookup:
		return sandbox.variable_lookup[write]
	elif type(identifier) == str:
		new_variable = variable()
		new_variable.name = identifier
		sandbox.resolution.variable_lookup[identifier] = new_variable
		return new_variable
	else:
		resolution_error()

def resolve_operator(operator):
	operator.arg = [resolve_operator_transform(arg) for arg in operator.arg]

def resolve_operator_transform(arg):
	if type(arg) is str:
		return resolve_value(arg)
	elif s.is_operator(arg):
		resolve_operator(arg)
		return arg
	else:
		print(arg)
		resolution_error()

def resolve_value(token_string):
	if token_is_name(token_string):
		return res.variable_lookup[token_string]
	elif token_is_numeric(token_string):
		if token_string in res.constant_lookup:
			return res.constant_lookup[token_string]
		else:
			new_constant = generate_constant(token_string)
			res.constant_lookup[token_string] = new_constant
			return new_constant


def generate_constant(value):
	constant_val = constant()
	constant_val.identity = 'constant'
	constant_val.name = value
	constant_val.value = value
	return constant_val
