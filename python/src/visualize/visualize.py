import src.model.structure as model

def visualize(global_object):
	print('GLOBAL MAPPINGS: ')
	for event in global_object.maps.maps:
		if event.key is not None:
			print('EVENT IS "' + event.string + '"BOUND TO "' + event.key + '"')
		print('EVENT IS "' + event.string + '" MAPPED TO SERVICES: ' )
		for service in event.services:
			print(service.identifier)
	for sandbox in global_object.sandbox:
		print('SANDBOX : ' + sandbox.name)
		print('WITH SERVICES:')
		for service in sandbox.services:
			print(service.name)
			print('WITH SEQUENCING:')
			for statement in service.sequence:
				if model.is_assignment(statement):
					print('STATEMENT ON "' + statement.identifier.name + '"')
					for arg in statement.arg:
						visualize_subexpression(arg)

def visualize_unwrapping(global_object):
	for sandbox in global_object.sandbox:
		print('SANDBOX: ' + sandbox.name)
		for service in sandbox.services:
			print('	SERVICE: ' + service.name)
			for ele in service.sequence:
				if model.is_unary_operator(ele):
					print('		' + ele.identity + ' ' + ele.arg[0].name + ' ' + ele.output.name)
				elif model.is_binary_operator(ele):
					print('		' + ele.identity + ' ' + ele.arg[0].name + ' ' + ele.arg[1].name + ' ' + ele.output.name)

def visualize_subexpression(arg, indentation_level=0):
	indent = '  ' * indentation_level
	if type(arg) == str:
		print(indent + 'PYTHON STRING: (' + '"' + arg + '")')
	elif model.is_variable(arg) and not model.is_constant(arg):
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


