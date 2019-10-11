
import vbuilder

alias = "alias "
true = "btrue "
false = "bfalse "
true_return = "gt"
false_return = "gf"
alpha_bit = "ga"
beta_bit = "gb"
next = "; "
new = '\n'

def sandboxed_ascii(var):
	if (var >= 33 and var <= 37) or (var >= 39 and var <= 57) or (var >= 60 and var <= 127):
		return chr(var)
	else:
		return 'ascii' + str(var)

def icopy(word_size):
	out = 'alias copy "'
	for word in range(0, word_size):
		out += alias + true + true_return + str(word) + next + alias + false + false_return + str(word) + next + beta_bit + str(word)
		if word != word_size - 1:
			out += next
	out += '"'
	return out


def idump(word_size):
	out = alias + 'dump "'
	out += alias + true + 'echo 1' + next + alias + false + 'echo 0' + next
	for word in range(0, word_size):
		out += alpha_bit + str(word)
		if word != word_size - 1:
			out += next
	out += '"'
	return out


#hex instruction is not generated if word size < 4
def ihexdump(word_size):
	def hd_label(num):
		if num > 0:
			return 'hdc' + str(num) + '_'
		else:
			return 'hd'
	
	def hex_bootstrap(x):
		def hex_modifier(z):
			if z == 0:
				return str(z + 4 * x) + next + hd_label(x + 1)
			else:
				return str(z + 4 * x)
		return hex_modifier

	out = ''
	for x in range(0, int(word_size / 4)):
		out += vbuilder.build_lookup(hd_label(x), word_size, 16, hex, hex_bootstrap(x))
	out += alias + hd_label(int(word_size/4)) 
	return out

def ibitwise_or(word_size):
	out = ''
	for x in range(0, word_size):
		out += alias + 'bor_false_branch' + str(x) + ' "' + alias + true + true_return + str(x) + next + alias + false + false_return + str(x) + next + beta_bit + str(x) + '"' + new
	out += new + alias + 'bor "'
	for x in range(0, word_size):
		out += alias + true + true_return + str(x) + next + alias + false + 'bor_false_branch' + str(x) + next + alpha_bit + str(x)
		if x != word_size - 1:
			out += next
	out += '"'
	return out

def ibitwise_and(word_size):
	out = ''
	for x in range(0, word_size):
		out += alias + 'band_true_branch' + str(x) + ' "' + alias + true + true_return + str(x) + next + alias + false + false_return + str(x) + next + beta_bit + str(x) + '"' + new
	out += new + alias + 'band "'
	for x in range(0, word_size):
		out += alias + true + 'band_true_branch' + str(x) + next + alias + false + false_return + str(x) + next + alpha_bit + str(x)
		if x != word_size - 1:
			out += next
	out += '"'
	return out

