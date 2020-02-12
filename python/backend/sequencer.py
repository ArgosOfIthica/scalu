
from backend.definitions.instructions import build_instruction
import random

class sequence_generator():
	sequence = ''
	header = ''
	alias_name_length = 31
	console_max_buffer = 510
	random_max = 9223372036854775806
	next = '; '

	def generate_sequence(self, raw_sequence, alias_set):

		random.seed(42)
		self.sequence = self.origin(alias_set)
		for ele in raw_sequence:
			new_header, new_sequence = build_instruction(ele)
			self.header += new_header
			self.sequence += new_sequence
		self.sequence += '"'


	def origin(self, alias_set):
		seq_seed = str(random.randint(0, self.random_max))
		new_origin, new_origin_name = gen_origin(seq_seed)
		while new_origin_name in alias_set:
			seq_seed = str(random.randint(0, random_max))
			new_origin, new_origin_name = gen_origin(seq_seed)
		alias_set.add(new_origin_name)
		return new_origin



def gen_origin(tail):
	alias = 'alias '
	next = '; '
	origin_name = 'or' + tail
	origin_declaration = alias + origin_name + ' "'
	return origin_declaration, origin_name
