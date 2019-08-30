
"""vbuilder.py is a code writing utility for the scalu framework

Usage:
	vbuilder.py variable <name> <word_size> [--value=<v>]
	vbuilder.py batch <name> <word_size> <size>
	vbuilder.py array <name> <word_size> <size>
	vbuilder.py constants <word_size>
	vbuilder.py (-h | --help)
	vbuilder.py --version

Options:
	-h --help			Show usage
	--version			Show version
	--value=<v>			Value a variable will be generated with [default: 0]
"""

from docopt import docopt

types = list()
version = "08292019"


#global types

types.append('int')

#global strings

alias = 'alias '
next = '; '


#externalize functions

def generate_variable_external(varname, word_size, value):
	varname = verify_varname(varname)
	word_size = verify_word_size(word_size)
	value = verify_value(value, word_size)
	generate_variable(varname, word_size, value)

def generate_array_external(varname, word_size, size, type = 'int', import_list = None):
	varname = verify_varname(varname)
	word_size = verify_word_size(word_size)
	size = verify_array_size(size, word_size)
	type = verify_array_type(type)
	if import_list is not None:
		import_list = verify_array_list(size, import_list)
	generate_array(varname, word_size, size, type, import_list)

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

def verify_array_size(size, word_size):
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
		assert(lst[x] <= get_max_int(word_size)), "imported integer list has value greater than maximum integer"
		assert(lst[x] >= get_min_int(word_size)), "imported integer list has value less than minimum integer"

def get_bin(value, bit_size):
	return format(value, 'b').zfill(bit_size)

def get_max_int(word_size):
	return int(2**(word_size - 1) - 1)

def get_min_int(word_size):
	return int(2**(word_size - 1) * -1)


def argcheck(args):
	if args.get("variable"):
		name = verify_varname(args.get("<name>"))
		word_size = verify_word_size(args.get("<word_size>"))
		value = 0
		if args.get("--value") is not None:
			value = verify_value(args.get("--value"), word_size)
		generate_variable(name, word_size, value)
	elif args.get("constants"):
		word_size = verify_word_size(args.get("<word_size>"))
		generate_all_constants(word_size)
	elif args.get("batch"):
		name = verify_varname(args.get("<name>"))
		word_size = verify_word_size(args.get("<word_size>"))
		size = verify_batch_size(args.get("<size>"))
		generate_batch(name, word_size, size)
	elif args.get("array"):
		name = verify_varname(args.get("<name>"))
		word_size = verify_word_size(args.get("<word_size>"))
		size = verify_array_size(args.get("<size>"), args.get("<word_size>"))
		generate_array(name, word_size, size)

def generate_all_constants(word_size):
	max_int = int(2 ** (word_size - 1))
	for var in range( - max_int, max_int):
		varname = str(var)
		generate_variable(varname, word_size, var)


def generate_array(varname, word_size, size, type = 'int', incoming_list = None):
	alpha_register = 'ga'
	beta_register = 'gb'
	array_varname = 'a' + varname
	if type == 'int':
		verify_int_array(word_size, incoming_list)
		generate_batch(varname, word_size, size, incoming_list)

		def get_endpoint_string(var):
			return alias + array_varname + '_ret_alpha ' + varname + str(var) + '_is_a' + next + alias + array_varname + '_ret_beta ' + varname + str(var) + '_is_b'

		generate_lookup_table('a' + varname, word_size, size, get_endpoint_string)

def generate_batch(varname, word_size, size, incoming_list = None):
	if incoming_list is not None:
		for var in range(0, size):
			bname = varname + str(var)
			if len(incoming_list) >= var:
				generate_variable(bname, word_size, incoming_list[var])
			else:
				generate_variable(bname, word_size)
	else:
		for var in range(0, size):
			bname = varname + str(var)
			generate_variable(bname, word_size)

def generate_variable(varname, word_size, value = 0):
	prefix = varname
	alpha_register = 'ga'
	beta_register = 'gb'
	return_true = 'gt'
	return_false = 'gf'
	true = ' btrue'
	false = ' bfalse'


	out = '// ---VARIABLE ' + varname + ' ( ' + str(word_size) + ' BIT, ver: ' + version + ' )\n'
	out += alias + prefix + '_is_a "' + prefix + '_bind_val_a' + next + prefix + '_bind_true' + next + prefix + '_bind_false"\n'
	out += alias + prefix + '_is_b ' + prefix + '_bind_val_b\n\n'


	out += alias + prefix + '_bind_val_a "'
	for x in range(0, word_size - 1):
		out += alias + alpha_register + str(x) + ' ' + prefix + 'b' + str(x) + next
	out += alias + alpha_register + str(word_size - 1) + ' ' + prefix + 'b' + str(word_size - 1) + '"\n\n'


	out += alias + prefix + '_bind_val_b "'
	for x in range(0, word_size - 1):
		out += alias + beta_register + str(x) + ' ' + prefix + 'b' + str(x) + next
	out += alias + beta_register + str(word_size - 1) + ' ' + prefix + 'b' + str(word_size - 1) + '"\n\n'


	out += alias + prefix + '_bind_true "'
	for x in range(0, word_size - 1):
		out += alias + return_true + str(x) + ' ' + prefix + 'tr' + str(x) + next
	out += alias + return_true + str(word_size - 1) + ' ' + prefix + 'tr' + str(word_size - 1) + '"\n\n'


	out += alias + prefix + '_bind_false "'
	for x in range(0, word_size - 1):
		out += alias + return_false + str(x) + ' ' + prefix + 'fr' + str(x) + next
	out += alias + return_false + str(word_size - 1) + ' ' + prefix + 'fr' + str(word_size - 1) + '"\n\n'


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
	
	print(out)

#lookup tables

def validate_true_branch(prefix, var, p, size):
	new_branch = int(2**p) + var
	if new_branch > size:
		return prefix + 'fail'
	else:
		return prefix + '1' + get_bin(var, p)


def generate_lookup_table(prefix, word_size, size, custom_function):
	global_register = 'ga'
	true = 'btrue'
	false = 'bfalse'
	out = ""
	word_increment = 1
	out += alias + prefix + '_ret_alpha\n'
	out += alias + prefix + '_ret_beta\n'
	out += alias + prefix + ' "' + alias + 'btrue ' + prefix + '1; alias bfalse ' + prefix + '0; ' + global_register + '0' + '"\n\n'
	while word_increment != word_size:
		for var in range(0, min(size, int(2**word_increment))):
			out += alias + prefix + get_bin(var, word_increment) + ' "' + alias + 'btrue ' + validate_true_branch(prefix, var, word_increment, size) + '; alias bfalse ' + prefix + '0' + get_bin(var, word_increment) + '; ' + global_register + str(word_increment) + '"\n'
		word_increment += 1
		out += '\n'
	for var in range(0, size):
		out += alias + prefix + get_bin(var, word_increment) + ' "' + custom_function(var) + '"\n'

	out += alias + prefix + 'fail'
	print(out)