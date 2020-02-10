"""
EBNF

block = { variable | assignment}
type = core_type , word_size
access = ( 'private' | 'public' )
variable = type vname '=' literal
assignment = vname '=' exp
exp = ( p_exp | exp binop exp | unop exp | value)
p_exp = '(' exp ')'
binop = '=' | '|' | '&'
unop = '~'

"""

import re


class block():
	family = 'block'
	identity = 'block'

	def __init__(self):
		self.scope = list()
		self.sequence = list()

class variable():
	family = 'variable'
	identity = 'variable'
	name = ''
	type = ''
	value = ''
	word_size = ''

class unary_operator():
	family = 'unary'
	identity = ''
	arg1 = ''
	output = ''

class binary_operator():
	family = 'binary'
	identity = ''
	arg1 = ''
	arg2 = ''
	output = ''
	is_literal = False

class assignment():
	family = 'assignment'
	identity = 'assignment'
	write = ''
	evaluate = ''

class parser_obj():

	def __init__(self, tokens):
		self.tokens = tokens
		self.count = 0

	def token(self, lookahead = 0):
		if self.count + lookahead >= len(self.tokens):
			return ''
		else:
			return self.tokens[self.count + lookahead].value

	def current_line(self):
		return self.tokens[self.count].line

	def consume_token(self, verify_token = None):
		if verify_token is not None and self.token() != verify_token:
			parsing_error(parser)
		elif self.count >= len(self.tokens):
			parsing_error(parser)
		else:
			self.count += 1

	def token_is_name(self):
		return self.token()[0].isalpha()

	def token_is_numeric(self):
		if self.token()[0] == '-':
			return self.token()[1:].isnumeric()
		else:
			return self.token().isnumeric()

	def token_is_value(self):
		return self.token_is_name() or self.token_is_numeric()

	def is_variable_declaration(self):
		return self.token(2) == '='

	def is_not_end_block(self):
		return self.token() != '}'

	def is_variable_assignment(self):
		return self.token(1) == '='

	def is_subexpression(self):
		return self.token() == '('

	def is_unchained_value(self):
		return self.token_is_value() and not self.is_binop(1)

	def is_unop(self, lookahead=0):
		ops = ['~']
		return self.token(lookahead) in ops

	def is_binop(self, lookahead=0):
		ops = ['|', '&']
		return self.token(lookahead) in ops

	def retrieve_identity(self):
		identity_map = {
		'~' : 'bitwise_neg',
		'|' : 'bitwise_or',
		'&' : 'bitwise_and'
		}
		return identity_map[self.token()]


#parser logic

def parse(tokens):
	parser = parser_obj(tokens)
	return global_context(parser)

def parsing_error(parser):
	raise Exception('did not expect token # ' + str(parser.count) + ' : """' + parser.token() + '""" at line ' + str(parser.current_line()))

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
		else:
			parsing_error(parser)
	return new_block


def expect_assignment(parser):
	new_assignment = assignment()
	new_assignment.write = expect_assignment_write(parser)
	new_assignment.evaluate = expect_assignment_evaluate(parser)
	return new_assignment

def expect_assignment_write(parser):
	if parser.token_is_name():
		write = parser.token()
		parser.consume_token()
		parser.consume_token('=')
		return write
	else:
		parsing_error(parser)

def expect_assignment_evaluate(parser):
	return expect_expression(parser)


def expect_p_expression(parser):
	parser.consume_token('(')
	new_expression = expect_expression(parser)
	parser.consume_token(')')
	return new_expression

def expect_expression(parser):
	new_expression = ''

	if parser.is_unop():
		new_expression = expect_unop(parser)

	elif parser.is_subexpression():
		new_expression = expect_p_expression(parser)

	elif parser.is_unchained_value():
		new_expression = parser.token()
		parser.consume_token()

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
		parser.consume_token()
	else:
		parsing_error(parser)
	return arg

def expect_unop(parser):
	new_unop = unary_operator()
	new_unop.identity = parser.retrieve_identity()
	parser.consume_token()
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
		parser.consume_token()
	else:
		parsing_error(parser)
	new_binop.arg2 = expect_argument(parser)
	return new_binop


def expect_variable(parser):
	new_variable = variable()
	new_variable.type, new_variable.word_size = expect_type(parser)
	new_variable.name = expect_name(parser)
	new_variable.value = expect_literal_source(parser)
	return new_variable


def expect_type(parser):
	if parser.token_is_name():
		parsed_type = list(filter(lambda x: x != '', re.split('(\d)', parser.token())))
		if len(parsed_type) == 2:
			type = parsed_type[0]
			word_size = parsed_type[1]
			parser.consume_token()
			return type, word_size
		else:
			parsing_error(parser)
	else:
		parsing_error(parser)

def expect_name(parser):
	if parser.token_is_name():
		name = parser.token()
		parser.consume_token()
		return name
	else:
		parsing_error(parser)

def expect_literal_source(parser):
	parser.consume_token() #we know this is the identifier token
	if parser.token_is_numeric():
		is_literal = True
		source = parser.token()
		parser.consume_token()
		return source
	else:
		parsing_error(parser)


