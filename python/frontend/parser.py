"""
EBNF


type = core_type word_size
access = ( 'private' | 'public' )
new_var = type vname '=' literal
new_assign = vname '=' value
block = { new_var | new_assign }
"""

import re


class block():
	identity = 'block'
	scope = list()
	sequence = list()

class variable():
	identity = 'variable'
	name = ''
	type = ''
	value = ''
	word_size = ''

class assignment():
	identity = 'assignment'
	source = ''
	destination = ''
	is_literal = False

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

	new_block = block()
	while is_not_end_block():
		if is_variable_declaration():
			new_variable = expect_variable(parser)
			block.sequence.append(new_variable)
		elif is_variable_assignment():
			new_assignment = expect_assignment(parser)
			block.sequence.append(new_assignment)
		else:
			parsing_error()
	parser.consume_token()
	return new_block

def expect_assignment(parser):
	new_assignment = assignment()
	new_assignment.destination = expect_destination(parser)
	new_assignment.is_literal, new_assignment.source = expect_source(parser)
	return new_assignment

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
	parser.consume_token() #we know this is '='
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
	parser.consume_token() #we know this is '='
	if parser.token_is_numeric():
		is_literal = True
		source = parser.token()
		parser.consume_token()
		return source
	else:
		parsing_error()
