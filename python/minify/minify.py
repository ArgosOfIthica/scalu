
import re
import math

class minifier():

	def minify(self, cfg_string):
		output_text = ''
		aliases = self.to_tuple_list(cfg_string)
		aliases = self.sanitize_list(aliases)
		alias_dict = dict()
		alias_mapping = dict()
		output_text = self.minify_names(aliases, alias_dict, alias_mapping)
		output_text = re.sub(';(\s+)', ';', output_text)
		output_text = re.sub(';(\s*)\"', '"', output_text)
		print(output_text)


	def minify_names(self, aliases, alias_dict, alias_mapping):
		output_text = ''
		pick = picker()
		for alias in aliases:
			attempt = 'π' + pick.new_alias()
			alias_mapping[alias[0]] = attempt
			alias_dict[attempt] = alias[1]
			new_alias = alias_mapping[alias[0]]
			self.minify_payload(new_alias, alias_dict, alias_mapping)
			output_text += 'alias ' + new_alias + ' "' + alias_dict[new_alias] + '"\n'
		return output_text


	def minify_payload(self, alias, alias_dict, alias_mapping):
		split_value = re.split('(\W)', alias_dict[alias])
		updated_value = [ self.minify_word(word, alias_mapping) for word in split_value]
		updated_value = ''.join(updated_value)
		alias_dict[alias] = updated_value

	def sanitize_list(self, aliases):
		return [tuple(filter(lambda x:  x != '', alias)) for alias in aliases]

	def to_tuple_list(self, cfg_string):
		return list(re.findall('alias\s(\S+)\s(?:\"(.*)\"|(\S+))', cfg_string))

	def minify_word(self, word, alias_mapping):
		if word in alias_mapping:
			return alias_mapping[word]
		else:
			return word



class picker():

	def __init__(self):
		self.symbols = list()
		self.current_use = 1
		for x in range(48, 58):
			self.symbols.append(chr(x))
		for x in range(97, 123):
			self.symbols.append(chr(x))

	def new_alias(self):
		revolutions = int(math.log(self.current_use, len(self.symbols))) + 1
		revo = math.log(self.current_use, len(self.symbols))
		new_alias = list()
		for x in range(0, revolutions):
			selected = int((self.current_use / int((len(self.symbols) ** x)) % len(self.symbols)))
			new_alias = [self.symbols[selected]] + new_alias
		new_alias = ''.join(new_alias)
		self.current_use += 1
		return new_alias

