from enum import Enum
import re

def tokenize(prog_string):
    for char in prog_string:
        pass


def preprocess(prog_string):
    tokens = tokenize(prog_string)
    proc = Preprocessor(tokens)
    print(tokens)
    iter_count = 0
    ITER_MAX = 10000
    process_token(proc)
    while len(proc.tokens) > 1 and iter_count < ITER_MAX:
        proc.delete()
        iter_count += 1
        process_token(proc)
    return ''.join(proc.cleared_tokens)

def process_token(proc):
    if proc.is_nominal():
        proc.process()
    elif proc.mode == '#clear':
        process_clear(proc)
    elif proc.mode == '#deep':
        process_deep(proc)
    elif proc.mode == '#wide':
        process_wide(proc)

def process_clear(proc):
    if proc.token() in proc.builtins:
        proc.mode = proc.token()
        process_builtin(proc)
    else:
        proc.tokens = proc.spawn_user_macro() + proc.tokens

def process_deep(proc):
    if proc.token() != '#save':
        proc.queue += proc.spawn_user_macro()
    elif proc.token() == '#save':
        proc.macros[proc.active_macro] = proc.queue
        proc_queue = list()
        proc.mode = '#clear'

def process_wide(proc):
    max_macro_size = 1
    if proc.token() != '#save':
        proc.queue.append(proc.spawn_user_macro())
    elif proc.token() == '#save':
        pass

def process_builtin(proc):
    if proc.mode == '#wide' or proc.mode == '#deep':
        proc.delete()
        if not proc.is_nominal() and proc.token() not in proc.builtins and proc.token() not in proc.macros:
            proc.active_macro = proc.token()
        else:
            raise Exception('bad macro')
    elif proc.mode == '#save':
        raise Exception('cannot use #save here')

class Preprocessor():

    def __init__(self, tokens):
        self.builtins = ('#deep', '#wide', '#save', '#clear')
        self.mode = '#clear'
        self.tokens = tokens
        self.cleared_tokens = list()
        self.macros = dict()
        self.active_macro = ''
        self.queue = list()

    def is_nominal(self):
        if len(self.token()) > 1:
            return self.tokens[0] != '#' or self.tokens[1] == '#'
        else:
            return True

    def token(self):
        return self.tokens[0]

    def delete(self):
        del self.tokens[0]
    
    def process(self):
        self.clear(self.token())
    
    def clear(self, nominal_token):
        if len(self.token()) > 1 and nominal_token[0] == '#' and nominal_token[1] == '#':
            nominal_token = nominal_token[1:]
        self.cleared_tokens.append(nominal_token) 
    
    def forward(self):
        self.queue.append(self.tokens[0])
    
    def spawn_user_macro(self):
        macro_list = self.macros[self.token()]
        computed_list = list()
        for ele in macro_list:
            if len(self.token()) > 1 and ele[0] == '#' and ele[1] == '#':
                computed_list.append(ele[:1])
            elif len(self.token()) > 1 and ele[0] == '#':
                computed_list.append(self.macros[ele]) #check for exceptions
            else:
                computed_list.append(ele)
        return computed_list
  