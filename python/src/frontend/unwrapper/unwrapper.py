
import src.model.structure as model
import copy

def unwrap(global_object):
	for sandbox in global_object.sandbox:
		for service in sandbox.service:
			sequence_out = list()
			for statement in service.sequence:
				unwrapped = unwrapped_element(sandbox.resolution)
				if is_assignment(statement):
					new_sequencing = unwrapped.unwrap_assignment(statement)
				sequence_out = sequence_out + new_sequencing
			service.sequence = sequence_out
	return global_object


def header_error(self):
	Exception('header error')


class unwrapped_element():

	def __init__(self, res):
		self.instr_order = list()
		self.res = res
		self.var_counter = 0


	def unwrap_assignment(self, assignment):
		if is_variable(assignment.arg[0]):
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
		if not is_variable(item):
			new_output_variable = self.generate_temporary_variable()
			self.unwrap(item, new_output_variable)
			return new_output_variable
		else:
			return item


	def generate_temporary_variable(self):
		name = 'temp' + str(self.var_counter)
		if name in self.res.variable_lookup:
			self.var_counter += 1
			return self.res.variable_lookup[name]
		else:
			temp = variable()
			temp.name = name
			self.res.variable_lookup[temp.name] = temp
			self.var_counter += 1
			return temp

