from enum import Enum
import re


def preprocess(prog_string):
    token_col = Tokenizer().tokenize(prog_string)
    proc = Sable(token_col)
    result = proc.compute()
    return ''.join(proc.cleared_tokens)


class Tokenizer():

    def tokenize(self, prog_string):
        self.WHITESPACE = (' ', '\t', '\n')
        self.SYMBOL = '#'
        self.prog_string = prog_string
        self.tc = Token_Collection(prog_string)
        self.string_collector = ''
        self.macro_stage = 0
        self.type_collector = ''
        for char in prog_string:
            if self.macro_stage == 0:
                self.detect_symbol(char)
            elif self.macro_stage == 1:
                self.detect_escape(char)
            elif self.macro_stage == 2:
                self.detect_macro_end(char)
        self.tc.append(Token(self.string_collector, self.type_collector))
        return self.tc

    def detect_symbol(self, char):
        self.type_collector = 'string'
        if char != self.SYMBOL:
            self.string_collector += char
        elif char == self.SYMBOL:
            self.macro_stage = 1

    def detect_escape(self, char):
        if char != self.SYMBOL:
            self.tc.add_token(string_collector, 'string')
            self.string_collector = self.SYMBOL + char
            self.type_collector = 'macro'
            self.macro_stage = 2
        elif char == self.SYMBOL or char in self.WHITESPACE:
            self.string_collector.append(char)
            self.macro_stage = 0

    def detect_macro_end(self, char):
            if char in self.WHITESPACE:
                tc.add_token(string_collector, 'macro')
                string_collector = char
                self.macro_stage = 0
            elif char == '#':
                string_collector.append(char)
                tc.add_token(string_collector, 'macro')
                string_collector = str()
                self.macro_stage = 0
            else:
                string_collector.append(char)


class Token_Collection(list):

    def add_token(self, value, token_type):
        self.append(Token(value, token_type))

class Token():

    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type

class Sable_State():

    def __init__(self, proc):
        self.proc = proc

    def update_state(self):
        self.proc.previous_state = self.proc.current_state
        self.proc.current_state = self

    def process(self):
        if self.proc.is_nominal():
            self.process_nominal()
        elif self.proc.is_macro():
            self.process_macro()

    def process_nominal():
        self.proc.process()
    
    def process_macro(self):
        self.proc.match(proc.token()).update_state()
    
    def transition(self):
        allowed = self.allowed()
        if self.proc.previous_state in allowed:
            self.initial_process()
            while len(self.proc.tokens != 0) and self.proc.current_state == self:
                self.process()
        else:
            raise Exception('an exception')

    def initial_process(self):
        pass

class Clear(Sable_State):

    def allowed(self):
        return (Save, Clear)

class Macro(Sable_State):

    def process_nominal():
        self.proc.forward()

    def initial_process(self):
        if self.proc.token().token_type == 'macro' and not self.proc.token().value[0].is_numeric():
            self.proc.active_macro = self.proc.current_token()
            self.proc.delete()
        else:
            raise Exception('macro declaration not properly named')
    
    def allowed(self):
        return (Clear)

class Deep(Macro):
    pass

class Wide(Macro):
    pass

class Unprocessed(Sable_State):

    def initial_process(self):
        self.proc.tokens = self.value + self.proc.tokens
        self.proc.current_state = self.proc.previous_state
        self.proc.previous_state = self.proc.clear
    
    def process(self):
        raise Exception('process should be unreachable from custom macro')

class Custom(Unprocessed):

    def __init__(self, value):
        super.__init__()
        self.value = Tokenizer().tokenize(value)


class Sequence(Unprocessed):

    def __init__(self, recipe):
        super.__init__()
        self.recipe = recipe
        self.value = None
    
    def initial_process(self):
        if self.value is None:
            self.construct_value()


class Sequence_Construct():

    def __init__(self, recipe):
        self.recipe = recipe
        self.empty = False
        self.reversed = False

    def build_sequence(self):
        self.parse()
        return self.create()

    def parse(self):
        extracted_number = ''
        for char in self.recipe:
            if char.is_numeric():
                extracted_number.append(char)
            else:
                break
        for char in self.recipe:
            if char == 'e':
                self.empty = True
            elif char == 'r':
                self.reversed = True
    
    def create(self):
        iterable = [_ for _ in range(int(extracted_number))]
        if self.reversed:
            iterable = iterable.reverse()
        
            


class Sable():

    def __init__(self, tc):
        #setup builtins
        self.clear = Clear()
        self.deep = Deep()
        self.wide = Wide()
        self.save = Save()
        self.macros = {
            'deep' : self.deep,
            'wide' : self.wide,
            'save' : self.save
        }
        #FSM machinery
        self.previous_state = self.clear
        self.current_state = self.clear
        #tokens
        self.tokens = tc
        self.cleared_tokens = list()
        self.active_macro = ''
        self.queue = list()
    
    def compute(self):
        while len(self.tokens) != 0:
            self.mode.transition()

    def is_nominal(self):
        return self.current_token().token_type == 'string'

    def is_macro(self):
        return self.current_token().token_type == 'macro'

    def current_token(self):
        return self.tokens[0]

    def delete(self):
        del self.tokens[0]
    
    def process(self):
        self.cleared_tokens.append(self.current_token().value)
        self.delete()
    
    def forward(self):
        self.queue.append(self.current_token())
        self.delete()
    
    def match(self, token):
        if token.value in self.macros:
            return self.macros[token.value]
        if token.value[0].is_numeric():
            pass
        else:
            raise Exception('cannot find')
        