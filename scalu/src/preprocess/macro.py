
import platform
import re

def compile(program):
    engine = MacroEngine()
    engine.reset()
    return engine.run(program)

class MacroEngine():

    def reset(self):
        self.variables = dict()
        self.templates = dict()
        self.run_preamble()

    def run(self, program):
        return re.sub('(?:#def |#write |#reset )[\w\W]*?##', lambda match: self.process(match), program)

    def process(self, match):
        macro = match.group(0)
        macro = macro.split()
        return self.outer_function(macro)
    
    def clean(self, macro):
        return ' '.join(macro[1:]).rstrip('#')

    def outer_function(self, macro):
        if macro[0] == '#def':
            self.define(macro[1:])
            return ''
        elif macro[0] == '#write':
            return self.write(self.clean(macro))
        elif macro[0] == '#reset':
            self.reset()
            return ''

    def define(self, macro):
        macro_type = macro[0]
        if macro_type == 'var':
            self.expect_var(macro[1:])
        elif macro_type == 'template':
            self.expect_template(macro[1:])
        elif macro_type == 'generate':
            self.expect_generate(macro[1:])
        else:
            raise Exception('invalid macro type')
    
    def expect_template(macro):
        pass
    
    def expect_generate(macro):
        pass

    def write(self, macro):
        output = self.expand_vars(macro)
        return output
            
    def expect_var(self, macro):
        name = macro[0]
        value = self.expand_vars(self.clean(macro))
        self.variables[name] = value
    
    def expand_vars(self, macro):
        return re.sub('#[a-zA-Z0-9_\-]+', lambda match: self.expand_var(match), macro)
    
    def expand_var(self, match):
        macro = match.group(0)
        return self.variables.get(macro.strip('#'), '')

    def verify(test_word, verify_word):
        if (test_word != verify_word):
            raise Exception('critical error')
    
    def run_preamble(self):
        preamble = '''
        #def var scalu_version 1.1.1##
        #def var scalu_machine '''+ platform.machine() +'''##
        #def var scalu_system '''+ platform.system() +'''##
        #def var scalu_language python3##
        #def var scalu_python_implementation '''+ platform.python_implementation() +'''##
        #def var scalu_python_version '''+ platform.python_version() +'''##
        '''
        self.run(preamble)