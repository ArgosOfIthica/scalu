import src.model.structure as model
import src.backend.model.universe as universe


def unary_mapper(identity):
	return { 'binary_print' : ibinary_print }

class instruction_wrapper():

	def __init__(self, global_object, compute, statement):
		self.global_object = global_object
		self.compute = compute
		self.statement = statement

class computation_wrapper():

	def __init__(self, global_object, instr_computation, var_access):
		self.global_object = global_object
		self.instr_computation = instr_computation
		self.var_access = var_access

def handle_instruction(global_object, compute, statement):
	unary_map = {'binary_print' : ibinary_print}

	uni = global_object.universe
	if statement.output not in uni.constructs:
		var_compute = add_var(global_object, statement.output)
		uni.constructs[statement.output] = var_compute
	for arg in statement.arg:
		if arg not in uni.constructs:
			var_compute = add_var(global_object, arg)
			uni.constructs[arg] = var_compute
	instr = instruction_wrapper(global_object, compute, statement)
	if model.is_literal_value(statement):
		icopy(instr)
	elif model.is_unary_operator(statement):
		instr_function = unary_map[statement.identity]
		instr_function(instr)

def get_bin(value, word_size):
	return format(int(value), 'b').zfill(int(word_size))

def add_var(global_object, var):
	uni = global_object.universe
	bool_string = get_bin(var.value, var.word_size)
	var_computation = uni.add_computation('variable')
	bits = uni.extend_add_computation(var_computation, 'bit_collection')
	set_true = uni.extend_add_computation(var_computation, 'true_collection')
	set_false = uni.extend_add_computation(var_computation, 'false_collection')
	for bit in range(0, int(var.word_size)):
		vb = uni.extend_add_computation(bits, "variable_bit")
		#vb_sub = uni.extend_add_computation(vb, "set_vb")
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

def set_true_return(comp_wrapper, bit):
	uni = comp_wrapper.global_object.universe
	INDEX_OF_TRUE_SETTERS = 1
	true_vb_alias = comp_wrapper.var_access.commands[INDEX_OF_TRUE_SETTERS].commands[bit].alias
	set_true_to_true_return = uni.extend_add_computation(comp_wrapper.instr_computation, "code")
	set_true_to_true_return.alias = uni.true
	set_true_to_true_return.extend(true_vb_alias)
	return set_true_to_true_return

def set_false_return(comp_wrapper, bit):
	uni = comp_wrapper.global_object.universe
	INDEX_OF_FALSE_SETTERS = 2
	false_vb_alias = comp_wrapper.var_access.commands[INDEX_OF_FALSE_SETTERS].commands[bit].alias
	set_false_to_false_return = uni.extend_add_computation(comp_wrapper.instr_computation, "code")
	set_false_to_false_return.alias = uni.false
	set_false_to_false_return.extend(false_vb_alias)
	return set_false_to_false_return

def execute_bit(comp_wrapper, bit):
	uni = comp_wrapper.global_object.universe
	INDEX_OF_VALUES = 0
	exec_vb_alias = comp_wrapper.var_access.commands[INDEX_OF_VALUES].commands[bit].alias
	comp_wrapper.instr_computation.extend(exec_vb_alias)
	return exec_vb_alias


def icopy(instr):
	uni = instr.global_object.universe
	output = uni.constructs[instr.statement.output]
	alpha_arg = uni.constructs[instr.statement.arg[0]]
	copy = uni.extend_add_computation(instr.compute, "instruction")
	output_wrapper = computation_wrapper(instr.global_object, copy, output)
	alpha_wrapper = computation_wrapper(instr.global_object, copy, alpha_arg)
	for bit in range(0, int(instr.statement.output.word_size)):
		true_return = set_true_return(output_wrapper, bit)
		false_return = set_false_return(output_wrapper, bit)
		alpha_bit = execute_bit(alpha_wrapper, bit)

def ibinary_print(instr):
	uni = instr.global_object.universe
	alpha_arg = uni.constructs[instr.statement.arg[0]]
	binary_print = uni.extend_add_computation(instr.compute, "instruction")
	alpha_wrapper = computation_wrapper(instr.global_object, binary_print, alpha_arg)
	set_uni_boolean_to_command(alpha_wrapper, 'echo 1', True)
	set_uni_boolean_to_command(alpha_wrapper, 'echo 0', False)
	for bit in range(0, int(instr.statement.output.word_size)):
		alpha_bit = execute_bit(alpha_wrapper, bit)


def set_uni_boolean_to_command(comp_wrapper, command_string, uni_boolean):
	uni = comp_wrapper.global_object.universe
	if uni_boolean:
		set_compute_to_command(comp_wrapper, command_string, uni.true)
	else:
		set_compute_to_command(comp_wrapper, command_string, uni.false)

def set_compute_to_command(comp_wrapper, command_string, compute_head):
	uni = comp_wrapper.global_object.universe
	set_compute_command = uni.extend_add_computation(comp_wrapper.instr_computation, "code")
	set_compute_command.alias = compute_head
	execute_command = universe.source_command(command_string)
	set_compute_command.extend(execute_command)


'''
		self.bundle.sequence += alias + true + 'echo 1' + next + alias + false + 'echo 0' + next
		for bit in range(0, self.word_size):
			self.bundle.sequence += self.alpha_bit + str(bit) + next
		return self.bundle
'''

