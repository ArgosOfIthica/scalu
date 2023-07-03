import re

def tokenize(program):
    split_program = split_on_word(program)
    tokens = to_tokens(split_program)
    return tokens

class token():

    def __init__(self, value, line):
        self.value = value
        self.line = line

def split_on_word(program):
    return re.split('(\/\*[\s\S]*?\*\/|\[[\s\S]*?(?<!\\\)\]|-\w+|\+\w+|\+\?|>>|<<|<=|>=|!=|==|\W)', program)
    #this regex splits on comments, console blocks, negative events, positive events, and various operators

def to_tokens(split_program):
    tokens = list()
    newline_count = 1
    for token_string in split_program:
        if token_string == '\n':
            newline_count += 1
        elif token_string.isspace() or token_string == '':
            pass
        elif token_string[0] == '[':
            newline_count += tokenize_source_call(tokens, token_string)
        elif token_string[0] == '/' and token_string[1] == '*':
            newline_count += tokenize_comments(tokens, token_string)
        else:
            tokens.append(token(token_string, newline_count))
    return tokens

def tokenize_source_call(tokens, token_string):
    newline_count = 0
    for char in token_string:
        if char == '\n':
            newline_count += 1
    new_token = token(token_string[0], newline_count)
    tokens.append(new_token)
    new_token = token(token_string[1:-1], newline_count)
    tokens.append(new_token)
    new_token = token(token_string[-1], newline_count)
    tokens.append(new_token)
    return newline_count

def tokenize_comments(tokens, token_string):
    newline_count = 0
    for i in range(len(token_string)):
        if token_string[i] == '\n':
            newline_count += 1
    if token_string[-1] != '/' or token_string[-2] != '*':
        raise Exception('Comment was not terminated. Last valid token is """' + tokens[-1].value + '""" at line ' + tokens[-1].line)
    return newline_count

