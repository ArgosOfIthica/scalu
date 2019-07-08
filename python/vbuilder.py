import sys

version = "07082019"
types = list()

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
	batch = vartype()
	batch.short_form = "b"
	batch.long_form = "batch"
	types.append(batch)
	all_constants = vartype()
	all_constants.short_form = "ac"
	all_constants.long_form = "all_constants"
	types.append(all_constants)


def argcheck():
	build_types()
	if len(sys.argv) < 4:
		print("=" * 20)
		print("Corresponding SCALU build: " + version + "\n")
		print("vbuilder always expects at least 3 positional arguments: type, name, word_size\n")
		print("If type is register or constant, vbuilder expects 1 additional argument: value (e.g. vbuilder.py r myvariablename 8 42)\n")
		print("If type is batch, vbuilder expects 2 additional arguments: subtype (r,c), size (e.g. vbuilder.py b myvariablename 8 r 6)\n")
		print("Valid types: ")
		for type in types:
			print(type.short_form + " : " + type.long_form)
		print("=" * 20)
	else:
		process_arguments()

def verify_word_size(word):
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

def verify_batch_size(size, word_size):
	assert(size > 0), "size must be positive integer"
	return size

def verify_value(value, word_size):
	max_int = int((2**word_size) / 2)
	assert(value < max_int ), "value is higher than maximum value"
	assert(value >= -max_int ), "value is lower than minimum value"
	return value

get_bin = lambda x, n: format(x, 'b').zfill(n)


def process_arguments():
	type = verify_type(sys.argv[1])
	varname = sys.argv[2]
	word_size =  verify_word_size(int(sys.argv[3]))
	if type.long_form is "batch":
		generate_batch(varname, type, word_size)
	elif type.long_form is "all_constants":
		generate_all_constants(word_size)
	else:
		value = verify_value(int(sys.argv[4]), word_size)
		generate_variable(varname, type, word_size, value)

def generate_all_constants(word_size):
	max_int = int((2 ** word_size) / 2)
	constant_type = types[1]
	for var in range( - max_int, max_int):
		varname = str(var)
		generate_variable(varname, constant_type, word_size, var)


def generate_batch(varname, type, word_size):
	subtype = verify_type(sys.argv[4])
	size = verify_batch_size(int(sys.argv[5]), word_size)
	assert(subtype.long_form is "register" or "constant"), "unsupported batch type"
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

argcheck()
