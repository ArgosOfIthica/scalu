
import platform
import re

def compile(program):
    engine = MacroEngine()
    engine.setup()
    return engine.run(program)

class MacroEngine():

    def __init__(self):
        self.variables = dict()
        self.functions = dict()
    
    def setup(self):
        self.reset()

    def run(self, program):
        return re.sub('(?:#def |#write |#reset )[\w\W]*?##', lambda match: self.process(match), program)

    def process(self, match):
        macro = match.group(0)
        macro = macro.split()
        macro = self.outer_function(macro)

    def outer_function(self, macro):
        if macro[0] == '#def':
            self.define(macro[1:])
            return ''
        elif macro[0] == '#write':
            return self.write(strip(macro[1:], '#'))
        elif macro[0] == '#reset':
            self.reset()
            return ''

    def define(self, macro):
        macro_type = macro[0]
        if macro_type == 'var':
            self.expect_var(macro[:1])
        elif macro_type == 'template':
            self.expect_template(macro[:1])
        elif macro_type == 'generate':
            self.expect_generate(macro[:1])
        else:
            raise Exception('invalid macro type')
    
    def expect_template(macro):
        pass
    
    def expect_generate(macro):
        pass

    def write(self, macro):
        return self.variables.get(macro, '')
    
    def reset(self):
        self.variables = dict()
        self.functions = dict()
        self.run_preamble()
            
    def expect_var(self, macro):
        name = macro[0]
        return re.sub('#[a-zA-Z0-9]+', lambda match: self.expand_vars(match), ' '.join(macro))
    
    def expand_vars(self, match):
        macro = match.group(0)
        return self.get_var(strip(macro, '#'))

    def get_var(self, var_name):
        if var_name in variables:
            return self.variables[var_name]
        else:
            return ''

    def verify(test_word, verify_word):
        if (test_word != verify_word):
            raise Exception('critical error')
    
    def run_preamble(self):
        preamble = '''
        #def var scalu_version 1.1.1##
        #def var machine '''+ platform.machine() +'''##
        #def var system '''+ platform.system() +'''##
        #def var python_implementation '''+ platform.python_implementation() +'''##
        #def var python_version '''+ platform.python_version() +'''##
        '''
        self.run(preamble)