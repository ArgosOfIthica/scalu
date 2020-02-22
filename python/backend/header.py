
from backend.definitions.vbuilder import build_variable
from frontend.parser.structure import unary_operator
import copy

class header_generator():

	def __init__(self, program):
		self.program = program
		self.header_out = ''
		self.sequence = list()


	def process(self):
		for ele in self.program.sequence:
			self.request(ele)

	def header_error():
		Exception('header error')

	def request(self, item):
		if item.family == 'variable':
			if item.type == 'int':
				self.header_out += build_variable(item.name, item.word_size, item.value)
			else:
				header_error()
		elif item.family == 'assignment':
			unwrapper = unwrapped_assignment(item)
			unwrapped_assignment_object, temp_headers = unwrapper.unwrap_assignment()
			for elem in temp_headers:
				self.request(elem)
			self.sequence = self.sequence + unwrapped_assignment_object


class unwrapped_assignment():
	family = 'wrapper'
	identity = 'wrapper'

	def __init__(self, assignment):
		self.assignment = assignment
		self.instr_order = list()
		self.new_headers = list()
		self.var_counter = 0


	def unwrap(self, item, output_variable, arg_index):
		item.output = output_variable
		if not item.arg[arg_index].family == 'variable':
			new_output_variable = self.generate_temporary_variable()
			if item.arg[arg_index].family == 'unary':
				self.unwrap_unary(item.arg[arg_index], new_output_variable)
			elif item.arg[arg_index].family == 'binary':
				self.unwrap_binary(item.arg[arg_index], new_output_variable)
			else:
				header_error()
			item.arg[arg_index] = new_output_variable


	def unwrap_assignment(self):
		item = self.assignment
		variable_headers = ''
		out = ''
		if item.evaluate.family == 'variable':
			icopy = unary_operator()
			icopy.identity = 'copy'
			icopy.arg1 = item.evaluate
			icopy.output = item.write
			self.instr_order.append(icopy)
		elif item.evaluate.family == 'unary':
			self.unwrap_unary(item.evaluate, item.write)
		elif item.evaluate.family == 'binary':
			self.unwrap_binary(item.evaluate, item.write)
		return self.instr_order, self.new_headers

	def unwrap_unary(self, item, output_variable):
		self.unwrap(item, output_variable, 0)
		self.instr_order.append(item)



	def unwrap_binary(self, item, output_variable):
		self.unwrap(item, output_variable, 0)
		self.unwrap(item, output_variable, 1)
		self.instr_order.append(item)



	def generate_temporary_variable(self):
		temp = copy.deepcopy(self.assignment.write)
		temp.name = 'temp' + str(self.var_counter)
		self.var_counter += 1
		self.new_headers.append(temp)
		return temp

