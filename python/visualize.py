from model.structure import *

def visualize(global_object):
	for sandbox in global_object.sandbox:
		print('SANDBOX : ' + sandbox.name)
		print('WITH SERVICES:')
		for service in sandbox.service:
			print(service.name)
			print('WITH ARGS:')
			for arg in service.arg:
				visualize_subexpression(arg)
			print('WITH SEQUENCING:')
			for statement in service.sequence:
				print('STATEMENT ON "' + statement.identifier.name + '"')
				print(statement.arg[0])
				for arg in statement.arg:
					visualize_subexpression(arg)

def visualize_unwrapping(block):
	for ele in block.sequence:
		if self.s.is_unary_operator(ele):
			print(ele.identity + ' ' + ele.arg[0].name + ' ' + ele.output.name)
		elif self.s.is_binary_operator(ele):
			print(ele.identity + ' ' + ele.arg[0].name + ' ' + ele.arg[1].name + ' ' + ele.output.name)

def visualize_subexpression(arg, indentation_level=0):
	indent = '  ' * indentation_level
	if type(arg) == str:
		print(indent + 'ARG IS PYTHON STRING: (' + '"' + arg + '")')
	elif is_variable(arg) and not is_constant(arg):
		print(indent + 'ARG IS SCALU VARIABLE: "' + arg.name + '"')
	elif is_constant(arg):
		print(indent + 'ARG IS SCALU CONSTANT: "' + arg.name + '"')
	elif is_binary_operator(arg):
		print(indent + 'ARG IS BINARY OPERATOR: "' + arg.identity + '" WITH ARGS:')
		for sub_arg in arg.arg:
			visualize_subexpression(sub_arg, indentation_level + 1)
	elif is_unary_operator(arg):
		print('ARG IS UNARY OPERATOR: "' + arg.identity + '" WITH ARGS:')
		for sub_arg in arg.arg:
			visualize_subexpression(sub_arg, indentation_level + 1)


