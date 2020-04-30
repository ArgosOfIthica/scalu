
import re
import math

class minifier():

	def minify(self, cfg_string):
		blob = alias_blob()
		blob.alias_tuples = self.sanitize_list(self.to_tuple_list(cfg_string))
		output_text = self.minify_names(blob)
		output_text = re.sub(';(\s+)', ';', output_text)
		output_text = re.sub(';(\s*)\"', '"', output_text)
		output_text = self.reallocate(output_text, blob)
		return output_text

	def minify_names(self, blob):
		HEAD = 0
		TAIL = 1
		output_text = ''
		for alias in blob.alias_tuples:
			attempt = blob.pick.new_alias()
			blob.alias_convert[alias[HEAD]] = attempt
			blob.alias_new[attempt] = alias[TAIL]
			new_alias = blob.alias_convert[alias[HEAD]]
			self.minify_payload(new_alias, blob)
			output_text += 'alias ' + new_alias + ' "' + blob.alias_new[new_alias] + '"\n'
		return output_text


	def minify_payload(self, alias, blob):
		split_value = re.split('(\W)', blob.alias_new[alias])
		updated_value = [ self.minify_word(word, blob.alias_convert) for word in split_value]
		updated_value = ''.join(updated_value)
		blob.alias_new[alias] = updated_value

	def reallocate(self, output_text, blob):
		split_lines = re.split('\n', output_text)
		line = 0
		while True:
			if len(split_lines[line]) > blob.CONSOLE_MAX_BUFFER:
				replacement = self.compute_reallocation(split_lines[line], blob)
				split_lines = split_lines[:line] + replacement + split_lines[line + 1:]
			line += 1
			if line == len(split_lines):
				break
		new_output = '\n'.join(split_lines)
		return new_output



	def compute_reallocation(self, text, blob):
		command_split = re.split(';', text)
		line_count = math.ceil(len(text) / blob.CONSOLE_MAX_BUFFER)
		new_aliases = blob.pick.new_alias_list(line_count)
		lines = [''] * line_count
		command = 0
		for line in range(len(lines)):
			if line > 0 and command < len(command_split):
				lines[line] = 'alias ' + new_aliases[line - 1] + ' "'
			while(command < len(command_split)):
				test_line = lines[line] + command_split[command] + ';' + new_aliases[line]
				if len(test_line) < blob.CONSOLE_MAX_BUFFER:

					lines[line] = lines[line] + command_split[command] + ';'
					command += 1
				else:
					lines[line] = lines[line] + new_aliases[line] + '"'
					break
			lines[line] = lines[line]
		return lines





#TODO: continue from here

	def sanitize_list(self, aliases):
		return [tuple(filter(lambda x:  x != '', alias)) for alias in aliases]

	def to_tuple_list(self, cfg_string):
		return list(re.findall('alias\s(\S+)\s(?:\"(.*)\"|(\S+))', cfg_string))

	def minify_word(self, word, alias_convert):
		if word in alias_convert:
			return alias_convert[word]
		else:
			return word

class alias_blob():

	def __init__(self):
		self.CONSOLE_MAX_BUFFER = 512 -2
		self.alias_tuples = tuple()
		self.alias_new = dict()
		self.alias_convert = dict()
		self.pick = picker()

class picker():

	def __init__(self):

		self.symbols = list()
		self.current_use = 1
		for x in range(48, 58):
			self.symbols.append(chr(x))
		for x in range(97, 123):
			self.symbols.append(chr(x))

	def new_alias_list(self, count):
		alias_list = list()
		for alias in range(count):
			alias_list.append(self.new_alias())
		return alias_list


	def new_alias(self):
		revolutions = int(math.log(self.current_use, len(self.symbols))) + 1
		revo = math.log(self.current_use, len(self.symbols))
		new_alias = list()
		for x in range(0, revolutions):
			selected = int((self.current_use / int((len(self.symbols) ** x)) % len(self.symbols)))
			new_alias = [self.symbols[selected]] + new_alias
		new_alias = ''.join(new_alias)
		new_alias = 'π' + new_alias
		self.current_use += 1
		return new_alias

