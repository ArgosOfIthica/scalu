from frontend.parser.structure import *

class visualizer():

	def __init__(self):
		self.s = structure()


	def visualize(self, block):
		for ele in block.sequence:
			print('STATEMENT ON "' + ele.identifier.name + '"')
			for arg in ele.arg:
				self.visualize_subexpression(arg)

	def visualize_unwrapping(self, block):
		for ele in block.sequence:
			if self.s.is_unary_operator(ele):
				print(ele.identity + ' ' + ele.arg[0].name + ' ' + ele.output.name)
			elif self.s.is_binary_operator(ele):
				print(ele.identity + ' ' + ele.arg[0].name + ' ' + ele.arg[1].name + ' ' + ele.output.name)

	def visualize_subexpression(self, arg, indentation_level=0):
		indent = '  ' * indentation_level
		if type(arg) == str:
			print(indent + 'ARG IS PYTHON STRING: (' + '"' + arg + '")')
		elif self.s.is_variable(arg) and not self.s.is_constant(arg):
			print(indent + 'ARG IS SCALU VARIABLE: "' + arg.name + '"')
		elif self.s.is_constant(arg):
			print(indent + 'ARG IS SCALU CONSTANT: "' + arg.name + '"')
		elif self.s.is_binary_operator(arg):
			print(indent + 'ARG IS BINARY OPERATOR: "' + arg.identity + '" WITH ARGS:')
			for sub_arg in arg.arg:
				self.visualize_subexpression(sub_arg, indentation_level + 1)
		elif self.s.is_unary_operator(arg):
			print('ARG IS UNARY OPERATOR: "' + arg.identity + '" WITH ARGS:')
			for sub_arg in arg.arg:
				self.visualize_subexpression(sub_arg, indentation_level + 1)


