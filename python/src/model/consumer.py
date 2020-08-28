import src.frontend.utility.utility as utility

def parsing_error(parser):
	raise Exception('did not expect token # ' + str(parser.count) + ' : """' + parser.token() + '""" at line ' + str(parser.current_line()))

class consumer():

	def __init__(self, tokens):
		self.current_sandbox = None
		self.global_object = None
		self.tokens = tokens
		self.count = 0
		self.binary_symbol_map = {
		'|' : 'bitwise_or',
		'&' : 'bitwise_and'
		}
		self.unary_symbol_map = {
		'!' : 'bitwise_neg',
		'?' : 'binary_print'
		}
		self.conditional_symbol_map = {
		'==' : 'equality',
		'!=' : 'inequality'
		}

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

	def maybe_consume(self, maybe_token):
			if maybe_token == self.token():
				consume(maybe_token)

	def token_is_name(self):
		return utility.token_is_name(self.token())

	def token_is_numeric(self):
		return utility.token_is_numeric(self.token())

	def token_is_value(self):
		return self.token_is_name() or self.token_is_numeric()

	def use_if_name(self):
		if self.token_is_name():
			token_s = self.token()
			self.consume()
			return token_s
		else:
			parsing_error(self)

	def is_variable_assignment(self):
		return self.token(1) == '='

	def is_service_call(self):
		return self.token() == '@'

	def is_else(self):
		return self.token() == 'else'

	def is_source_call(self):
		return self.token() == '['

	def is_begin_block(self):
		return self.token() == '{'

	def is_not_end_block(self):
		return self.token() != '}'

	def is_not_end_service_arg(self):
		return self.token() != ')'

	def is_sandbox(self):
		return self.token() == 'sandbox'

	def is_if(self):
		return self.token() == 'if'

	def is_block(self):
		block_types = ('service', 'map', 'bind', 'file')
		return self.token() in block_types

	def is_subexpression(self):
		return self.token() == '('

	def is_literal_value(self):
		return self.token_is_value()

	def is_unop(self, lookahead=0):
		return self.token(lookahead) in self.unary_symbol_map

	def is_binop(self, lookahead=0):
		return self.token(lookahead) in self.binary_symbol_map

	def retrieve_and_use_binary_identity(self):
		token = self.token()
		if token in self.binary_symbol_map:
			self.consume()
			return self.binary_symbol_map[token]
		else:
			parsing_error(self)

	def retrieve_and_use_unary_identity(self):
		token = self.token()
		if token in self.unary_symbol_map:
			self.consume()
			return self.unary_symbol_map[token]
		else:
			parsing_error(self)

	def retrieve_and_use_conditional(self):
		token = self.token()
		if token in self.conditional_symbol_map:
			self.consume()
			return self.conditional_symbol_map[token]
		else:
			parsing_error(self)
