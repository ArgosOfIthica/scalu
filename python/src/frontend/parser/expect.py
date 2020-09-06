import src.model.structure as model
import src.frontend.utility.utility as utility
import src.model.consumer as consume
import re

def parse(tokens):
	consumer_obj =  consume.consumer(tokens)
	return global_context(consumer_obj)


def global_context(consumer):
	new_global_object = model.global_object()
	consumer.global_object = new_global_object
	while consumer.is_sandbox():
		new_sandbox = expect_sandbox(consumer)
		new_global_object.sandbox.append(new_sandbox)
	if consumer.token() == '':
		new_global_object.resolve()
		return new_global_object
	else:
		consume.parsing_error(consumer)


def expect_sandbox(consumer):
	new_sandbox = model.sandbox()
	consumer.current_sandbox = new_sandbox #this lets us cheat and
	#see the resolution of the sandbox without passing the sandbox as a argument
	consumer.consume('sandbox')
	new_sandbox.name = consumer.use_if_name()
	while consumer.is_block():
		block_type = consumer.token()
		if block_type == 'service':
			new_block = expect_service_block(consumer)
		elif block_type == 'map':
			new_block = expect_map_block(consumer)
		elif block_type == 'bind':
			new_block = expect_bind_block(consumer)
		elif block_type == 'file':
			new_block = expect_file_block(consumer)
		else:
			consume.parsing_error(consumer, 'invalid block type error')
	return new_sandbox


def expect_bind_block(consumer):
	binding = consumer.global_object.maps
	consumer.consume('bind')
	consumer.consume('{')
	while consumer.is_not_end_block():
		new_key = consumer.token()
		consumer.consume()
		consumer.consume(':')
		new_event = model.event(consumer.token())
		consumer.consume()
		new_event.add_key(new_key)
		binding.add(new_event)
	consumer.consume('}')
	return binding

def expect_map_block(consumer):
	mapping = consumer.global_object.maps
	consumer.consume('map')
	consumer.consume('{')
	while consumer.is_not_end_block():
		new_event = model.event(consumer.token())
		consumer.consume()
		consumer.consume(':')
		call = expect_call(consumer)
		new_event.services.append(call)
		mapping.add(new_event)
	consumer.consume('}')
	return mapping

def expect_file_block(consumer):
	file_map = consumer.global_object.maps
	consumer.consume('file')
	consumer.consume('{')
	while consumer.is_not_end_block():
		new_file = consumer.token()
		consumer.consume()
		consumer.consume(':')
		new_event = model.event(consumer.token())
		consumer.consume()
		new_event.add_file(new_file)
		file_map.add(new_event)
	consumer.consume('}')
	return file_map

def expect_service_block(consumer, named=True):
	new_block = model.service()
	if named == True:
		consumer.consume('service')
		new_block.name = consumer.use_if_name()
	else:
		new_block.name = ''
		new_block.is_anonymous = True
	consumer.consume('{')
	while consumer.is_not_end_block():
		if consumer.is_variable_assignment():
			new_assignment = expect_assignment(consumer)
			new_block.sequence.append(new_assignment)
		elif consumer.is_service_call():
			new_service_call = expect_service_call(consumer)
			new_block.sequence.append(new_service_call)
		elif consumer.is_source_call():
			new_source_call = expect_source_call(consumer)
			new_block.sequence.append(new_source_call)
		elif consumer.is_if():
			new_if = expect_if(consumer)
			new_block.sequence.append(new_if)
		else:
			consume.parsing_error(consumer, 'invalid statement error')
	consumer.consume('}')
	consumer.current_sandbox.services.append(new_block)
	return new_block

def empty_service(consumer):
	new_block = model.service()
	new_block.name = ''
	new_block.is_anonymous = True
	consumer.current_sandbox.services.append(new_block)
	return new_block

def expect_if(consumer):
	new_if = model.if_statement()
	consumer.consume('if')
	if consumer.is_subexpression():
		consumer.consume('(')
		new_if.condition = expect_conditional(consumer)
		consumer.consume(')')
	else:
		new_if.condition = expect_conditional(consumer)
	new_if.true_service = expect_service_block(consumer, False)
	if consumer.is_else():
		consumer.consume('else')
		new_if.false_service = expect_service_block(consumer, False)
	else:
		new_if.false_service = empty_service(consumer)
	return new_if

def expect_call(consumer):
	if consumer.is_service_call():
		return expect_service_call(consumer)
	elif consumer.is_source_call():
		return expect_source_call(consumer)
	else:
		consume.parsing_error(consumer, 'invalid call error')

def expect_source_call(consumer):
	new_source_call = model.source_call()
	consumer.consume('[')
	new_source_call.arg[0] = consumer.token()
	new_source_call.identifier = '[' + consumer.token() + ']'
	consumer.consume()
	consumer.consume(']')
	return new_source_call

def expect_service_call(consumer):
	new_service_call = model.service_call(consumer.current_sandbox)
	consumer.consume('@')
	new_service_call.identifier = consumer.use_if_name()
	new_service_call.sandbox = consumer.current_sandbox
	return new_service_call


def expect_assignment(consumer):
	new_assignment = model.assignment()
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
		new_variable = model.variable(identifier)
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
	elif consumer.token_is_value():
		return expect_value(consumer)
	else:
		consume.parsing_error(consumer, 'invalid expression atomic error')

def expect_expression(consumer):
	new_expression = expect_expression_atomic(consumer)
	if consumer.is_binop():
		new_expression = expect_binop(consumer, new_expression)
	return new_expression

def expect_value(consumer):
	value = consumer.token()
	consumer.consume()
	res = consumer.current_sandbox.resolution
	if value in res.variable_lookup:
		return res.variable_lookup[value]
	elif utility.token_is_numeric(value):
		if value in res.constant_lookup:
			return res.constant_lookup[value]
		else:
			new_constant = model.constant(value)
			res.constant_lookup[value] = new_constant
			return new_constant
	else:
		consume.parsing_error(consumer, 'invalid variable error')

def expect_conditional(consumer):
	new_cond = model.conditional()
	new_cond.arg[0] = expect_value(consumer)
	new_cond.identity = consumer.retrieve_and_use_conditional()
	new_cond.arg[1] = expect_value(consumer)
	return new_cond


def expect_unop(consumer):
	new_unop = model.unary_operator()
	new_unop.identity = consumer.retrieve_and_use_unary_identity()
	new_unop.arg[0] = expect_expression(consumer)
	return new_unop


def expect_binop(consumer, chain):
	new_binop = model.binary_operator()
	new_binop.arg[0] = chain
	new_binop.identity = consumer.retrieve_and_use_binary_identity()
	new_binop.arg[1] = expect_expression(consumer)
	return new_binop


