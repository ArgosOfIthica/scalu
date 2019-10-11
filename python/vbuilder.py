types = list()
version = "10102019"


#global types

types.append('int')

#global strings

alias = 'alias '
next = '; '


#externalize functions

def build_variable(varname, word_size, value):
	varname = verify_varname(varname)
	word_size = verify_word_size(word_size)
	value = verify_value(value, word_size)
	return generate_variable(varname, word_size, value)

def build_array(varname, word_size, size, type = 'int', import_list = None):
	varname = verify_varname(varname)
	word_size = verify_word_size(word_size)
	size = verify_size(size, word_size)
	type = verify_array_type(type)
	if import_list is not None:
		import_list = verify_array_list(size, import_list)
	return generate_array(varname, word_size, size, type, import_list)


def build_lookup(varname, word_size, size, operation, register_modifier = lambda x: str(x)):
	varname = verify_varname(varname)
	word_size = verify_word_size(word_size)
	size = verify_size(size, word_size)
	return generate_lookup_table(varname, word_size, size, operation, register_modifier)

#verification functions

def verify_varname(varname):
	assert(len(varname) < 8), "varname length greater than maximum"
	assert(len(varname) > 0), "varname must have non-zero length"
	return varname

def verify_word_size(word):
	word = int(word)
	assert(word > 2), "invalid word size"
	return word

def verify_batch_size(size):
	size = int(size)
	assert(size > 0), "size must be positive integer"
	return size

def verify_size(size, word_size):
	size = int(size)
	word_size = int(word_size)
	assert(size <= int(2**word_size)), "size must be representable by word_size"
	return size

def verify_value(value, word_size):
	value = int(value)
	max_int = int(2**(word_size - 1))
	assert(value < max_int ), "value is higher than maximum value"
	assert(value >= -max_int ), "value is lower than minimum value"
	return value

def verify_array_type(type):
	assert(types.index(type) is not None), "invalid array type"
	return type

def verify_array_list(size, lst):
	assert(len(lst) <= size), "imported list length is greater than internal size"
	return lst

def verify_int_array(word_size, lst):
	for x in range(0,len(lst)):
		assert(lst[x] == int(lst[x])), "elements in imported list must be of type int"
		assert(lst[x] <= get_max_int(word_size)), "imported integer list has value greater than maximum integer"
		assert(lst[x] >= get_min_int(word_size)), "imported integer list has value less than minimum integer"

#utility functions

def get_bin(value, bit_size):
	return format(value, 'b').zfill(bit_size)

def get_max_int(word_size):
	return int(2**(word_size - 1) - 1)

def get_min_int(word_size):
	return int(2**(word_size - 1) * -1)

#generation functions

def generate_array(varname, word_size, size, type, incoming_list):
	alpha_register = 'ga'
	beta_register = 'gb'
	array_varname = 'a' + varname
	if type == 'int':
		if incoming_list is not None:
			verify_int_array(word_size, incoming_list)
		out = generate_batch(varname, word_size, size, incoming_list)
		

		def get_endpoint_string(var):
			return alias + array_varname + '_ret_alpha ' + varname + str(var) + '_is_a' + next + alias + array_varname + '_ret_beta ' + varname + str(var) + '_is_b'
		
		out += alias + array_varname + '_ret_alpha\n'
		out += alias + array_varname + '_ret_beta\n'
		out += generate_lookup_table(array_varname, word_size, size, get_endpoint_string)
		return out

def generate_batch(varname, word_size, size, incoming_list):
	out = ''
	if incoming_list is not None:
		for var in range(0, size):
			bname = varname + str(var)
			if len(incoming_list) >= var:
				out += generate_variable(bname, word_size, incoming_list[var])
			else:
				out += generate_variable(bname, word_size)
	else:
		for var in range(0, size):
			bname = varname + str(var)
			out += generate_variable(bname, word_size)
	out += '\n'
	return out

def generate_variable(varname, word_size, value):
	prefix = varname
	alpha_register = 'ga'
	beta_register = 'gb'
	return_true = 'gt'
	return_false = 'gf'
	true = ' btrue'
	false = ' bfalse'


	def generate_binder(bind_string, register, binding_prefix):
		out = alias + prefix + bind_string + ' "'
		for x in range(0, word_size - 1):
			out += alias + register + str(x) + ' ' + prefix + binding_prefix + str(x) + next
		out += alias + register + str(word_size - 1) + ' ' + prefix + binding_prefix + str(word_size - 1) + '"\n\n'
		return out


	out = '// ---VARIABLE ' + varname + ' ( ' + str(word_size) + ' BIT, ver: ' + version + ' )\n'
	out += alias + prefix + '_is_a "' + prefix + '_bind_val_a' + next + prefix + '_bind_true' + next + prefix + '_bind_false"\n'
	out += alias + prefix + '_is_b ' + prefix + '_bind_val_b\n\n'

	out += generate_binder('_bind_val_a', alpha_register, 'b')
	out += generate_binder('_bind_val_b', beta_register, 'b')
	out += generate_binder('_bind_true', return_true, 'tr')
	out += generate_binder('_bind_false', return_false, 'fr')

	bool_string = get_bin(value, word_size)
	for x in range(1, word_size + 1):
		if bool_string[len(bool_string) - x: len(bool_string) - x + 1] is "0":
			out += alias + prefix + "b" + str(x - 1) + false + '\n'
		else:
			out += alias + prefix + "b" + str(x - 1) + " btrue\n"
	out += "\n"

	for x in range(0, word_size):
		out += alias + prefix + 'tr' + str(x) + ' "' + alias + prefix + 'b' + str(x) + true +'"\n'
	out += '\n'

	for x in range(0, word_size):
		out += alias + prefix + 'fr' + str(x) + ' "' + alias + prefix + 'b' + str(x) + false +'"\n'

	return out


def generate_lookup_table(prefix, word_size, size, custom_function, modifier):
	global_register = 'ga'
	true = 'btrue '
	false = 'bfalse '
	out = ""
	word_increment = 0


	def validate_true_branch(prefix, var, p, size):
		new_branch = int(2**p) + var
		if new_branch >= size:
			return prefix + 'fail'
		else:
			return prefix + '1' + get_bin(var, p)


	def generate_layer():
		nonlocal word_increment
		out = ''
		for var in range(0, min(size, int(2**word_increment))):
			out += alias + prefix + get_bin(var, word_increment) + ' "' + alias + true + validate_true_branch(prefix, var, word_increment, size) + next + alias + false + prefix + '0' + get_bin(var, word_increment) + next + global_register + modifier(word_increment) + '"\n'
		word_increment += 1
		out += '\n'
		return out

	out += alias + prefix + ' "' + alias + true + prefix + '1' + next + alias + false + prefix + '0' + next + global_register + modifier(word_increment) + '"\n\n'
	word_increment += 1
	while word_increment != word_size and int(2**word_increment) < size:
		out += generate_layer()
	for var in range(0, size):
		out += alias + prefix + get_bin(var, word_increment) + ' "' + custom_function(var) + '"\n'

	out += alias + prefix + 'fail\n'
	return out