"""
EBNF

access = ( 'private' | 'public' )
new_var = type vname '=' value
new_assign = vname '=' value
block = { new_var | new_assign }
"""


def parsing(tokens):


#parsing structures

	class block():
		identity = 'block'
		scope = list()
		sequence = list()

	class variable():
		identity = 'variable'
		name = ''
		type = ''
		value = ''
		is_literal = False

	class assignment():
		identity = 'assignment'
		source = ''
		destination = ''
		is_literal = False

#token handling

	count = 0
	def current_token(lookahead=0):
		if count + lookahead >= len(tokens):
			raise Exception('unexpected end of token stream')
		else:
			return tokens[count + lookahead].value

	def current_token_line():
		return tokens[count].line

	def consume_token():
		nonlocal count
		count += 1

	def token_is_name(token):
		return token[0].isalpha()

	def token_is_numeric(token):
		return token.isnumeric()


#parser logic

	def parsing_error():
		raise Exception('did not expect token # ' + str(count) + ' : """' + current_token() + '""" at line ' + str(current_token_line()))

	def new_block():
		def is_variable_declaration():
			return current_token(2) == '='
		def is_not_end_block():
			return current_token() != '}'
		def is_variable_assignment():
			return current_token(1) == '='

		new_cblock = block()
		while is_not_end_block():
			if is_variable_declaration():
				new_variable = new_var()
				block.sequence.append(new_variable)
			elif is_variable_assignment():
				new_assignment = new_assign()
				block.sequence.append(new_assignment)
			else:
				parsing_error()
		consume_token()
		return new_cblock

	def new_assign():
		new_assignment = assignment()
		if token_is_name(current_token()):
			new_assignment.destination = current_token()
			consume_token()
			consume_token() #we know this is '='
			if token_is_numeric(current_token()):
				new_assignment.is_literal = True
			new_assignment.value = current_token()
			consume_token()
		else:
			parsing_error()
		return new_assignment

	def new_var():
		new_variable = variable()
		if token_is_name(current_token()):
			new_variable.type = current_token()
			consume_token()
			if token_is_name(current_token()):
				new_variable.name = current_token()
				consume_token()
				consume_token() #we know this is '='
				if token_is_numeric(current_token()):
					new_variable.is_literal = True
				new_variable.value = current_token()
				consume_token()
			else:
				parsing_error()
		else:
			parsing_error()
		return new_variable
	
	def global_context():
		global_object = new_block()
		return global_object
	
	return global_context()