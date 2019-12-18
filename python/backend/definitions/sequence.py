
alias = 'alias '
next = '; '


def request(op, var1='', var2='', word_size='', entropy='42', optimize=''):
	seq_map = {
		'origin': gen_origin(entropy),
		'assignment': arg2_optimize('copy', var1, var2, word_size, optimize),
		'bitwise_or': arg2_optimize('bor', var1, var2, word_size, optimize),
		'bitwise_and': arg2_optimize('band', var1, var2, word_size, optimize)
		}
	return seq_map[op]

def gen_origin(tail):
	origin_name = 'or' + tail
	origin_declaration = alias + origin_name + ' "'
	return origin_declaration, origin_name

def arg2_optimize(op, var1, var2, word_size, optimize):
	if optimize == 'ab':
		return op + word_size
	elif optimize == 'a':
		return var2 + '_is_b' + next + op + word_size
	elif optimize == 'b':
		return var1 + '_is_a' + next + op + word_size
	else:
		return var1 + '_is_a' + next + var2 + '_is_b' + next + op + word_size