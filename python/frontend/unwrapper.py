
from frontend.parser.structure import unary_operator
from frontend.parser.structure import variable
from frontend.parser.structure import structure
import copy

class unwrapper():

	def __init__(self):
		self.s = structure()
		self.sequence_out = list()

	def unwrap(self, block):
		for item in block.sequence:
			if self.s.is_assignment(item):
				unwrapped = unwrapped_assignment(block.resolution)
				new_sequencing = unwrapped.unwrap_assignment(item)
				self.sequence_out = self.sequence_out + new_sequencing
		block.sequence = self.sequence_out
		return block
	def header_error(self):
		Exception('header error')




class unwrapped_assignment():

	def __init__(self, res):
		self.instr_order = list()
		self.res = res
		self.var_counter = 0
		self.s = structure()

	def unwrap_assignment(self, assignment):
		variable_headers = ''
		out = ''
		if self.s.is_variable(assignment.arg[0]):
			icopy = unary_operator()
			icopy.identity = 'copy'
			icopy.arg[0] = assignment.arg[0]
			icopy.output = assignment.identifier
			self.instr_order.append(icopy)
		else:
			self.unwrap(assignment.arg[0], assignment.identifier)
		return self.instr_order

	def unwrap(self, item, output_variable):
		item.output = output_variable
		item.arg = [self.unwrap_transform(arg, output_variable) for arg in item.arg]
		self.instr_order.append(item)

	def unwrap_transform(self, item, output_variable):
		if not self.s.is_variable(item):
			new_output_variable = self.generate_temporary_variable()
			self.unwrap(item, new_output_variable)
			return new_output_variable
		else:
			return item


	def generate_temporary_variable(self):
		temp = variable()
		temp.name = 'temp' + str(self.var_counter)
		self.res.variable_lookup[temp.name] = temp
		self.var_counter += 1
		return temp

