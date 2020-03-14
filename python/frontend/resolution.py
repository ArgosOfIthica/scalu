
import copy
from frontend.utility.utility import *
from frontend.parser.structure import constant
from frontend.parser.structure import variable
from frontend.parser.structure import structure
from frontend.service_definitions.service import core_service_resolver

class resolution_block():
	variable_lookup = dict()
	service_lookup = dict()
	constant_lookup = dict()


class resolver():

	def __init__(self):
		self.res = resolution_block()
		self.s = structure()
		self.core = core_service_resolver()

	def resolve(self, shallow_ast):
		self.resolve_block(shallow_ast)
		return shallow_ast


	def resolution_error(self):
		raise Exception("Resolution error")


	def resolve_block(self, block):
		for ele in block.sequence:
			if self.s.is_assignment(ele):
				self.resolve_assignment(ele)
			elif self.s.is_service_call(ele):
				self.resolve_service_call(ele)
			else:
				self.resolution_error()

	def resolve_service_call(self, ele):
		ele.identifier = self.resolve_service_call_write(ele.identifier)
		self.resolve_operator(ele)

	def resolve_service_call_write(self, write):
		if write in self.core.core_service_list():
			return self.core.get_service_object(write)
		else:
			self.resolution_error()

	def resolve_assignment(self, ele):
		ele.identifier = self.resolve_assignment_write(ele.identifier)
		self.resolve_operator(ele)

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

	def resolve_operator_transform(self, arg):
		if type(arg) is str:
			return self.resolve_value(arg)
		elif self.s.is_operator(arg):
			self.resolve_operator(arg)
			return arg
		else:
			self.resolution_error()

	def resolve_value(self, token_string):
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
		constant_val = constant()
		constant_val.identity = 'constant'
		constant_val.name = value
		constant_val.value = value
		return constant_val
