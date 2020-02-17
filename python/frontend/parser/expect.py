"""
EBNF

block = { variable | assignment | service_call }
type = core_type , word_size
access = ( 'private' | 'public' )
variable = type vname '=' literal
service_call = ename '(' { vname [,]} ')'
assignment = vname '=' exp
exp = ( p_exp | exp binop exp | unop exp | value)
p_exp = '(' exp ')'
binop = '=' | '|' | '&'
unop = '~'

"""
from frontend.parser.structure import *
import re
#parser logic

def parse(tokens):
	parser = parser_obj(tokens)
	return global_context(parser)



def global_context(parser):
	global_object = expect_block(parser)
	return global_object


#definitions

def expect_block(parser):
	new_block = block()
	while parser.is_not_end_block():
		if parser.is_variable_declaration():
			new_variable = expect_variable(parser)
			new_block.sequence.append(new_variable)
		elif parser.is_variable_assignment():
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
		new_service_call.args.append(arg)
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
	new_unop.arg1 = expect_argument(parser)
	return new_unop

def expect_binop(parser, chain=None):
	new_binop = binary_operator()
	if chain is None:
		new_binop.arg1 = expect_argument(parser)
	else:
		new_binop.arg1 = chain
	if parser.is_binop():
		new_binop.identity = parser.retrieve_identity()
		parser.consume()
	else:
		parsing_error(parser)
	new_binop.arg2 = expect_argument(parser)
	return new_binop


def expect_variable(parser):
	new_variable = variable()
	new_variable.type, new_variable.word_size = expect_type(parser)
	new_variable.name = parser.use_if_name()
	new_variable.value = expect_declaration_literal(parser)
	return new_variable


def expect_type(parser):
	if parser.token_is_name():
		parsed_type = list(filter(lambda x: x != '', re.split('(\d)', parser.token())))
		if len(parsed_type) == 2:
			ptype = parsed_type[0]
			word_size = parsed_type[1]
			parser.consume()
			return ptype, word_size
		else:
			parsing_error(parser)
	else:
		parsing_error(parser)

def expect_declaration_literal(parser):
	parser.consume('=')
	if parser.token_is_numeric():
		literal = parser.token()
		parser.consume()
		return literal
	else:
		parsing_error(parser)


