import sys

version = "1.0"
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

def argcheck():
	build_types()
	if len(sys.argv) != 4:
		print("=" * 20)
		print("Corresponding SCALU build: " + version + "\n")
		print("vbuilder expects 3 positional arguments: name, word_size, type (e.g. vbuilder.py myvariablename 8 r)\n")
		print("Valid types: ")
		for type in types:
			print(type.short_form + " : " + type.long_form)
		print("=" * 20)
	else:
		generate()

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

def generate():
	varname = sys.argv[1]
	word_size = int(sys.argv[2])
	type = verify_type(sys.argv[3])
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
	for x in range(1, word_size + 1):
		out += "alias " + prefix + "b" + str(x) + " bfalse\n"
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
