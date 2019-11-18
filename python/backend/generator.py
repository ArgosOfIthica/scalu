
import re
from backend.definitions.vbuilder import build_variable
from backend.definitions.instructions import generate_instructions
def generate(resolved_program):
	out = ''
	def generate_block_header():
		seq = resolved_program.sequence
		used_instructions = set()
		used_variables = set()
		seq = list(filter(lambda x: x.identity != 'variable' , seq))
		out = ''
		for ele in resolved_program.sequence:
			if ele.identity == 'assignment':
				used_variables.add(ele.source)
				used_variables.add(ele.destination)
				used_instructions.add((ele.identity, ele.destination.word_size))
		out += generate_instructions(used_instructions)
		for var in used_variables:
			if var.type == 'int':
				out += build_variable(var.name, var.word_size, var.value)
		return out
	
	def generate_block():
		seq = resolved_program.sequence
		out = ''
		for ele in seq:
			pass
		return out
	
	out += generate_block_header()
	out += generate_block()
	return out