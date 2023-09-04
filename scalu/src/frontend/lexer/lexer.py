import re
from typing import List

class Token():

    def __init__(self, value: str, line: int):
        self.value = value
        self.line = line


class Tokenizer():

    def __init__(self):
        self.tokens: List[Token] = list()
        self.newline_count: int = 1

    def tokenize(self, program: str) -> List[Token]:
        split_program = self.split_on_word(program)
        self.to_tokens(split_program)
        return self.tokens

    def split_on_word(self, program: str) -> List[str]:
        return re.split('(\/\*[\s\S]*?\*\/|\[[\s\S]*?(?<!\\\)\]|-\w+|\+\w+|\+\?|>>|<<|<=|>=|!=|==|\W)', program)
        #this regex splits on comments, console blocks, negative events, positive events, and various operators

    def to_tokens(self, split_program: List[str]):
        for token_string in split_program:
            if token_string == '\n':
                self.newline_count += 1
            elif token_string.isspace() or token_string == '':
                pass
            elif token_string[0] == '[':
                self.tokenize_source_call(token_string)
            elif token_string[0] == '/' and token_string[1] == '*':
                self.tokenize_comments(token_string)
            else:
                self.tokens.append(Token(token_string, self.newline_count))

    def tokenize_source_call(self, token_string: str):
        for char in token_string:
            if char == '\n':
                self.newline_count += 1
        open_bracket = Token(token_string[0], self.newline_count)
        self.tokens.append(open_bracket)
        content = Token(token_string[1:-1], self.newline_count)
        self.tokens.append(content)
        close_bracket = Token(token_string[-1], self.newline_count)
        self.tokens.append(close_bracket)

    def tokenize_comments(self, token_string: str):
        for i in range(len(token_string)):
            if token_string[i] == '\n':
                self.newline_count += 1
        if token_string[-1] != '/' or token_string[-2] != '*':
            raise Exception('Comment was not terminated. Last valid token is """' + self.tokens[-1].value + '""" at line ' + str(self.tokens[-1].line))
