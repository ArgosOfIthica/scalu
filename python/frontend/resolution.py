
import copy
from frontend.parser.structure import variable

class resolution_block():
	variable_lookup = dict()
	service_lookup = dict()
	constant_lookup = dict()


class resolver():

	def __init__(self):
		self.res = resolution_block()

	def resolve(self, shallow_ast):
		self.resolve_block(shallow_ast)
		return shallow_ast


	def resolution_error(self):
		raise Exception("Resolution error")


	def resolve_block(self, block):
		for ele in block.sequence:
			if ele.identity == 'assignment':
				self.resolve_assignment(ele)
			elif ele.identity == 'service_call':
				self.resolve_service_call(ele)
			else:
				self.resolution_error()


	def resolve_service_call(self, ele):
		core_services = ( 'bprint')
		for arg in range(0, len(ele.arg)):
			self.resolve_operator(ele, arg)
		if ele.service not in core_services:
			self.resolution_error()

	def resolve_assignment(self, ele):
		ele.write = self.resolve_assignment_write(ele.write)
		self.resolve_assignment_evaluate(ele)

	def resolve_assignment_write(self, write):
		if write in self.res.variable_lookup:
			return self.res.variable_lookup[write]
		elif type(write) == str:
			new_variable = variable()
			new_variable.name = write
			self.res.variable_lookup[write] = new_variable
			return new_variable
		else:
			self.resolution_error()


	def resolve_operator(self, ele):
		ele.arg = [self.resolve_operator_transform(arg) for arg in ele.arg]

#combine rot and rae
	def resolve_operator_transform(self, arg):
		if type(arg) is str:
			return self.resolve_value(arg)
		elif arg.family == 'binary' or arg.family == 'unary':
			self.resolve_operator(arg)
		else:
			self.resolution_error()

	def resolve_assignment_evaluate(self, ele):
		if type(ele.evaluate) is str:
			ele.evaluate = self.resolve_value(ele.evaluate)
		elif ele.evaluate.family == 'binary' or arg.family == 'unary':
			self.resolve_operator(ele.evaluate)
		else:
			self.resolution_error()

	def resolve_value(self, token_string):

		def token_is_name(token):
			return token[0].isalpha()

		def token_is_numeric(token):
			if token[0] == '-':
				return token[1:].isnumeric()
			else:
				return token.isnumeric()

		if token_is_name(token_string):
			return self.res.variable_lookup[token_string]
		elif token_is_numeric(token_string):
			if token_string in self.res.constant_lookup:
				return self.res.constant_lookup[token_string]
			else:
				new_constant = self.generate_constant(token_string)
				self.res.constant_lookup[token_string] = new_constant
				return new_constant


	def generate_constant(self, value):
		constant = variable()
		constant.identity = 'constant'
		constant.name = value
		constant.value = value
		return constant
