
import re
import math
import src.backend.model.universe as universe

def minify(cfg_string, uni):
	blob = alias_blob(uni)
	blob.alias_tuples = to_tuple_list(cfg_string)
	root_computation = blob.alias_convert[blob.alias_tuples[0][0]]
	output_text = minify_names(blob) + root_computation
	output_text = clean_output(output_text)
	output_text = reallocate(output_text, blob)
	output_text = clean_output(output_text)
	return output_text

def clean_output(output_text):
	output_text = re.sub(';(\s*)\"', '"', output_text)
	output_text = re.sub('\";', '"', output_text)
	output_text = re.sub('\n{2,}', '\n', output_text)
	return output_text

def minify_names(blob):
	HEAD_INDEX = 0
	TAIL_INDEX = 1
	output_text = ''
	for alias in blob.alias_tuples:
		new_head = blob.alias_convert[alias[HEAD_INDEX]]
		new_tail = minify_payload(alias[TAIL_INDEX], blob)
		output_text += 'alias ' + new_head + ' "' + new_tail + '"\n'
	return output_text


def minify_payload(tail, blob):
	split_tail = re.split('(\W)', tail)
	split_value = clean_split(split_tail)
	updated_value = [ minify_word(word, blob.alias_convert) for word in split_value]
	updated_value = ''.join(updated_value)
	return updated_value

def clean_split(split_tail):
	for token in range(len(split_tail)):
		if split_tail[token] == '%':
			split_tail[token] = ''
			split_tail[token + 1] = '%' + split_tail[token + 1]
	return split_tail


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
	line_count = math.ceil(len(text) / blob.CONSOLE_MAX_BUFFER) + 1
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
	return lines


def to_tuple_list(cfg_string):
	return list(re.findall('alias\s(\S+)\s\"(.*)\"', cfg_string))

def minify_word(word, alias_convert):
	if word in alias_convert:
		return alias_convert[word]
	else:
		return word

class alias_blob():

	def __init__(self, uni=None):
		self.CONSOLE_MAX_BUFFER = 440 #limit determined by trial and error in HL:Source
		self.alias_tuples = tuple()
		self.alias_convert = dict()
		self.pick = universe.picker()
		if uni is not None:
			for alias in uni.known_aliases:
				if alias.type == 'event':
					self.alias_convert[alias.identity] = alias.string
				else:
					self.alias_convert[alias.identity] = self.pick.new_alias()

