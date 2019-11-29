
import re
from backend.definitions.vbuilder import build_variable
from backend.definitions.instructions import generate_instructions
from backend.sequencer import generate_sequence


def generate(resolved_program):
	out = ''
	seq = list()
	def generate_block_header():
		seq = resolved_program.sequence
		used_instructions = set()
		used_variables = set()
		seq = list(filter(lambda x: x.identity != 'variable' , seq))
		out = ''
		for ele in seq:
			if ele.identity == 'assignment':
				used_variables.add(ele.source)
				used_variables.add(ele.destination)
				used_instructions.add((ele.identity, ele.destination.word_size))
		out += generate_instructions(used_instructions)
		for var in used_variables: #TODO replace this with a dedicated handler for vbuilder
			if var.type == 'int':
				out += build_variable(var.name, var.word_size, var.value)
		alias_set = set(re.findall('alias+\s(\w*)', out))
		resolved_program.sequence = seq
		return out, alias_set
	
	def generate_block():
		seq = generate_sequence(resolved_program.sequence, alias_set)
		return seq

	out, alias_set = generate_block_header()
	out += generate_block()
	return out