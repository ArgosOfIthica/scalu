
from backend.definitions.vbuilder import build_lookup
from frontend.parser.structure import structure


alias = 'alias '
true = 'btrue '
false = 'bfalse '
next = '; '
new = '\n'

class atom():
	ele = None

	def __init__(self, ele):
		self.ele = ele
		self.s = structure()

	def get_word_size(self):
		try:
			return int(self.ele.output.word_size)
		except:
			print(self.ele.identity)
			print(self.ele.arg[0])
			return int(self.ele.arg[0].word_size)

	def get_true_return(self):
		return self.ele.output.name + 'tr'

	def get_false_return(self):
		return self.ele.output.name + 'fr'

	def get_alpha_bit(self):
		return self.ele.arg[0].name + 'b'

	def get_beta_bit(self):
		return self.ele.arg[1].name + 'b'

	def get_hash(self):
		if self.s.is_unary_operator(self.ele):
			return str(hash(self.ele.identity + self.ele.arg[0].name + self.ele.output.name))
		elif self.s.is_binary_operator(self.ele):
			return str(hash(self.ele.identity + self.ele.arg[0].name + self.ele.arg[1].name + self.ele.output.name))
		else:
			Exception('failure')


class instruction_bundle():
		header = ''
		sequence = ''


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
	bundle = instruction_bundle()
	for bit in range(0, word_size):
		bundle.sequence += alias + true + true_return + str(bit) + next + alias + false + false_return + str(bit) + next + alpha_bit + str(bit) + next
	return bundle


def ibprint(atom):
	word_size = atom.get_word_size()
	alpha_bit = atom.get_alpha_bit()
	bundle = instruction_bundle()

	bundle.sequence += alias + true + 'echo 1' + next + alias + false + 'echo 0' + next
	for bit in range(0, word_size):
		bundle.sequence += alpha_bit + str(bit) + next
	return bundle




def ibitwise_neg(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	bundle = instruction_bundle()
	for bit in range(0, word_size):
		bundle.sequence += alias + true + false_return + str(bit) + next + alias + false + true_return + str(bit) + next + alpha_bit + str(bit) + next
	return bundle

def ibitwise_or(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()
	false_branch = atom.get_hash() + '_false_branch'
	bundle = instruction_bundle()

	for bit in range(0, word_size):
		bundle.header += alias + false_branch + str(bit) + ' "' + alias + true + true_return + str(bit) + next + alias + false + false_return + str(bit) + next + beta_bit + str(bit) + '"' + new
	for bit in range(0, word_size):
		bundle.sequence += alias + true + true_return + str(bit) + next + alias + false + false_branch + str(bit) + next + alpha_bit + str(bit) + next
	return bundle

def ibitwise_and(atom):
	word_size = atom.get_word_size()
	true_return = atom.get_true_return()
	false_return = atom.get_false_return()
	alpha_bit = atom.get_alpha_bit()
	beta_bit = atom.get_beta_bit()
	true_branch = atom.get_hash() + '_true_branch'
	bundle = instruction_bundle()

	for bit in range(0, word_size):
		bundle.header += alias + true_branch + str(bit) + ' "' + alias + true + true_return + str(bit) + next + alias + false + false_return + str(bit) + next + beta_bit + str(bit) + '"' + new
	for bit in range(0, word_size):
		bundle.sequence += alias + true + true_branch + str(bit) + next + alias + false + false_return + str(bit) + next + alpha_bit + str(bit) + next
	return bundle


