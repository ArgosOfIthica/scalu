


def instruction_handler(global_object, compute, statement):
	uni = global_object.universe
	if statement.output not in uni.constructs:
		add_var(global_object, statement.output)
	if is_literal(statement.identity):
		icopy(global_object, compute, statement):


def get_bin(value, word_size):
	return format(value, 'b').zfill(word_size)

def add_var(global_object, var):
	uni = global_object.universe
	bool_string = get_bin(var.value, var.word_size)
	var_computation = uni.add_computation('variable')
	bits = uni.add_computation('bit_collection')
	for bit in range(0, var.word_size):
		vb = uni.add_computation("variable_bit")
		if bool_string[bit] == '0':
			vb.extend(uni.false)
		elif bool_string[bit] == '1':
			vb.extend(uni.true)
		else:
			print('TODO: ADD EXCEPTION')
		bits.extend(vb)
	set_true = uni.add_computation('truth_collection')
	for x in range(0, var.word_size):
		true_compute = uni.add_computation('set_true')









def icopy(global_object, compute, statement):
	uni = global_object.universe
	copy = uni.add_computation("instruction")
	output =
