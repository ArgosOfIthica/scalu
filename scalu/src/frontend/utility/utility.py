import math

def token_is_name(token):
    return token[0].isalpha()

def token_is_numeric(token):
    if token[0] == '-':
        return token[1:].isnumeric()
    else:
        return token.isnumeric()

def calc_min_word_size(old_word_size, value):
    return str(max(int(old_word_size), math.frexp(int(value))[1]))