import re

def tokenize(program):
	program = disambiguate_subtraction(program)
	tokens = re.split('(\W)', program)
	tokens = to_tokens(tokens)
	tokens = list(filter(lambda x: (not(x.value.isspace())) and x.value != '', tokens))
	tokens = fuse_negative_numbers(tokens)
	tokens = reform_subtraction(tokens)
	for token in tokens:
		token.value = token.value.lower()
	return tokens

class token():
	value = ''
	line = -1

def to_tokens(tokens):
	tokens_list = list()
	newline_count = 1
	for token_string in tokens:
		new_token = token()
		new_token.value = token_string
		new_token.line = newline_count
		if new_token.value == '\n':
			newline_count += 1
		tokens_list.append(new_token)
	return tokens_list

def disambiguate_subtraction(source):
	return re.sub('\w+\s*(-)', "$", source) # replaces all subtraction operations with "$" token

def fuse_negative_numbers(tokens):
	for token in range(0, len(tokens) - 1):
		if tokens[token].value == '-' and tokens[token + 1].value.isnumeric():
			tokens[token].value = '-' + tokens[token + 1].value
			del tokens[token + 1]
	return tokens

def reform_subtraction(tokens):
	for token in tokens:
		if token.value == '$':
			token.value = '-'
	return tokens