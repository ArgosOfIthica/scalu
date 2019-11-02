import re

def tokenize(program):

	class token():
		value = ''
		line = -1

	def to_tokens(tokens):
		tokens_list = list()
		newline_count = 1
		for token_string in range(0, len(tokens)):
			new_token = token()
			new_token.value = tokens[token_string]
			new_token.line = newline_count
			if new_token.value == '\n':
				newline_count += 1
			tokens_list.append(new_token)
		return tokens_list

	tokens = re.split('(\W)', program)
	tokens = to_tokens(tokens)
	tokens = list(filter(lambda x: (not(x.value.isspace())) and x.value != '', tokens))
	for token in range(0, len(tokens)):
		tokens[token].value.lower()
	return tokens


