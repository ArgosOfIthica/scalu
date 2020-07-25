
import re
import math
import src.backend.model.universe as universe

def minify(cfg_string):
	blob = alias_blob()
	blob.alias_tuples = to_tuple_list(cfg_string)
	output_text = minify_names(blob)
	output_text = clean_output(output_text)
	output_text = reallocate(output_text, blob)
	output_text = clean_output(output_text)
	return output_text

def clean_output(output):
	output_text = output
	output_text = re.sub(';(\s+)', ';', output_text)
	output_text = re.sub(';(\s*)\"', '"', output_text)
	output_text = re.sub('\";', '"', output_text)
	return output_text

def minify_names(blob):
	HEAD = 0
	TAIL = 1
	output_text = ''
	for alias in blob.alias_tuples:
		attempt = blob.pick.new_alias()
		blob.alias_convert[alias[HEAD]] = attempt
		blob.alias_new[attempt] = alias[TAIL]
		new_alias = blob.alias_convert[alias[HEAD]]
		minify_payload(new_alias, blob)
		output_text += 'alias ' + new_alias + ' "' + blob.alias_new[new_alias] + '"\n'
	return output_text


def minify_payload(alias, blob):
	split_value = re.split('(\W)', blob.alias_new[alias])
	updated_value = [ minify_word(word, blob.alias_convert) for word in split_value]
	updated_value = ''.join(updated_value)
	blob.alias_new[alias] = updated_value

def reallocate(output_text, blob):
	split_lines = re.split('\n', output_text)
	line = 0
	while True:
		if len(split_lines[line]) > blob.CONSOLE_MAX_BUFFER:
			replacement = compute_reallocation(split_lines[line], blob)
			split_lines = split_lines[:line] + replacement + split_lines[line + 1:]
		line += 1
		if line == len(split_lines):
			break
	new_output = '\n'.join(split_lines)
	return new_output



def compute_reallocation(text, blob):
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

def to_tuple_list(cfg_string):
	return list(re.findall('alias\s(\S+)\s\"(.*)\"', cfg_string))

def minify_word(word, alias_convert):
	if word in alias_convert:
		return alias_convert[word]
	else:
		return word

class alias_blob():

	def __init__(self):
		self.CONSOLE_MAX_BUFFER = 436 - 2
		self.alias_tuples = tuple()
		self.alias_new = dict()
		self.alias_convert = dict()
		self.pick = universe.picker()

