import re

class lexer():

	def tokenize(self, program):
		program = self.disambiguate_subtraction(program)
		split_program = re.split('(\W)', program)
		tokens = self.to_tokens(split_program)
		tokens = list(filter(lambda x: (not(x.value.isspace())) and x.value != '', tokens))
		tokens = self.fuse_negative_numbers(tokens)
		tokens = self.reform_subtraction(tokens)
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

	def disambiguate_subtraction(self, source):
		return re.sub('\w+\s*(-)', "$", source) # replaces all subtraction operations with "$" token

	def fuse_negative_numbers(self, tokens):
		for token in range(0, len(tokens) - 1):
			if tokens[token].value == '-' and tokens[token + 1].value.isnumeric():
				tokens[token].value = '-' + tokens[token + 1].value
				del tokens[token + 1]
		return tokens

	def reform_subtraction(self, tokens):
		for token in tokens:
			if token.value == '$':
				token.value = '-'
		return tokens
