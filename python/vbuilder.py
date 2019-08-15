
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
version = "08072019"


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

def get_bin(value, bit_size):
	return format(value, 'b').zfill(bit_size)

def argcheck(args):
	if args.get("variable"):
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		value = 0
		if args.get("--value") is not None:
			value = verify_value(args.get("--value"), word_size)
		generate_variable(name, word_size, value)
	elif args.get("constants"):
		word_size = verify_word_size(args.get("<word_size>"))
		generate_all_constants(word_size)
	elif args.get("batch"):
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		size = verify_batch_size(args.get("<size>"))
		generate_batch(name, word_size, size)
	elif args.get("array"):
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		size = verify_array_size(args.get("<size>"), args.get("<word_size>"))
		generate_array(name, word_size, size)

def generate_all_constants(word_size):
	max_int = int(2 ** (word_size - 1))
	for var in range( - max_int, max_int):
		varname = str(var)
		generate_variable(varname, word_size, var)


def generate_array(varname, word_size, size):
	generate_batch(varname, word_size, size)

	def get_endpoint_string(var):
		return 'alias a' + varname + '_ret r' + varname + str(var) + '; '

	generate_lookup_table('a' + varname, word_size, size, get_endpoint_string)

def generate_batch(varname, word_size, size):
	for var in range(0, size):
		bname = varname + str(var)
		generate_variable(bname, word_size)


def generate_variable(varname, word_size, value = 0):
	prefix = varname
	
	out = '// ---VARIABLE ' + varname + ' ( ' + str(word_size) + ' BIT, ver: ' + version + ' )\n'
	out += 'alias ' + prefix + '_is_a "' + prefix + '_bind_val_a; ' + prefix + '_bind_true; ' + prefix + '_bind_false"\n'
	out += 'alias ' + prefix + '_is_b ' + prefix + '_bind_val_b\n\n'


	out += 'alias ' + prefix + '_bind_val_a "'
	for x in range(0, word_size - 1):
		out += 'alias ga' + str(x) + ' ' + prefix + 'b' + str(x) + '; '
	out += 'alias ga' + str(word_size - 1) + ' ' + prefix + 'b' + str(word_size - 1) + '"\n\n'


	out += 'alias ' + prefix + '_bind_val_b "'
	for x in range(0, word_size - 1):
		out += 'alias gb' + str(x) + ' ' + prefix + 'b' + str(x) + '; '
	out += 'alias gb' + str(word_size - 1) + ' ' + prefix + 'b' + str(word_size - 1) + '"\n\n'


	out += 'alias ' + prefix + '_bind_true "'
	for x in range(0, word_size - 1):
		out += 'alias gt' + str(x) + ' ' + prefix + 'tr' + str(x) + '; '
	out += 'alias gt' + str(word_size - 1) + ' ' + prefix + 'tr' + str(word_size - 1) + '"\n\n'


	out += 'alias ' + prefix + '_bind_false "'
	for x in range(0, word_size - 1):
		out += 'alias gf' + str(x) + ' ' + prefix + 'fr' + str(x) + '; '
	out += 'alias gf' + str(word_size - 1) + ' ' + prefix + 'fr' + str(word_size - 1) + '"\n\n'


	bool_string = get_bin(value, word_size)
	for x in range(1, word_size + 1):
		if bool_string[len(bool_string) - x: len(bool_string) - x + 1] is "0":
			out += "alias " + prefix + "b" + str(x - 1) + " bfalse\n"
		else:
			out += "alias " + prefix + "b" + str(x - 1) + " btrue\n"
	out += "\n"
	
	for x in range(0, word_size):
		out += 'alias ' + prefix + 'tr' + str(x) + ' "alias ' + prefix + 'b' + str(x) + ' btrue"\n'
	out += '\n'
	
	for x in range(0, word_size):
		out += 'alias ' + prefix + 'fr' + str(x) + ' "alias ' + prefix + 'b' + str(x) + ' bfalse"\n'
	
	print(out)



def validate_true_branch(prefix, var, p, size):
	new_branch = int(2**p) + var
	if new_branch > size:
		return prefix + 'fail' + str(p)
	else:
		return prefix + '1' + get_bin(var, p)


def generate_lookup_table(prefix, word_size, size, custom_function):
	out = ""
	pointer = prefix + '_ptr'
	word_increment = 1
	out += 'alias ' + prefix + '_ret\n'
	out += 'alias ' + prefix + '_ptr\n'
	out += 'alias ' + prefix + ' "alias btrue ' + prefix + '1; alias bfalse ' + prefix + '0; ' + pointer + '"\n\n'
	while word_increment != word_size:
		for var in range(0, min(size, int(2**word_increment))):
			out += 'alias ' + prefix + get_bin(var, word_increment) + ' "rcycle; alias btrue ' + validate_true_branch(prefix, var, word_increment, size) + '; alias bfalse ' + prefix + '0' + get_bin(var, word_increment) + '; ' + pointer + '"\n'
		word_increment += 1
		out += '\n'
	for var in range(0, size):
		out += 'alias ' + prefix + get_bin(var, word_increment) + ' "' + custom_function(var) + 'rcycle; deinit"\n'

	#failure branches

	for branch in range(1, word_size):
		out += 'alias ' + prefix + 'fail' + str(branch) + ' "rcycle; ' + prefix + 'fail' + str(branch + 1) + '"\n'
	out += 'alias ' + prefix + 'fail' + str(word_size)
	print(out)


if __name__ == '__main__':
	args = docopt(__doc__, version=version)
	argcheck(args)