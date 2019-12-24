
import copy

class resolution_block():
	variable_lookup = dict()
	constant_lookup = set()

def resolve(global_object):
	res = resolution_block()
	validate_block(global_object, res)
	resolve_block(global_object, res)
	return global_object


def resolution_error():
	raise Exception("Resolution error")


def validate_block(block, res):
	for ele in block.sequence:
		if ele.identity == "variable":
			validate_variable(res, ele)
		elif ele.family == "binary":
			validate_binary(res, ele)
		elif ele.family == "unary":
			validate_unary(res, ele)
		else:
			resolution_error()


def resolve_block(block, res):
	for ele in block.sequence:
		if ele.family == "binary":
			resolve_binary(res, ele)
		elif ele.family == "unary":
			resolve_unary(res, ele)


def validate_variable(res, ele):
	if ele.name not in res.variable_lookup:
		res.variable_lookup[ele.name] = ele
	else:
		resolution_error()


def validate_unary(res, ele):
	if ele.destination not in res.variable_lookup:
		resolution_error()

def validate_binary(res, ele):
	if ele.is_literal and (ele.destination in res.variable_lookup):
		res.constant_lookup.add((res.variable_lookup[ele.destination].type, ele.source))
	elif ele.source not in res.variable_lookup or ele.destination not in res.variable_lookup:
		resolution_error()

def resolve_unary(res, ele):
	ele.destination = res.variable_lookup[ele.destination]

def resolve_binary(res, ele):
	if ele.is_literal:
		ele.destination = res.variable_lookup[ele.destination]
		literal = copy.deepcopy(ele.destination)
		literal.name = ele.source
		literal.value = ele.source
		ele.source = literal
	else:
		ele.destination = res.variable_lookup[ele.destination]
		ele.source = res.variable_lookup[ele.source]