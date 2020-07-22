import src.model.structure as model

def visualize(global_object):
	print('GLOBAL KEYBINDS: ')
	for bind in global_object.bind:
		print('BIND IS KEY "' + bind.value + '" BOUND TO EVENT "' + global_object.bind[bind].value + '"')
	print('GLOBAL MAPPINGS: ')
	for mapping in global_object.map:
		print('EVENT IS "' + mapping.value + '" MAPPED TO SERVICES: ' )
		for service in global_object.map[mapping]:
			print(service.identifier)
	for sandbox in global_object.sandbox:
		print('SANDBOX : ' + sandbox.name)
		print('WITH SERVICES:')
		for service in sandbox.service:
			print(service.name)
			print('WITH SEQUENCING:')
			for statement in service.sequence:
				print('STATEMENT ON "' + statement.identifier.name + '"')
				for arg in statement.arg:
					visualize_subexpression(arg)

def visualize_unwrapping(global_object):
	for sandbox in global_object.sandbox:
		print('SANDBOX: ' + sandbox.name)
		for service in sandbox.service:
			print('	SERVICE: ' + service.name)
			for ele in service.sequence:
				if is_unary_operator(ele):
					print('		' + ele.identity + ' ' + ele.arg[0].name + ' ' + ele.output.name)
				elif is_binary_operator(ele):
					print('		' + ele.identity + ' ' + ele.arg[0].name + ' ' + ele.arg[1].name + ' ' + ele.output.name)

def visualize_subexpression(arg, indentation_level=0):
	indent = '  ' * indentation_level
	if type(arg) == str:
		print(indent + 'PYTHON STRING: (' + '"' + arg + '")')
	elif model.is_variable(arg) and not is_constant(arg):
		print(indent + 'SCALU VARIABLE: "' + arg.name + '"')
	elif model.is_constant(arg):
		print(indent + 'SCALU CONSTANT: "' + arg.value + '"')
	elif model.is_binary_operator(arg):
		print(indent + 'BINARY OPERATOR: "' + arg.identity + '" WITH ARGS:')
		for sub_arg in arg.arg:
			visualize_subexpression(sub_arg, indentation_level + 1)
	elif model.is_unary_operator(arg):
		print(indent + 'UNARY OPERATOR: "' + arg.identity + '" WITH ARGS:')
		for sub_arg in arg.arg:
			visualize_subexpression(sub_arg, indentation_level + 1)
	elif model.is_literal_value(arg):
		print(indent + 'INTEGER VALUE: "' + arg.identity + '" WITH ARGS:')
		for sub_arg in arg.arg:
			visualize_subexpression(sub_arg, indentation_level + 1)


