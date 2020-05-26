"""
EBNF

sandbox = 'sandbox ' sname { bind_block | map_block | service_block }
service_block = 'service' sname service_args '{' script_block '}'
script_block = { statement }
bind_block = '{' { key ':' event } '}'
map_block = '{' { event ':' service_call } '}'
statement = assignment | service_call
service_call = ename service_args
assignment = vname '=' exp
service_args = '(' { vname [,] } ')'
exp = ( p_exp | exp binop exp | unop exp | value)
p_exp = '(' exp ')'
binop = '=' | '|' | '&'
unop = '~'

"""
from model.structure import *
import re

def parse(tokens):
	consumer_obj = consumer(tokens)
	return global_context(consumer_obj)


def global_context(consumer):
	new_global_object = global_object()
	while consumer.is_sandbox():
		new_sandbox = expect_sandbox(consumer)
		new_global_object.sandbox.append(new_sandbox)
	if consumer.token() == '':
		return new_global_object
	else:
		parsing_error(consumer)


def expect_sandbox(consumer):
	new_sandbox = sandbox()
	consumer.current_sandbox = new_sandbox #this lets us cheat and see the resolution of the sandbox without passing the sandbox as a argument
	consumer.consume('sandbox')
	new_sandbox.name = consumer.use_if_name()
	while consumer.is_block():
		block_type = consumer.token()
		if block_type == 'service':
			new_block = expect_service_block(consumer)
			new_sandbox.service.append(new_block)
		elif block_type == 'map':
			new_block = expect_map_block(consumer)
			new_sandbox.map.append(new_block)
		elif block_type == 'bind':
			new_block = expect_bind_block(consumer)
			new_sandbox.bind.append(new_block)
		else:
			parsing_error(consumer)
	return new_sandbox



def expect_bind_block(consumer):
	new_binding = binding()
	consumer.consume('bind')
	consumer.consume('{')
	while consumer.is_not_end_block():
		new_key = key(consumer.token())
		consumer.consume()
		consumer.consume(':')
		new_event = event(consumer.token())
		consumer.consume()
		new_binding.map[new_key] = new_event
	consumer.consume('}')
	return new_binding

def expect_map_block(consumer):
	new_mapping = mapping()
	consumer.consume('map')
	consumer.consume('{')
	while consumer.is_not_end_block():
		event_string = consumer.token()
		consumer.consume()
		consumer.consume(':')
		service_call = expect_service_call(consumer)
		new_mapping.map[event_string] = service_call
	consumer.consume('}')
	return new_mapping


def expect_service_block(consumer):
	new_block = service()
	consumer.consume('service')
	new_block.name = consumer.use_if_name()
	new_block.arg = expect_service_header(consumer)
	consumer.consume('{')
	while consumer.is_not_end_block():
		if consumer.is_variable_assignment():
			new_assignment = expect_assignment(consumer)
			new_block.sequence.append(new_assignment)
		elif consumer.is_service_call():
			new_service_call = expect_service_call(consumer)
			new_block.sequence.append(new_service_call)
		else:
			parsing_error(consumer)
	consumer.consume('}')
	return new_block


def expect_service_call(consumer):
	new_service_call = service_call()
	new_service_call.identifier = consumer.use_if_name()
	new_service_call.arg = expect_service_header(consumer)
	return new_service_call

def expect_service_header(consumer):
	args = list()
	consumer.consume('(')
	while consumer.is_not_end_service_arg():
		arg = expect_expression(consumer)
		args.append(arg)
		if consumer.is_not_end_service_arg() and consumer.token() == ',':
			consumer.consume(',')
	consumer.consume(')')
	return args


def expect_assignment(consumer):
	new_assignment = assignment()
	new_assignment.identifier = expect_assignment_identifier(consumer)
	consumer.consume('=')
	new_assignment.arg[0] = expect_expression(consumer)
	return new_assignment


def expect_assignment_identifier(consumer):
	identifier = consumer.use_if_name()
	res = consumer.current_sandbox.resolution
	if identifier in res.variable_lookup:
		return res.variable_lookup[identifier]
	else:
		new_variable = variable(identifier)
		res.variable_lookup[identifier] = new_variable
		return new_variable


def expect_p_expression(consumer):
	consumer.consume('(')
	new_expression = expect_expression(consumer)
	consumer.consume(')')
	return new_expression

def expect_expression_atomic(consumer):
	if consumer.is_unop():
		return expect_unop(consumer)
	elif consumer.is_subexpression():
		return expect_p_expression(consumer)
	elif consumer.is_literal_value():
		return expect_literal_value(consumer)
	else:
		parsing_error(consumer)

def expect_expression(consumer):
	new_expression = expect_expression_atomic(consumer)
	if consumer.is_binop():
		new_expression = expect_binop(consumer, new_expression)
	return new_expression


def expect_literal_value(consumer):
	new_literal_value = literal_value()
	new_literal_value.arg[0] = expect_value(consumer)
	return new_literal_value


def expect_value(consumer):
	value = consumer.token()
	consumer.consume()
	res = consumer.current_sandbox.resolution
	if value in res.variable_lookup:
		return res.variable_lookup[value]
	elif token_is_numeric(value):
		if value in res.constant_lookup:
			return res.constant_lookup[value]
		else:
			new_constant = constant(value)
			res.constant_lookup[value] = new_constant
			return new_constant
	else:
		parsing_error(consumer)


def expect_unop(consumer):
	new_unop = unary_operator()
	new_unop.identity = consumer.retrieve_and_use_unary_identity()
	new_unop.arg[0] = expect_expression(consumer)
	return new_unop


def expect_binop(consumer, chain):
	new_binop = binary_operator()
	new_binop.arg[0] = chain
	new_binop.identity = consumer.retrieve_and_use_binary_identity()
	new_binop.arg[1] = expect_expression(consumer)
	return new_binop


