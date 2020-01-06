
alias = 'alias '
next = '; '


def request(op, var1='', var2='', word_size='', entropy='42'):
	seq_map = {
		'origin': gen_origin(entropy),
		'assignment': bin_gen('copy', var1, var2, word_size),
		'bitwise_or': bin_gen('bor', var1, var2, word_size),
		'bitwise_and': bin_gen('band', var1, var2, word_size),
		'bitwise_neg': un_gen('bneg', var1, word_size)
		}
	return seq_map[op]

def gen_origin(tail):
	origin_name = 'or' + tail
	origin_declaration = alias + origin_name + ' "'
	return origin_declaration, origin_name

def bin_gen(op, var1, var2, word_size):
	return var1 + var2 + op + word_size

def un_gen(op, var1, word_size):
	return var1 + op + word_size