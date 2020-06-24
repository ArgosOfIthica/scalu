
from backend.definitions.instructions import instruction_constructor
import random



'''
class sequence_generator():
	alias_name_length = 31
	random_max = 9223372036854775806
	next = '; '

	def generate_sequence(self, global_object, alias_set=set()):
		random.seed(42)
		instr_constr = instruction_constructor()
		bundle = self.sequence_bundle()
		bundle.sequence = self.origin(alias_set)
		for ele in raw_sequence:
			instr_bundle = instr_constr.build_instruction(ele)
			bundle.header += instr_bundle.header
			bundle.sequence += instr_bundle.sequence
		bundle.sequence += '"'
		return bundle


	def origin(self, alias_set):
		seq_seed = str(random.randint(0, self.random_max))
		new_origin, new_origin_name = gen_origin(seq_seed)
		while new_origin_name in alias_set:
			seq_seed = str(random.randint(0, random_max))
			new_origin, new_origin_name = gen_origin(seq_seed)
		alias_set.add(new_origin_name)
		return new_origin

	class sequence_bundle():
		header = ''
		sequence = ''



def gen_origin(tail):
	alias = 'alias '
	next = '; '
	origin_name = 'or' + tail
	origin_declaration = alias + origin_name + ' "'
	return origin_declaration, origin_name
'''
