
import re
from backend.definitions.vbuilder import build_variable
from backend.definitions.instructions import generate_instructions
from backend.sequencer import generate_sequence


def generate(resolved_program):
	out, alias_set = generate_block_header(resolved_program)
	out += generate_block(resolved_program, alias_set)
	return out
	
def generation_error():
	print("generation error")
	
def generate_block_header(resolved_program):
	seq = resolved_program.sequence
	used_variables = set()
	seq = list(filter(lambda x: x.identity != 'variable' , seq))
	out = ''
	for ele in seq:
		if ele.family == 'binary':
			used_variables.add(ele.source)
			used_variables.add(ele.destination)
		elif ele.family == 'unary':
			used_variables.add(ele.destination)
		else:
			generation_error()
	out += generate_instructions(seq)
	for var in used_variables: #TODO replace this with a dedicated handler for vbuilder
		if var.type == 'int':
			out += build_variable(var.name, var.word_size, var.value)
	alias_set = set(re.findall('alias+\s(\w*)', out))
	resolved_program.sequence = seq
	return out, alias_set
	
def generate_block(resolved_program, alias_set):
	seq = generate_sequence(resolved_program.sequence, alias_set)
	return seq