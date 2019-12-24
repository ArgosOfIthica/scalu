
from backend.definitions.sequence import request
import random

alias_name_length = 31
console_max_buffer = 510
random_max = 9223372036854775806
next = '; '

def generate_sequence(sequence, alias_set):
	random.seed(42)
	new_origin = origin(alias_set)
	register_a = ''
	register_b = ''
	optimize_string = ''
	out = new_origin
	for ele in sequence:
		if ele.family == 'binary':
			if (register_a == ele.destination.name) and (register_b == ele.source.name):
				optimize_string = 'ab'
			elif (register_a == ele.destination.name):
				optimize_string = 'a'
			elif (register_b == ele.source.name):
				optimize_string = 'b'
			else:
				optimize_string = ''
			out += request(op = ele.identity, var1 = ele.destination.name, var2 = ele.source.name, word_size = ele.destination.word_size, optimize = optimize_string) + next
			register_a = ele.destination.name
		elif ele.family == 'unary':
			if (register_a == ele.destination.name):
				optimize_string = 'a'
			else:
				optimize_string = ''
			out += request(op = ele.identity, var1 = ele.destination.name, word_size = ele.destination.word_size, optimize = optimize_string) + next
			register_a = ele.destination.name

	out += '"'
	return out


def origin(alias_set):
	seq_seed = str(random.randint(0, random_max))
	new_origin, new_origin_name = request(op='origin', entropy=seq_seed)
	while new_origin_name in alias_set:
		seq_seed = str(random.randint(0, random_max))
		new_origin, new_origin_name = request(op='origin', entropy=seq_seed)
	alias_set.add(new_origin_name)
	return new_origin