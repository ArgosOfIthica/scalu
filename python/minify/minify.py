
import re

class minifier():

	def minify(self, cfg_string):
		output = ''
		aliases = list(re.findall('alias\s(\S+)\s(?:\"(.*)\"|(\S+))', cfg_string))
		aliases = [tuple(filter(lambda x:  x != '', alias)) for alias in aliases]
		print(aliases)
		alias_dict = dict()
		alias_mapping = dict()
		for alias in aliases:
			for slice_size in range(16):
				attempt = 'π' + str(hash(alias[0]))[:slice_size]
				if attempt not in alias_dict:
					alias_mapping[alias[0]] = attempt
					alias_dict[attempt] = alias[1]
					break
		for alias in alias_dict:
			split_value = re.split('(\W)', alias_dict[alias])
			updated_value = [ self.minify_word(word, alias_mapping) for word in split_value]
			updated_value = ''.join(updated_value)
			alias_dict[alias] = updated_value
		for alias in alias_dict:
			output += 'alias ' + alias + ' "' + alias_dict[alias] + '"\n'
		output = re.sub(';(\s+)', ';', output)
		output = re.sub(';(\s*)\"', '"', output)
		print(output)


	def minify_word(self, word, alias_mapping):
		if word in alias_mapping:
			return alias_mapping[word]
		else:
			return word

