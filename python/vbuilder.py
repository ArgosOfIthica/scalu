
"""vbuilder.py is a code writing utility for the scalu framework

Usage:
	vbuilder.py register <name> <word_size> [--value=<v>]
	vbuilder.py constant <name> <word_size> [--value=<v>]
	vbuilder.py batch <name> <word_size> ( -r | -c ) <size>
	vbuilder.py array <name> <word_size> ( -r | -c ) <size>
	vbuilder.py constants <word_size>
	vbuilder.py (-h | --help)
	vbuilder.py --version

Options:
	-h --help			Show usage
	--version			Show version
	--value=<v>			Value a variable will be generated with [default: 0]
	-r					Use the register subtype
	-c					Use the constant subtype
"""

from docopt import docopt

types = list()
version = "07162019"

class vartype():
	short_form = ""
	long_form = ""
	is_writable = False

def build_types():
	register = vartype()
	register.short_form = "r"
	register.long_form = "register"
	register.is_writable = True
	types.append(register)
	constant = vartype()
	constant.short_form = "c"
	constant.long_form = "constant"
	constant.is_writable = False
	types.append(constant)


def verify_word_size(word):
	word = int(word)
	assert(word > 2), "invalid word size"
	return word

def verify_type(input):
	input = input.lower()
	result = ""
	for type in types:
		if input == type.short_form:
			result = type
			break
		elif input == type.long_form:
			result = type
			break
	assert(result is not ""), "type could not be validated"
	return result

def verify_batch_size(size):
	size = int(size)
	assert(size > 0), "size must be positive integer"
	return size

def verify_array_size(size, word_size):
	size = int(size)
	word_size = int(word_size)
	assert(size <= int(2**word_size))
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
	build_types()
	if args.get("register"):
		type = verify_type("register")
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		value = 0
		if args.get("--value") is not None:
			value = verify_value(args.get("--value"), word_size)
		generate_variable(name, type, word_size, value)
	elif args.get("constant"):
		type = verify_type("constant")
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		value = 0
		if args.get("--value") is not None:
			value = verify_value(args.get("--value"), word_size)
		generate_variable(name, type, word_size, value)
	elif args.get("constants"):
		word_size = verify_word_size(args.get("<word_size>"))
		generate_all_constants(word_size)
	elif args.get("batch"):
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		size = verify_batch_size(args.get("<size>"))
		if args.get("-c"):
			subtype = verify_type("constant")
			generate_batch(name, subtype, word_size, size)
		if args.get("-r"):
			subtype = verify_type("register")
			generate_batch(name, subtype, word_size, size)
	elif args.get("array"):
		name = args.get("<name>")
		word_size = verify_word_size(args.get("<word_size>"))
		size = verify_array_size(args.get("<size>"), args.get("<word_size>"))
		if args.get("-c"):
			subtype = verify_type("constant")
			generate_array(name, subtype, word_size, size)
		if args.get("-r"):
			subtype = verify_type("register")
			generate_array(name, subtype, word_size, size)

def generate_all_constants(word_size):
	max_int = int(2 ** (word_size - 1))
	constant_type = verify_type("constant")
	for var in range( - max_int, max_int):
		varname = str(var)
		generate_variable(varname, constant_type, word_size, var)


def generate_array(varname, subtype, word_size, size):
	generate_batch(varname, subtype, word_size, size)

	def get_string(var):
		if var < size:
			return 'alias a' + varname + '_ret r' + varname + str(var) + '; '
		else:
			return ''
	generate_lookup_table('a' + varname, word_size, size, get_string)

def generate_batch(varname, subtype, word_size, size):
	for var in range(0, size):
		bname = varname + str(var)
		generate_variable(bname, subtype, word_size)


