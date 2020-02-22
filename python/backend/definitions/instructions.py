
from backend.definitions.vbuilder import build_lookup

alias = 'alias '
true = 'btrue '
false = 'bfalse '
next = '; '
new = '\n'

class atom():
	ele = None

	def __init__(self, ele):
		self.ele = ele

	def get_word_size(self):
		return int(self.ele.output.word_size)

	def get_true_return(self):
		return self.ele.output.name + 'tr'

	def get_false_return(self):
		return self.ele.output.name + 'fr'

	def get_alpha_bit(self):
		print(self.ele)
		return self.ele.arg[0].name + 'b'

	def get_beta_bit(self):
		return self.ele.arg[1].name + 'b'

	def get_hash(self):
		if self.ele.family== 'unary':
			return str(hash(self.ele.identity + self.ele.arg1.name + self.ele.output.name))
		elif self.ele.family == 'binary':
			return str(hash(self.ele.identity + self.ele.arg1.name + self.ele.arg2.name + self.ele.output.name))
		else:
			Exception('failure')

def build_instruction(ele):
	instr_map = {
		'copy': icopy,
		'bprint': ibprint,
		'bitwise_or': ibitwise_or,
		'bitwise_and': ibitwise_and,
		'bitwise_neg': ibitwise_neg
		}
	instr = atom(ele)
	instr_function = instr_map[ele.identity]
	return instr_function(instr)


def icopy(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	sequence = ''
	header = ''
	for bit in range(0, word_size):
		sequence += alias + true + true_return + str(bit) + next + alias + false + false_return + str(bit) + next + alpha_bit + str(bit) + next
	return header, sequence


def ibprint(atom):
	word_size = atom.get_word_size()
	alpha_bit = atom.get_alpha_bit()
	sequence = ''
	header = ''

	sequence += alias + true + 'echo 1' + next + alias + false + 'echo 0' + next
	for bit in range(0, word_size):
		sequence += alpha_bit + str(bit) + next
	return header, sequence




def ibitwise_neg(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	sequence = ''
	header = ''
	for bit in range(0, word_size):
		sequence += alias + true + false_return + str(bit) + next + alias + false + true_return + str(bit) + next + alpha_bit + str(bit) + next
	return header, sequence

def ibitwise_or(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()
	false_branch = atom.get_hash() + '_false_branch'
	sequence = ''
	header = ''

	for bit in range(0, word_size):
		header += alias + false_branch + str(bit) + ' "' + alias + true + true_return + str(bit) + next + alias + false + false_return + str(bit) + next + beta_bit + str(bit) + '"' + new
	for bit in range(0, word_size):
		sequence += alias + true + true_return + str(bit) + next + alias + false + false_branch + str(bit) + next + alpha_bit + str(bit) + next
	return header, sequence

def ibitwise_and(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()
	true_branch = atom.get_hash() + '_true_branch'
	sequence = ''
	header = ''

	for bit in range(0, word_size):
		header += alias + true_branch + str(bit) + ' "' + alias + true + true_return + str(bit) + next + alias + false + false_return + str(bit) + next + beta_bit + str(bit) + '"' + new
	for bit in range(0, word_size):
		sequence += alias + true + true_branch + str(bit) + next + alias + false + false_return + str(bit) + next + alpha_bit + str(bit) + next
	return header, sequence


