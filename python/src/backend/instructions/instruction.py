import src.model.structure as model


def handle_instruction(global_object, compute, statement):
	uni = global_object.universe
	if statement.output not in uni.constructs:
		var_compute = add_var(global_object, statement.output)
		uni.constructs[statement.output] = var_compute
	for arg in statement.arg:
		if arg not in uni.constructs:
			var_compute = add_var(global_object, arg)
			uni.constructs[arg] = var_compute
	if is_literal_value(statement):
		icopy(global_object, compute, statement)


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
		vb = uni.add_computation("variable_bit")
		if bool_string[bit] == '0':
			vb.extend(uni.false)
		elif bool_string[bit] == '1':
			vb.extend(uni.true)
		else:
			print('TODO: ADD EXCEPTION')
		bits.extend(vb)
		true_compute = uni.extend_add_computation(set_true, 'set_true')
		true_vb = uni.extend_add_computation(true_compute, 'set_vb_true')
		true_vb.alias = vb.alias
		true_vb.extend(uni.true)
		false_compute = uni.extend_add_computation(set_false, 'set_false')
		false_vb = uni.extend_add_computation(false_compute, 'set_vb_false')
		false_vb.alias = vb.alias
		false_vb.extend(uni.false)
	return var_computation



def set_true_return(global_object, instruction_computation, variable_computation, bit):
	uni = global_object.universe
	INDEX_OF_TRUE_SETTERS = 1
	true_vb_alias = variable_computation.commands[INDEX_OF_TRUE_SETTERS].commands[bit].alias
	set_true_to_true_return = uni.extend_add_computation(instruction_computation, "code")
	set_true_to_true_return.alias = uni.true
	set_true_to_true_return.extend(true_vb_alias)
	return set_true_to_true_return

def set_false_return(global_object, instruction_computation, variable_computation, bit):
	uni = global_object.universe
	INDEX_OF_FALSE_SETTERS = 2
	false_vb_alias = variable_computation.commands[INDEX_OF_FALSE_SETTERS].commands[bit].alias
	set_false_to_false_return = uni.extend_add_computation(instruction_computation, "code")
	set_false_to_false_return.alias = uni.false
	set_false_to_false_return.extend(false_vb_alias)
	return set_false_to_false_return

def execute_bit(global_object, instruction_computation, variable_computation, bit):
	uni = global_object.universe
	INDEX_OF_VALUES = 0
	exec_vb_alias = variable_computation.commands[INDEX_OF_VALUES].commands[bit].alias
	instruction_computation.extend(exec_vb_alias)
	return exec_vb_alias


def icopy(global_object, compute, statement):
	uni = global_object.universe
	output = uni.constructs[statement.output]
	alpha_arg = uni.constructs[statement.arg[0]]
	copy = uni.extend_add_computation(compute, "instruction")
	for bit in range(0, int(statement.output.word_size)):
		true_return = set_true_return(global_object, copy, output, bit)
		false_return = set_false_return(global_object, copy, output, bit)
		alpha_bit = execute_bit(global_object, copy, alpha_arg, bit)








