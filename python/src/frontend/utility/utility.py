def token_is_name(token):
	return token[0].isalpha()

def token_is_numeric(token):
	if token[0] == '-':
		return token[1:].isnumeric()
	else:
		return token.isnumeric()
