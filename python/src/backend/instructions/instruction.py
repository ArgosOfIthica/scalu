import src.model.structure as model
import src.backend.model.universe as universe


def handle_instruction(global_object, compute, statement):
	operator_map = {'literal' : icopy,
				'binary_print' : ibinary_print,
				'bitwise_neg' : ibitwise_neg,
				'bitwise_or' : ibitwise_or,
				'bitwise_and' : ibitwise_and}

	uni = global_object.universe
	if statement.output not in uni.constructs:
		var_compute = add_var(global_object, statement.output)
		uni.constructs[statement.output] = var_compute
	for arg in statement.arg:
		if arg not in uni.constructs:
			var_compute = add_var(global_object, arg)
			uni.constructs[arg] = var_compute
	if model.is_operator(statement):
		instr_class = operator_map[statement.identity](global_object, compute, statement)
		instr_class.compile()
	else:
		raise Exception('invalid instruction generation')

def get_bin(value, word_size):
	return format(int(value), 'b').zfill(int(word_size))

def add_var(global_object, var):
	uni = global_object.universe
	bool_string = get_bin(var.value, var.word_size)
	var_computation = uni.add_computation('variable')
	bits = uni.extend_add_computation(var_computation, 'bit_collection')
	set_true = uni.extend_add_computation(var_computation, 'true_collection')
	set_false = uni.extend_add_computation(var_computation, 'false_collection')
	for bit in range(int(var.word_size)):
		vb = uni.extend_add_computation(bits, "variable_bit")
		if bool_string[bit] == '0':
			vb.extend(uni.false)
		elif bool_string[bit] == '1':
			vb.extend(uni.true)
		else:
			print('TODO: ADD EXCEPTION')
		true_compute = uni.extend_add_computation(set_true, 'set_true')
		true_vb = uni.extend_add_computation(true_compute, 'set_vb_true')
		true_vb.alias = vb.alias
		true_vb.extend(uni.true)
		false_compute = uni.extend_add_computation(set_false, 'set_false')
		false_vb = uni.extend_add_computation(false_compute, 'set_vb_false')
		false_vb.alias = vb.alias
		false_vb.extend(uni.false)
	return var_computation

class instruction():

	def __init__(self, global_object, container_compute, statement):
		self.uni = global_object.universe
		self.container_compute = container_compute
		self.identity_compute = self.uni.extend_add_computation(container_compute, 'instruction')
		self.statement = statement
		self.output = self.uni.constructs[statement.output]
		self.alpha = self.uni.constructs[statement.arg[0]]
		if model.is_binary_operator(statement):
			self.beta = self.uni.constructs[statement.arg[1]]

#these methods use None as a default argument because default args must be known at compile time.
#Therefore, setting the identity as a default arg MUST be done ad-hoc at runtime.

	def set_true_return(self, set_compute, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		set_compute_to_true_return = self.uni.extend_add_computation(compute_for, "code")
		set_compute_to_true_return.alias = set_compute
		INDEX_OF_TRUE_SETTERS = 1
		true_vb_alias = self.output.commands[INDEX_OF_TRUE_SETTERS].commands[bit].alias
		set_compute_to_true_return.extend(true_vb_alias)
		return set_compute_to_true_return

	def set_false_return(self, set_compute, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		set_compute_to_false_return = self.uni.extend_add_computation(compute_for, "code")
		set_compute_to_false_return.alias = set_compute
		INDEX_OF_FALSE_SETTERS = 2
		false_vb_alias = self.output.commands[INDEX_OF_FALSE_SETTERS].commands[bit].alias
		set_compute_to_false_return.extend(false_vb_alias)
		return set_compute_to_false_return

	def execute_alpha(self, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		INDEX_OF_VALUES = 0
		exec_vb_alias = self.alpha.commands[INDEX_OF_VALUES].commands[bit].alias
		compute_for.extend(exec_vb_alias)
		return exec_vb_alias

	def execute_beta(self, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		INDEX_OF_VALUES = 0
		exec_vb_alias = self.beta.commands[INDEX_OF_VALUES].commands[bit].alias
		compute_for.extend(exec_vb_alias)
		return exec_vb_alias

class icopy(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_return(self.uni.true, bit)
			self.set_false_return(self.uni.false, bit)
			self.execute_alpha(bit)

class ibinary_print(instruction):

	def compile(self):
		open_print = universe.source_command('echo **<')
		self.identity_compute.extend(open_print)
		self.echo_true()
		self.echo_false()
		for bit in range(int(self.statement.output.word_size)):
			self.execute_alpha(bit)
		close_print = universe.source_command('echo >**')
		self.identity_compute.extend(close_print)
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_return(self.uni.true, bit)
			self.set_false_return(self.uni.false, bit)
			self.execute_alpha(bit)

	def echo_true(self):
		set_true_computation = self.uni.extend_add_computation(self.identity_compute, 'code')
		set_true_computation.alias = self.uni.true
		set_true_computation.extend(universe.source_command('echo 1'))

	def echo_false(self):
		set_false_computation = self.uni.extend_add_computation(self.identity_compute, 'code')
		set_false_computation.alias = self.uni.false
		set_false_computation.extend(universe.source_command('echo 0'))


class ibitwise_neg(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_return(self.uni.false, bit)
			self.set_false_return(self.uni.true, bit)
			self.execute_alpha(bit)

class ibitwise_and(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			true_branch = self.compile_true_branch(bit)
			self.set_true_branch(true_branch)
			self.set_false_return(self.uni.false, bit)
			self.execute_alpha(bit)

	def set_true_branch(self, true_branch):
		set_true_to_true_branch = self.uni.extend_add_computation(self.identity_compute, 'code')
		set_true_to_true_branch.extend(true_branch.alias)
		set_true_to_true_branch.alias = self.uni.true

	def compile_true_branch(self, bit):
		true_branch_compute = self.uni.extend_add_computation(self.uni.root, 'code')
		self.set_true_return(self.uni.true, bit, true_branch_compute)
		self.set_false_return(self.uni.false, bit, true_branch_compute)
		self.execute_beta(bit, true_branch_compute)
		return true_branch_compute


class ibitwise_or(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_return(self.uni.true, bit)
			false_branch = self.compile_false_branch(bit)
			self.execute_alpha(bit)

	def set_false_branch(self, false_branch):
		set_false_to_false_branch = self.uni.extend_add_computation(self.uni.root, 'code')
		set_false_to_false_branch.extend(false_branch.alias)
		set_false_to_false_branch.alias = self.uni.false

	def compile_false_branch(self, bit):
		false_branch_compute = self.uni.extend_add_computation(self.uni.root, 'code')
		self.set_true_return(self.uni.true, bit, false_branch_compute)
		self.set_false_return(self.uni.false, bit, false_branch_compute)
		self.execute_beta(bit, false_branch_compute)
		return false_branch_compute

