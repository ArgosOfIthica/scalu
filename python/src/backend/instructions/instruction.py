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
		var = universe.variable(global_object, statement.output)
		uni.constructs[statement.output] = var
	for arg in statement.arg:
		if arg not in uni.constructs:
			var = universe.variable(global_object, arg)
			uni.constructs[arg] = var
	if model.is_operator(statement):
		instr_class = operator_map[statement.identity](global_object, compute, statement)
		instr_class.compile()
	else:
		raise Exception('invalid instruction generation')


def handle_conditional(global_object, compute, statement):
	operator_map = {'equality' : iequality,
				'inequality' : iinequality}

	uni = global_object.universe
	for arg in statement.condition.arg:
		if arg not in uni.constructs:
			var_compute = universe.variable(global_object, arg)
			uni.constructs[arg] = var_compute
	if model.is_conditional(statement.condition):
		instr_class = operator_map[statement.condition.identity](global_object, compute, statement)
		instr_class.compile()
	else:
		raise Exception('invalid conditional generation')

class instruction():

	def __init__(self, global_object, container_compute, statement):
		self.uni = global_object.universe
		self.container_compute = container_compute
		self.identity_compute = self.uni.host_def(container_compute, 'instruction')
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
		true_vb_alias = self.output.set_true[bit].alias
		compute_for.extend(self.uni.set_var(set_compute, true_vb_alias).alias)

	def set_false_return(self, set_compute, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		false_vb_alias = self.output.set_false[bit].alias
		compute_for.extend(self.uni.set_var(set_compute, false_vb_alias).alias)

	def execute_alpha(self, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		exec_vb_alias = self.alpha.bits[bit]
		compute_for.extend(exec_vb_alias)
		return exec_vb_alias

	def execute_beta(self, bit, compute_for=None):
		if compute_for == None:
			compute_for = self.identity_compute
		exec_vb_alias = self.beta.bits[bit]
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
		set_true_computation = self.uni.host_def(self.identity_compute, 'code')
		echo = universe.source_command('echo 1')
		set_true_computation.extend(self.uni.set_var(self.uni.true, echo).alias)

	def echo_false(self):
		set_false_computation = self.uni.host_def(self.identity_compute, 'code')
		echo = universe.source_command('echo 0')
		set_false_computation.extend(self.uni.set_var(self.uni.false, echo).alias)


class ibitwise_neg(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_return(self.uni.false, bit)
			self.set_false_return(self.uni.true, bit)
			self.execute_alpha(bit)

class ibitwise_and(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_branch(bit)
			self.set_false_return(self.uni.false, bit)
			self.execute_alpha(bit)

	def set_true_branch(self, bit):
		true_branch = self.compile_true_branch(bit)
		set_true_to_true_branch = self.uni.host_def(self.identity_compute, 'code')
		set_true_to_true_branch.extend(self.uni.set_var(self.uni.true, true_branch.alias).alias)

	def compile_true_branch(self, bit):
		true_branch_compute = self.uni.new_def('code')
		self.set_true_return(self.uni.true, bit, true_branch_compute)
		self.set_false_return(self.uni.false, bit, true_branch_compute)
		self.execute_beta(bit, true_branch_compute)
		return true_branch_compute


class ibitwise_or(instruction):

	def compile(self):
		for bit in range(int(self.statement.output.word_size)):
			self.set_true_return(self.uni.true, bit)
			self.set_false_branch(bit)
			self.execute_alpha(bit)

	def set_false_branch(self, bit):
		false_branch = self.compile_false_branch(bit)
		set_false_to_false_branch = self.uni.new_def('code')
		set_false_to_false_branch.extend(self.uni.set_var(self.uni.false, false_branch.alias).alias)

	def compile_false_branch(self, bit):
		false_branch_compute = self.uni.new_def('code')
		self.set_true_return(self.uni.true, bit, false_branch_compute)
		self.set_false_return(self.uni.false, bit, false_branch_compute)
		self.execute_beta(bit, false_branch_compute)
		return false_branch_compute


class conditional(instruction):

	def __init__(self, global_object, container_compute, statement):
		self.uni = global_object.universe
		self.container_compute = container_compute
		self.identity_compute = self.uni.host_def(container_compute, 'instruction')
		self.condition = statement.condition
		self.true_service = statement.true_service
		self.false_service = statement.false_service
		self.true_service_compute = self.uni.constructs[self.true_service]
		self.false_service_compute = self.uni.constructs[self.false_service]
		self.alpha = self.uni.constructs[self.condition.arg[0]]
		self.beta = self.uni.constructs[self.condition.arg[1]]


class iequality(conditional):

	def compile(self):
		self.iteration_list = list()
		for index in range(int(self.condition.arg[0].word_size)):
			new_compute = self.uni.new_def('code')
			self.iteration_list.append(new_compute)
		for bit in range(len(self.iteration_list)):
			self.iteration(bit)
		self.identity_compute.extend(self.iteration_list[0].alias)

	def iteration(self, bit):
		self.set_true_branch(bit)
		self.set_false_branch(bit)
		self.execute_alpha(bit, self.iteration_list[bit])

	def set_true_branch(self, bit):
		compute = self.uni.host_def(self.iteration_list[bit], 'code')
		true_branch = self.compile_true_branch(bit)
		compute.extend(self.uni.set_var(self.uni.true, true_branch.alias).alias)

	def set_false_branch(self, bit):
		compute = self.uni.host_def(self.iteration_list[bit], 'code')
		false_branch = self.compile_false_branch(bit)
		compute.extend(self.uni.set_var(self.uni.false, false_branch.alias).alias)

	def compile_true_branch(self, bit):
		root_compute = self.uni.new_def('code')
		if bit + 1 < len(self.iteration_list):
			root_compute.extend(self.uni.set_var(self.uni.true, self.iteration_list[bit + 1].alias).alias)
		else:
			root_compute.extend(self.uni.set_var(self.uni.true, self.true_service_compute.alias).alias)
		root_compute.extend(self.uni.set_var(self.uni.false, self.false_service_compute.alias).alias)
		self.execute_beta(bit, root_compute)
		return root_compute


	def compile_false_branch(self, bit):
		root_compute = self.uni.new_def('code')
		root_compute.extend(self.uni.set_var(self.uni.true, self.false_service_compute.alias).alias)
		if bit + 1 < len(self.iteration_list):
			root_compute.extend(self.uni.set_var(self.uni.false, self.iteration_list[bit + 1].alias).alias)
		else:
			root_compute.extend(self.uni.set_var(self.uni.false, self.true_service_compute.alias).alias)
		self.execute_beta(bit, root_compute)
		return root_compute




class iinequality(conditional):

	def compile(self):
		pass

