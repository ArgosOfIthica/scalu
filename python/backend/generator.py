
import re
from backend.definitions.instructions import build_instruction
from backend.sequencer import sequence_generator
from backend.header import header_generator

def generate(resolved_program):
	header = ''
	sequence = ''
	header_gen = header_generator(resolved_program)
	header_gen.process()
	header = header_gen.header_out
	alias_set = set(re.findall('alias+\s(\w*)', header))
	uncompiled_sequence = header_gen.sequence
	sequence_gen = sequence_generator()
	sequence_gen.generate_sequence(uncompiled_sequence, alias_set)
	header += sequence_gen.header
	sequence = sequence_gen.sequence
	return header + sequence
