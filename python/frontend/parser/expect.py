"""
EBNF

block = { variable | assignment | service_call }
service_call = ename '(' { vname [,]} ')'
assignment = vname '=' exp
exp = ( p_exp | exp binop exp | unop exp | value)
p_exp = '(' exp ')'
binop = '=' | '|' | '&'
unop = '~'

"""
from frontend.parser.structure import *
import re



def parse(tokens):
	parser = parser_obj(tokens)
	return global_context(parser)



def global_context(parser):
	global_object = expect_block(parser)
	return global_object


def expect_block(parser):
	new_block = block()
	while parser.is_not_end_block():
		if parser.is_variable_assignment():
			new_assignment = expect_assignment(parser)
			new_block.sequence.append(new_assignment)
		elif parser.is_service_call():
			new_service_call = expect_service_call(parser)
			new_block.sequence.append(new_service_call)
		else:
			parsing_error(parser)
	return new_block


def expect_service_call(parser):
	new_service_call = service_call()
	new_service_call.service = parser.use_if_name()
	parser.consume('(')
	while parser.is_not_end_service_call():
		arg = expect_expression(parser)
		new_service_call.arg.append(arg)
		if parser.is_not_end_service_call():
			parser.consume(',')
	parser.consume(')')
	return new_service_call



def expect_assignment(parser):
	new_assignment = assignment()
	new_assignment.write = expect_assignment_write(parser)
	new_assignment.evaluate = expect_expression(parser)
	return new_assignment

def expect_assignment_write(parser):
	write = parser.use_if_name()
	parser.consume('=')
	return write


def expect_p_expression(parser):
	parser.consume('(')
	new_expression = expect_expression(parser)
	parser.consume(')')
	return new_expression

def expect_expression(parser):
	new_expression = ''

	if parser.is_unop():
		new_expression = expect_unop(parser)

	elif parser.is_subexpression():
		new_expression = expect_p_expression(parser)

	elif parser.is_unchained_value():
		new_expression = parser.token()
		parser.consume()

	else:
		new_expression = expect_binop(parser)

	while parser.is_binop():
		new_expression = expect_binop(parser, new_expression)
		#this handles the case of binary "chaining" where order of operations is ambiguous.
		#the expression is nested into the first argument of a binary operation object.
		#this nesting produces left-to-right evaluation without operator precedence.


	return new_expression


def expect_argument(parser):
	arg = ''
	if parser.is_subexpression():
		arg = expect_p_expression(parser)
	elif parser.token_is_value():
		arg = parser.token()
		parser.consume()
	else:
		parsing_error(parser)
	return arg

def expect_unop(parser):
	new_unop = unary_operator()
	new_unop.identity = parser.retrieve_identity()
	parser.consume()
	new_unop.arg[0] = expect_argument(parser)
	return new_unop

def expect_binop(parser, chain=None):
	new_binop = binary_operator()
	if chain is None:
		new_binop.arg[0] = expect_argument(parser)
	else:
		new_binop.arg[0] = chain
	if parser.is_binop():
		new_binop.identity = parser.retrieve_identity()
		parser.consume()
	else:
		parsing_error(parser)
	new_binop.arg[1] = expect_argument(parser)
	return new_binop


