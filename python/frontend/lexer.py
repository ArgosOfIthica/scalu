import re

class lexer():

	def tokenize(self, program):
		split_program = re.split('(\W)', program)
		tokens = self.to_tokens(split_program)
		tokens = list(filter(lambda x: (not(x.value.isspace())) and x.value != '', tokens))
		for token in tokens:
			token.value = token.value.lower()
		return tokens

	class token():
		value = ''
		line = -1

	def to_tokens(self, split_program):
		tokens_list = list()
		newline_count = 1
		for token_string in split_program:
			new_token = self.token()
			new_token.value = token_string
			new_token.line = newline_count
			if new_token.value == '\n':
				newline_count += 1
			tokens_list.append(new_token)
		return tokens_list