def generate_variable(varname, type, word_size, value = 0):
	prefix = type.short_form + varname


	#head
	out = "// ---" + type.long_form.upper() + " " + varname.upper() + " ( " + str(word_size) + " BIT; ver: " + version + " )\n\n"
	out += "alias " + prefix + "cb " + prefix + "b1\n"
	out += "alias " + prefix + "cr " + prefix + "r1\n"
	out += "alias " + prefix + "eb " + prefix + "b" + str(word_size) + "\n"
	if type.is_writable:
		out += "alias " + prefix + "cto " + prefix + "tr1\n"
		out += "alias " + prefix + "cfo " + prefix + "fr1\n"
	out += "alias flag_" + prefix + "_cycle ctrue\n\n"



	#interface
	if type.is_writable:
		out += 'alias ' + prefix + '_is_a "alias racycle ' + prefix + 'cr; alias default_t ' + prefix + 'cto; alias default_f ' + prefix + 'cfo; alias cycle_flag_alpha flag_' + prefix + '_cycle; alias flag_order beta; alias raend ' + prefix + 'eb"\n'
		out += 'alias ' + prefix + '_is_b "alias rbcycle ' + prefix + 'cr; alias cycle_flag_beta flag_' + prefix + '_cycle; alias rbend ' + prefix + 'eb"\n\n'
	else:
		out += 'alias ' + prefix + '_is_a "alias racycle ' + prefix + 'cr; alias default_t; alias default_f; alias cycle_flag_alpha flag_' + prefix + '_cycle; alias flag_order beta; alias raend ' + prefix + 'eb"\n'
		out += 'alias ' + prefix + '_is_b "alias rbcycle ' + prefix + 'cr; alias cycle_flag_beta flag_' + prefix + '_cycle; alias rbend ' + prefix + 'eb"\n\n'
		
	out += 'alias ' + prefix + '_init "alias alpha ' + prefix + '_is_a; alias beta ' + prefix + '_is_b; flag_order; alias ' + prefix + ' ' + prefix + 'cb; ' + prefix + 'cb"\n'
	out += 'alias ' + prefix + ' ' + prefix + '_init\n\n'



	#bit values
	bool_string = get_bin(value, word_size)
	for x in range(1, word_size + 1):
		if bool_string[len(bool_string) - x: len(bool_string) - x + 1] is "0":
			out += "alias " + prefix + "b" + str(x) + " bfalse\n"
		else:
			out += "alias " + prefix + "b" + str(x) + " btrue\n"
	out += "\n"



	#main rotary
	if type.is_writable:
		out += 'alias ' + prefix + 'r1 "alias ' + prefix + 'cb ' + prefix + 'b2; alias ' + prefix +'cr ' + prefix + 'r2; alias ' + prefix + 'cto ' + prefix + 'tr2; alias ' + prefix + 'cfo ' + prefix + 'fr2; alias flag_' + prefix + '_cycle cfalse"\n'
		for x in range(2, word_size):
			out += 'alias ' + prefix + 'r' + str(x) + ' "alias ' + prefix + 'cb ' + prefix + 'b' + str(x + 1) + '; alias ' + prefix +'cr ' + prefix + 'r' + str(x + 1) + '; alias ' + prefix + 'cto ' + prefix + 'tr' + str(x + 1) + '; alias ' + prefix + 'cfo ' + prefix + 'fr' + str(x + 1) + '"\n'
		out += 'alias ' + prefix + 'r' + str(word_size) + ' "alias ' + prefix + 'cb ' + prefix + 'b1; alias ' + prefix +'cr ' + prefix + 'r1; alias ' + prefix + 'cto ' + prefix + 'tr1; alias ' + prefix + 'cfo ' + prefix + 'fr1; alias flag_' + prefix + '_cycle ctrue; alias ' + prefix + ' ' + prefix + '_init"\n\n'
	else:
		out += 'alias ' + prefix + 'r1 "alias ' + prefix + 'cb ' + prefix + 'b2; alias ' + prefix +'cr ' + prefix + 'r2; alias flag_' + prefix + '_cycle cfalse"\n'
		for x in range(2, word_size):
			out += 'alias ' + prefix + 'r' + str(x) + ' "alias ' + prefix + 'cb ' + prefix + 'b' + str(x + 1) + '; alias ' + prefix +'cr ' + prefix + 'r' + str(x + 1) + '"\n'
		out += 'alias ' + prefix + 'r' + str(word_size) + ' "alias ' + prefix + 'cb ' + prefix + 'b1; alias ' + prefix +'cr ' + prefix + 'r1; alias flag_' + prefix + '_cycle ctrue; alias ' + prefix + ' ' + prefix + '_init"\n\n'



		#true rotary
	if type.is_writable:
		for x in range(1, word_size + 1):
			out += 'alias ' + prefix + 'tr' + str(x) + ' "alias ' + prefix + 'b' + str(x) + ' btrue"\n'
		out += '\n'



		#false rotary
		for x in range(1, word_size + 1):
			out += 'alias ' + prefix + 'fr' + str(x) + ' "alias ' + prefix + 'b' + str(x) + ' bfalse"\n'
		out += '\n'
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
	p = 1
	out += 'alias ' + prefix + '_ret\n'
	out += 'alias ' + prefix + '_ptr\n'
	out += 'alias ' + prefix + ' "alias btrue ' + prefix + '1; alias bfalse ' + prefix + '0; ' + pointer + '"\n\n'
	while p != word_size:
		for var in range(0, min(size, int(2**p))):
			out += 'alias ' + prefix + get_bin(var, p) + ' "rcycle; alias btrue ' + validate_true_branch(prefix, var, p, size) + '; alias bfalse ' + prefix + '0' + get_bin(var, p) + '; ' + pointer + '"\n'
		p += 1
		out += '\n'
	for var in range(0, size):
		out += 'alias ' + prefix + get_bin(var, p) + ' "' + custom_function(var) + 'rcycle; deinit"\n'

	#failure branches

	for branch in range(1, word_size):
		out += 'alias ' + prefix + 'fail' + str(branch) + ' "rcycle; ' + prefix + 'fail' + str(branch + 1) + '"\n'
	out += 'alias ' + prefix + 'fail' + str(word_size)
	print(out)




if __name__ == '__main__':
	args = docopt(__doc__, version=version)
	argcheck(args)