
from frontend.utility.utility import *

def parsing_error(parser):
	raise Exception('did not expect token # ' + str(parser.count) + ' : """' + parser.token() + '""" at line ' + str(parser.current_line()))

def is_assignment(arg):
	return isinstance(arg, assignment)

def is_service_call(arg):
	return isinstance(arg, service_call)

def is_operator(arg):
	return isinstance(arg, operator)

def is_unary_operator(arg):
	return isinstance(arg, unary_operator)

def is_binary_operator(arg):
	return isinstance(arg, binary_operator)

def is_variable(arg):
	return isinstance(arg, variable)

def is_constant(arg):
	return isinstance(arg, constant)

class global_object():

	def __init__(self):
		self.sandbox = list()

class resolution_block():
	variable_lookup = dict()
	service_lookup = dict()
	constant_lookup = dict()

class sandbox():

	def __init__(self):
		self.name = ''
		self.resolution = resolution_block()
		self.service = list()
		self.bind = list()
		self.map = list()

class block():
	pass

class variable():

	def __init__(self, value='0'):
		self.name = ''
		self.type = 'int'
		self.value = value
		self.word_size = '8'



class service():
	name = ''

	def __init__(self):
		self.arg = list()
		self.sequence = list()

class config():

	def __init__(self):
		self.map = dict()

class binding(config):
	pass

class mapping(config):
	pass


class event():

	def __init__(self, event):
		self.value = event


class key():

	def __init__(self, key):
		self.value = key

class constant(variable):
	pass

class statement():
	identifier = ''

	def __init__(self):
		self.arg = list()

class assignment(statement):

	def __init__(self):
		self.arg = [None]

class service_call(statement):
	pass


class operator():
	identity = ''
	output = ''
	arg = list()

class unary_operator(operator):

	def __init__(self):
		self.arg = [None]

class binary_operator(operator):

	def __init__(self):
		self.arg =  [None] * 2

class literal_value(operator):

	def __init__(self):
		self.identity = 'literal'
		self.arg = [None]


class consumer():

	def __init__(self, tokens):
		self.current_sandbox = ''
		self.tokens = tokens
		self.count = 0


	#token functions

	def token(self, lookahead = 0):
		if self.count + lookahead >= len(self.tokens):
			return ''
		else:
			return self.tokens[self.count + lookahead].value

	def current_line(self):
		return self.tokens[self.count].line

	def consume(self, verify_token = None):
		if verify_token is not None and self.token() != verify_token:
			parsing_error(self)
		elif self.count >= len(self.tokens):
			parsing_error(self)
		else:
			self.count += 1

	def token_is_name(self):
		return token_is_name(self.token())

	def token_is_numeric(self):
		return token_is_numeric(self.token())

	def token_is_value(self):
		return self.token_is_name() or self.token_is_numeric()

	def use_if_name(self):
		if self.token_is_name():
			token_s = self.token()
			self.consume()
			return token_s
		else:
			parsing_error(self)

	#statement lookaheads

	def is_variable_assignment(self):
		return self.token(1) == '='

	def is_service_call(self):
		return self.token_is_name() and self.token(1) == '('

	#look for end token

	def is_not_end_block(self):
		return self.token() != '}'

	def is_not_end_service_arg(self):
		return self.token() != ')'

	#

	def is_sandbox(self):
		return self.token() == 'sandbox'

	def is_block(self):
		block_types = ('service', 'map', 'bind')
		return self.token() in block_types


	#expression functions

	def is_subexpression(self):
		return self.token() == '('

	def is_literal_value(self):
		return self.token_is_value()

	def is_unop(self, lookahead=0):
		ops = ['~']
		return self.token(lookahead) in ops

	def is_binop(self, lookahead=0):
		ops = ['|', '&']
		return self.token(lookahead) in ops

	def retrieve_and_use_binary_identity(self):
		identity_map = {
		'|' : 'bitwise_or',
		'&' : 'bitwise_and'
		}
		token = self.token()
		if token in identity_map:
			self.consume()
			return identity_map[token]
		else:
			parsing_error(self)

	def retrieve_and_use_unary_identity(self):
		identity_map = {
		'~' : 'bitwise_neg'
		}
		token = self.token()
		if token in identity_map:
			self.consume()
			return identity_map[token]
		else:
			parsing_error(self)
