import re

def tokenize(program):
	split_program = re.split('(\W)', program)
	tokens = to_tokens(split_program)
	tokens = filter_empty_tokens(tokens)
	for token in tokens:
		token.value = token.value.lower()
	return tokens

class token():

	def __init__(self, value, line):
		self.value = value
		self.line = line

def to_tokens(split_program):
	tokens = list()
	newline_count = 1
	for token_string in split_program:
		new_token = token(token_string, newline_count)
		if new_token.value == '\n':
			newline_count += 1
		tokens.append(new_token)
	return tokens

def filter_empty_tokens(tokens):
	return list(filter(lambda x: (not(x.value.isspace())) and x.value != '', tokens))
