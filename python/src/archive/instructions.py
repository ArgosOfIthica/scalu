
from backend.definitions.vbuilder import src.build_lookup
from model.structure import src.*


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
		return int(self.ele.output.word_size)

	def get_true_return(self):
		return self.ele.output.name + 'tr'

	def get_false_return(self):
		return self.ele.output.name + 'fr'

	def get_alpha_bit(self):
		return self.ele.arg[0].name + 'b'

	def get_beta_bit(self):
		if len(self.ele.arg) > 1:
			return self.ele.arg[1].name + 'b'
		else:
			return ''

	def get_true_branch(self):
		return self.get_hash() + '_true_branch'

	def get_false_branch(self):
		return self.get_hash() + '_false_branch'

	def get_hash(self):
		if self.s.is_unary_operator(self.ele):
			return str(abs(hash(self.ele.identity + self.ele.arg[0].name + self.ele.output.name)))
		elif self.s.is_binary_operator(self.ele):
			return str(abs(hash(self.ele.identity + self.ele.arg[0].name + self.ele.arg[1].name + self.ele.output.name)))
		else:
			Exception('failure')


class instruction_bundle():
		header = ''
		sequence = ''


class instruction_constructor():


	def build_instruction(self, ele):
		instr = atom(ele)
		instr_map = {
			'copy': icopy(instr),
			'bprint': ibprint(instr),
			'bitwise_or': ibitwise_or(instr),
			'bitwise_and': ibitwise_and(instr),
			'bitwise_neg': ibitwise_neg(instr)
			}

		instr_object = instr_map[ele.identity]
		return instr_object.compile()


class instruction():

	def __init__(self, atom):
		self.word_size = atom.get_word_size()
		self.true_return = atom.get_true_return()
		self.false_return = atom.get_false_return()
		self.alpha_bit = atom.get_alpha_bit()
		self.beta_bit = atom.get_beta_bit()
		self.true_branch = atom.get_true_branch()
		self.false_branch = atom.get_false_branch()
		self.bundle = instruction_bundle()

class icopy(instruction):

	def compile(self):
		for bit in range(0, self.word_size):
			self.bundle.sequence += alias + true + self.true_return + str(bit) + next + alias + false + self.false_return + str(bit) + next + self.alpha_bit + str(bit) + next
		return self.bundle


class ibprint(instruction):

	def compile(self):
		self.bundle.sequence += alias + true + 'echo 1' + next + alias + false + 'echo 0' + next
		for bit in range(0, self.word_size):
			self.bundle.sequence += self.alpha_bit + str(bit) + next
		return self.bundle

class ibitwise_neg(instruction):

	def compile(self):
		for bit in range(0, self.word_size):
			self.bundle.sequence += alias + true + self.false_return + str(bit) + next + alias + false + self.true_return + str(bit) + next + self.alpha_bit + str(bit) + next
		return self.bundle

class ibitwise_or(instruction):

	def compile(self):
		for bit in range(0, self.word_size):
			self.bundle.header += alias + self.false_branch + str(bit) + ' "' + alias + true + self.true_return + str(bit) + next + alias + false + self.false_return + str(bit) + next + self.beta_bit + str(bit) + '"' + new
		for bit in range(0, self.word_size):
			self.bundle.sequence += alias + true + self.true_return + str(bit) + next + alias + false + self.false_branch + str(bit) + next + self.alpha_bit + str(bit) + next
		return self.bundle

class ibitwise_and(instruction):

	def compile(self):
		for bit in range(0, self.word_size):
			self.bundle.header += alias + self.true_branch + str(bit) + ' "' + alias + true + self.true_return + str(bit) + next + alias + false + self.false_return + str(bit) + next + self.beta_bit + str(bit) + '"' + new
		for bit in range(0, self.word_size):
			self.bundle.sequence += alias + true + self.true_branch + str(bit) + next + alias + false + self.false_return + str(bit) + next + self.alpha_bit + str(bit) + next
		return self.bundle


