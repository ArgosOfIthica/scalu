"""
EBNF

block = { variable | binop_statement }
type = core_type , word_size
access = ( 'private' | 'public' )
variable = type vname '=' literal
binop_statement = vname binop value
binop = '=' | '|' | '&' 

"""

import re


class block():
	family = 'block'
	identity = 'block'
	scope = list()
	sequence = list()

class variable():
	family = 'variable'
	identity = 'variable'
	name = ''
	type = ''
	value = ''
	word_size = ''

class binary_operator():
	family = 'binary'
	source = ''
	destination = ''
	is_literal = False

class assignment(binary_operator):
	identity = 'assignment'

class bitwise_or(binary_operator):
	identity = 'bitwise_or'

class bitwise_and(binary_operator):
	identity = 'bitwise_and'

class parser_obj():

	def __init__(self, tokens):
		self.tokens = tokens
		self.count = 0

	def token(self, lookahead = 0):
		if self.count + lookahead >= len(self.tokens):
			raise Exception('unexpected end of token stream')
		else:
			return self.tokens[self.count + lookahead].value

	def current_line(self):
		return self.tokens[count].line
	
	def consume_token(self):
		self.count += 1
	
	def token_is_name(self):
		return self.token()[0].isalpha()

	def token_is_numeric(self):
		if self.token()[0] == '-': #TODO: NOT TESTED
			return self.token()[1:].isnumeric()
		else:
			return self.token().isnumeric()

#parser logic

def parse(tokens):
	parser = parser_obj(tokens)
	return global_context(parser)

def parsing_error(parser):
	raise Exception('did not expect token # ' + str(parser.count) + ' : """' + parser.token() + '""" at line ' + str(parser.current_line()))

def global_context(parser):
	global_object = expect_block(parser)
	return global_object

def expect_block(parser):
	def is_variable_declaration():
		return parser.token(2) == '='
	def is_not_end_block():
		return parser.token() != '}'
	def is_variable_assignment():
		return parser.token(1) == '='
	def is_bitwise_or():
		return parser.token(1) == '|'
	def is_bitwise_and():
		return parser.token(1) == '&'

	new_block = block()
	while is_not_end_block():
		if is_variable_declaration():
			new_variable = expect_variable(parser)
			block.sequence.append(new_variable)
		elif is_variable_assignment():
			new_assignment = expect_binary_operator(parser, assignment)
			block.sequence.append(new_assignment)
		elif is_bitwise_or():
			new_bitwise_or = expect_binary_operator(parser, bitwise_or)
			block.sequence.append(new_bitwise_or)
		elif is_bitwise_and():
			new_bitwise_and = expect_binary_operator(parser, bitwise_and)
			block.sequence.append(new_bitwise_and)
		else:
			parsing_error()
	parser.consume_token()
	return new_block


def expect_binary_operator(parser, op):
	new_operator = op()
	new_operator.destination = expect_destination(parser)
	new_operator.is_literal, new_operator.source = expect_source(parser)
	return new_operator

def expect_variable(parser):
	new_variable = variable()
	new_variable.type, new_variable.word_size = expect_type(parser)
	new_variable.name = expect_destination(parser)
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
			parsing_error()
	else:
		parsing_error()

def expect_destination(parser):
	if parser.token_is_name():
		destination = parser.token()
		parser.consume_token()
		return destination
	else:
		parsing_error()

def expect_source(parser):
	parser.consume_token() #we know this is the identifier token
	if parser.token_is_numeric():
		is_literal = True
		source = parser.token()
		parser.consume_token()
		return is_literal, source
	elif parser.token_is_name():
		is_literal = False
		source = parser.token()
		parser.consume_token()
		return is_literal, source
	else:
		parsing_error()

def expect_literal_source(parser):
	parser.consume_token() #we know this is the identifier token
	if parser.token_is_numeric():
		is_literal = True
		source = parser.token()
		parser.consume_token()
		return source
	else:
		parsing_error()
