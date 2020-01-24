
from backend.definitions.vbuilder import build_lookup

alias = 'alias '
true = 'btrue '
false = 'bfalse '
true_return = "gt"
false_return = "gf"
alpha_bit = "ga"
beta_bit = "gb"
next = '; '
new = '\n'

class target():
	true_return = 'gt'
	false_return = 'gf'
	alpha_bit = 'ga'
	beta_bit = 'gb'

class atomic_instruction():
	id = 0
	identity = ''
	destination = ''
	source = ''

	def get_word_size(self):
		return int(self.destination.word_size)

	def get_true_return(self):
		return self.destination.name + 'tr'

	def get_false_return(self):
		return self.destination.name + 'fr'

	def get_alpha_bit(self):
		return self.destination.name + 'b'

	def get_beta_bit(self):
		return self.source.name + 'b'

def generate_instructions(instruction_set):
	instruction_set = minimize_instructions(instruction_set)
	instr_map = {
		'assignment': icopy,
		'bitwise_or': ibitwise_or,
		'bitwise_and': ibitwise_and,
		'bitwise_neg': ibitwise_neg
		}
	out = ''
	for instr in instruction_set:
		instr_function = instr_map[instr.identity]
		out += instr_function(instr)
		out += new
	return out


def minimize_instructions(instruction_set):
	instructions = set()
	atomized_instructions = set()
	for ele in instruction_set:
		if ele.family == 'binary':
			instructions.add((ele.identity, ele.destination, ele.source))
		if ele.family == 'unary':
			instructions.add((ele.identity, ele.destination, None))
	for instr in instructions:
		new_instr = atomic_instruction()
		if instr[2] is not None:
			new_instr.id = instr[1].name + instr[2].name
		else:
			new_instr.id = instr[1].name
		new_instr.identity = instr[0]
		new_instr.destination = instr[1]
		new_instr.source = instr[2]
		atomized_instructions.add(new_instr)
	return atomized_instructions

def sandboxed_ascii(var):
	if (var >= 33 and var <= 37) or (var >= 39 and var <= 57) or (var >= 60 and var <= 127):
		return chr(var)
	else:
		return 'ascii' + str(var)

def icopy(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()
	identity = atom.id + 'copy'

	out =  alias + identity + str(word_size) + ' "'
	for word in range(0, word_size):
		out += alias + true + true_return + str(word) + next + alias + false + false_return + str(word) + next + beta_bit + str(word)
		if word != word_size - 1:
			out += next
	out += '"'
	return out


def idump(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	identity = atom.id + 'dump'

	out = alias  + identity + str(word_size) + ' "'
	out += alias + true + 'echo 1' + next + alias + false + 'echo 0' + next
	for word in range(0, word_size):
		out += alpha_bit + str(word)
		if word != word_size - 1:
			out += next
	out += '"'
	return out


#hex instruction is not generated if word size < 4
def ihexdump(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	


	def hd_label(num):
		if num > 0:
			return atom.id + 'hdc' + str(word_size) + str(num) + '_'
		else:
			return atom.id + 'hd' + str(word_size)
	
	def hex_bootstrap(x):
		def hex_modifier(z):
			if z == 0:
				return str(z + 4 * x) + next + hd_label(x + 1)
			else:
				return str(z + 4 * x)
		return hex_modifier

	out = ''
	for x in range(0, int(word_size / 4)):
		out += build_lookup(hd_label(x), word_size, 16, hex, hex_bootstrap(x))
	out += alias + hd_label(int(word_size/4)) 
	return out


def ibitwise_neg(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()

	out = alias  + atom.id + 'bneg' + str(word_size) + ' "'
	for word in range(0, word_size):
		out += alias + true + false_return + str(word) + next + alias + false + true_return + str(word) + next + beta_bit + str(word)
		if word != word_size - 1:
			out += next
	out += '"'
	return out

def ibitwise_or(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()
	identity = atom.id + 'bor'
	false_branch = identity + '_false_branch'

	out = ''
	for x in range(0, word_size):
		out += alias + false_branch + str(x) + ' "' + alias + true + true_return + str(x) + next + alias + false + false_return + str(x) + next + beta_bit + str(x) + '"' + new
	out += new + alias  + identity + str(word_size) + ' "'
	for x in range(0, word_size):
		out += alias + true + true_return + str(x) + next + alias + false + false_branch + str(x) + next + alpha_bit + str(x)
		if x != word_size - 1:
			out += next
	out += '"'
	return out

def ibitwise_and(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()

	out = ''
	for x in range(0, word_size):
		out += alias + 'band_true_branch' + str(x) + ' "' + alias + true + true_return + str(x) + next + alias + false + false_return + str(x) + next + beta_bit + str(x) + '"' + new
	out += new + alias  + atom.id +  'band' + str(word_size) + ' "'
	for x in range(0, word_size):
		out += alias + true + 'band_true_branch' + str(x) + next + alias + false + false_return + str(x) + next + alpha_bit + str(x)
		if x != word_size - 1:
			out += next
	out += '"'
	return out

