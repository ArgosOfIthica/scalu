import re

def tokenize(program):
	cleaned_program = purge_comments(program)
	split_program = split_on_word(cleaned_program)
	tokens = to_tokens(split_program)
	tokens = filter_empty_tokens(tokens)
	tokens = lower_tokens(tokens)
	return tokens

class token():

	def __init__(self, value, line):
		self.value = value
		self.line = line

def purge_comments(program):
	return re.sub("\/\*[\s\S]*?\*\/", "", program)

def split_on_word(program):
	return re.split('(\W)', program)

def to_tokens(split_program):
	tokens = list()
	newline_count = 1
	source_mode = False
	source_blob = ''
	for token_string in split_program:
		if token_string == '\n':
			newline_count += 1
		elif source_mode == False:
			new_token = token(token_string, newline_count)
			tokens.append(new_token)
			if new_token.value == '[':
				source_mode = True
		elif source_mode == True:
			if token_string == ']':
				new_token = token(source_blob, newline_count)
				tokens.append(new_token)
				end_call = token(token_string, newline_count)
				tokens.append(end_call)
				source_blob = ''
				source_mode = False
			else:
				source_blob += token_string
	return tokens

def filter_empty_tokens(tokens):
	return list(filter(lambda x: (not(x.value.isspace())) and x.value != '', tokens))

def lower_tokens(tokens):
	for token in tokens:
		token.value = token.value.lower()
	return tokens
