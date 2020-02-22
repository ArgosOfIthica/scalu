
import copy

class resolution_block():
	variable_lookup = dict()
	service_lookup = dict()
	constant_lookup = dict()


def resolve(global_object):
	res = resolution_block()
	resolve_block(global_object, res)
	return global_object


def resolution_error():
	raise Exception("Resolution error")


def resolve_block(block, res):
	for ele in block.sequence:
		if ele.identity == 'variable':
			resolve_variable(res, ele)
		elif ele.identity == 'assignment':
			resolve_assignment(res, ele)
		elif ele.identity == 'service_call':
			resolve_service_call(res, ele)
		else:
			resolution_error()


def resolve_variable(res, ele):
	if ele.name not in res.variable_lookup:
		res.variable_lookup[ele.name] = ele
	else:
		resolution_error()


def resolve_service_call(res, ele):
	core_services = ( 'bprint')
	print(ele.service)
	if ele.service not in core_services:
		resolution_error()

def resolve_assignment(res, ele):
	ele.write = resolve_assignment_write(res, ele.write)
	resolve_assignment_evaluate(res, ele)

def resolve_assignment_write(res, write):
	if write in res.variable_lookup:
		return res.variable_lookup[write]
	else:
		resolution_error()


def resolve_operator(res, this, write, arg_index):
	if type(this.arg[arg_index]) is str:
		this.arg[arg_index] = resolve_value(res, this.arg[arg_index], write)
	elif this.arg[arg_index].family == 'binary':
		resolve_binary(res, this.arg[arg_index], write)
	elif this.arg[arg_index].family == 'unary':
		resolve_unary(res, this.arg[arg_index], write)
	else:
		resolution_error()

def resolve_assignment_evaluate(res, ele):
	write = ele.write
	evaluate = ele.evaluate
	if type(evaluate) is str:
		ele.evaluate = resolve_value(res, ele.evaluate, write)
	elif evaluate.family == 'binary':
		resolve_binary(res, evaluate, write)
	elif evaluate.family == 'unary':
		resolve_unary(res, evaluate, write)
	else:
		resolution_error()

def resolve_unary(res, this, write):
	resolve_operator(res, this, write, 0)

def resolve_binary(res, this, write):
	resolve_operator(res, this, write, 0)
	resolve_operator(res, this, write, 1)



def resolve_value(res, token_string, write):

	def token_is_name(token):
		return token[0].isalpha()

	def token_is_numeric(token):
		if token[0] == '-':
			return token[1:].isnumeric()
		else:
			return token.isnumeric()

	if token_is_name(token_string):
		return res.variable_lookup[token_string]
	elif token_is_numeric(token_string):
		constant_trace = (token_string, write.word_size)
		if constant_trace in res.constant_lookup:
			return res.constant_lookup[constant_trace]
		else:
			new_constant = generate_constant(token_string, write)
			res.constant_lookup[constant_trace] = new_constant
			return new_constant


def generate_constant(value, template):
	constant = copy.deepcopy(template)
	constant.identity = 'constant'
	constant.name = value
	constant.value = value
	return constant
