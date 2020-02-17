


def parsing_error(parser):
	raise Exception('did not expect token # ' + str(parser.count) + ' : """' + parser.token() + '""" at line ' + str(parser.current_line()))



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

class service_call():
	family = 'service_call'
	identity = 'service_call'
	service = ''

	def __init__(self):
		self.args = list()


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

class assignment():
	family = 'assignment'
	identity = 'assignment'
	write = ''
	evaluate = ''

class parser_obj():

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
		return self.token()[0].isalpha()

	def token_is_numeric(self):
		if self.token()[0] == '-':
			return self.token()[1:].isnumeric()
		else:
			return self.token().isnumeric()

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

	def is_variable_declaration(self):
		return self.token(2) == '='

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
