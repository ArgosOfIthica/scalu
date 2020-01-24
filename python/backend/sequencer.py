
from backend.definitions.sequence import request
import random

alias_name_length = 31
console_max_buffer = 510
random_max = 9223372036854775806
next = '; '

def generate_sequence(sequence, alias_set):
	random.seed(42)
	new_origin = origin(alias_set)
	out = new_origin
	for ele in sequence:
		if ele.family == 'binary':
			out += request(op = ele.identity, var1 = ele.destination.name, var2 = ele.source.name, word_size = ele.destination.word_size) + next
		elif ele.family == 'unary':
			out += request(op = ele.identity, var1 = ele.destination.name, word_size = ele.destination.word_size) + next
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