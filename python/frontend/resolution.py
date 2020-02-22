
import copy
from frontend.parser.structure import variable

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
		if ele.identity == 'assignment':
			resolve_assignment(res, ele)
		elif ele.identity == 'service_call':
			resolve_service_call(res, ele)
		else:
			resolution_error()


def resolve_service_call(res, ele):
	core_services = ( 'bprint')
	for arg in range(0, len(ele.arg)):
		resolve_operator(res, ele, arg)
	if ele.service not in core_services:
		resolution_error()

def resolve_service_call_arg(res, ele):
	if type(ele.evaluate) is str:
		ele.evaluate = resolve_value(res, ele.evaluate)
	elif ele.evaluate.family == 'binary':
		resolve_binary(res, ele.evaluate)
	elif ele.evaluate.family == 'unary':
		resolve_unary(res, ele.evaluate)
	else:
		resolution_error()

def resolve_assignment(res, ele):
	ele.write = resolve_assignment_write(res, ele.write)
	resolve_assignment_evaluate(res, ele)

def resolve_assignment_write(res, write):
	if write in res.variable_lookup:
		return res.variable_lookup[write]
	else:
		new_variable = variable()
		new_variable.name = write
		res.variable_lookup[write] = new_variable


def resolve_operator(res, this, arg_index):
	if type(this.arg[arg_index]) is str:
		this.arg[arg_index] = resolve_value(res, this.arg[arg_index])
	elif this.arg[arg_index].family == 'binary':
		resolve_binary(res, this.arg[arg_index])
	elif this.arg[arg_index].family == 'unary':
		resolve_unary(res, this.arg[arg_index])
	else:
		resolution_error()

def resolve_assignment_evaluate(res, ele):
	if type(ele.evaluate) is str:
		ele.evaluate = resolve_value(res, ele.evaluate)
	elif ele.evaluate.family == 'binary':
		resolve_binary(res, ele.evaluate)
	elif ele.evaluate.family == 'unary':
		resolve_unary(res, ele.evaluate)
	else:
		resolution_error()

def resolve_unary(res, this):
	resolve_operator(res, this, 0)

def resolve_binary(res, this):
	resolve_operator(res, this, 0)
	resolve_operator(res, this, 1)



def resolve_value(res, token_string):

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
		if token_string in res.constant_lookup:
			return res.constant_lookup[token_string]
		else:
			new_constant = generate_constant(token_string)
			res.constant_lookup[token_string] = new_constant
			return new_constant


def generate_constant(value):
	constant = variable()
	constant.identity = 'constant'
	constant.name = value
	constant.value = value
	return constant
