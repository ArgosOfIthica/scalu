
from frontend.utility.utility import *

def parsing_error(parser):
	raise Exception('did not expect token # ' + str(parser.count) + ' : """' + parser.token() + '""" at line ' + str(parser.current_line()))



class structure():

	def is_assignment(self, arg):
		return isinstance(arg, assignment)

	def is_service_call(self, arg):
		return isinstance(arg, service_call)

	def is_operator(self, arg):
		return isinstance(arg, operator)

	def is_unary_operator(self, arg):
		return isinstance(arg, unary_operator)

	def is_binary_operator(self, arg):
		return isinstance(arg, binary_operator)

	def is_variable(self, arg):
		return isinstance(arg, variable)

	def is_constant(self, arg):
		return isinstance(arg, constant)

class block():

	def __init__(self):
		self.scope = list()
		self.sequence = list()

class variable():
	name = ''
	type = 'int'
	value = '0'
	word_size = '8'



class service():
	name = ''

	def __init__(self):
		self.arg = list()

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



class consumer():

	def __init__(self, tokens):
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

	def is_not_end_service_call(self):
		return self.token() != ')'

	#expression functions

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
