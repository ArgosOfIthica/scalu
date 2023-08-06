
import platform
import re
import scalu.src.cli.arg_handling as arg_handler

def compile(program):
    engine = MacroEngine()
    engine.reset()
    if arg_handler.args.enablemacros or arg_handler.args.mode[0] == 'test':
        return engine.run(program)
    else:
        return program

class MacroEngine():

    def reset(self):
        self.variables = dict()
        self.variables['empty'] = ''
        self.templates = dict()
        self.run_preamble()

    def run(self, program):
        return re.sub('(?:#def |#write |#reset )[\w\W]*?##', lambda match: self.process(match), program)

    def process(self, match):
        macro = match.group(0)
        macro = macro.split()
        return self.outer_function(macro)
    
    def clean(self, macro):
        return ' '.join(macro).rstrip('#')

    def outer_function(self, macro):
        if macro[0] == '#def':
            self.define(macro[1:])
            return ''
        elif macro[0] == '#write':
            return self.write(self.clean(macro[1:]))
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
    
    def expect_generate(self, macro):
        name = macro[0]
        template = macro[1]
        modifier = macro[2]
        argument = self.expand_vars(self.clean(macro[3:]))
        if modifier == 'special':
            result = self.special_template(template, argument)
            self.variables[name] = result

    def expect_var(self, macro):
        name = macro[0]
        value = self.expand_vars(self.clean(macro[1:]))
        self.variables[name] = value

    def write(self, macro):
        output = self.expand_vars(macro)
        return output
    
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
        #def var scalu_credits ArgosOfIthica, tmob03, getchoo
        #def var scalu_git https://github.com/ArgosOfIthica/scalu##
        '''
        preamble += self.load_standard_lib()
        self.run(preamble)
    
    def special_template(self, template, argument):
        if template == 'range':
            ranges = argument.split()
            ranges = [int(x) for x in ranges]
            result = list(range(ranges[0], ranges[1], ranges[2]))
            result = [str(x) for x in result]
            result = ' '.join(result)
            return result
    
    def load_standard_lib(self):
        std = '''
        #def var std_print '''+ self.std_print() +'''##
        #def var std_bitshift_right '''+ self.std_bitshift_right() +'''##
        #def var std_bitshift_left '''+ self.std_bitshift_left() +'''##
        #def var std_rng '''+ self.std_rng() +'''##
        #def var std_multiply '''+ self.std_multiply() +'''##
        #def var std_divide '''+ self.std_divide() +'''##
        #def var std_pow '''+ self.std_pow() +'''##
        #def var std_sqrt '''+ self.std_sqrt() +'''##
        '''
        return std


    def std_print(self):
        return '''service std_print { jump (std_input1) { {[echo 0]} {[echo 1]} {[echo 2]} {[echo 3]} {[echo 4]} {[echo 5]} {[echo 6]} {[echo 7]} {[echo 8]} {[echo 9]} {[echo 10]} {[echo 11]} {[echo 12]} {[echo 13]} {[echo 14]} {[echo 15]} {[echo 16]} {[echo 17]} {[echo 18]} {[echo 19]} {[echo 20]} {[echo 21]} {[echo 22]} {[echo 23]} {[echo 24]} {[echo 25]} {[echo 26]} {[echo 27]} {[echo 28]} {[echo 29]} {[echo 30]} {[echo 31]} {[echo 32]} {[echo 33]} {[echo 34]} {[echo 35]} {[echo 36]} {[echo 37]} {[echo 38]} {[echo 39]} {[echo 40]} {[echo 41]} {[echo 42]} {[echo 43]} {[echo 44]} {[echo 45]} {[echo 46]} {[echo 47]} {[echo 48]} {[echo 49]} {[echo 50]} {[echo 51]} {[echo 52]} {[echo 53]} {[echo 54]} {[echo 55]} {[echo 56]} {[echo 57]} {[echo 58]} {[echo 59]} {[echo 60]} {[echo 61]} {[echo 62]} {[echo 63]} {[echo 64]} {[echo 65]} {[echo 66]} {[echo 67]} {[echo 68]} {[echo 69]} {[echo 70]} {[echo 71]} {[echo 72]} {[echo 73]} {[echo 74]} {[echo 75]} {[echo 76]} {[echo 77]} {[echo 78]} {[echo 79]} {[echo 80]} {[echo 81]} {[echo 82]} {[echo 83]} {[echo 84]} {[echo 85]} {[echo 86]} {[echo 87]} {[echo 88]} {[echo 89]} {[echo 90]} {[echo 91]} {[echo 92]} {[echo 93]} {[echo 94]} {[echo 95]} {[echo 96]} {[echo 97]} {[echo 98]} {[echo 99]} {[echo 100]} {[echo 101]} {[echo 102]} {[echo 103]} {[echo 104]} {[echo 105]} {[echo 106]} {[echo 107]} {[echo 108]} {[echo 109]} {[echo 110]} {[echo 111]} {[echo 112]} {[echo 113]} {[echo 114]} {[echo 115]} {[echo 116]} {[echo 117]} {[echo 118]} {[echo 119]} {[echo 120]} {[echo 121]} {[echo 122]} {[echo 123]} {[echo 124]} {[echo 125]} {[echo 126]} {[echo 127]} {[echo 128]} {[echo 129]} {[echo 130]} {[echo 131]} {[echo 132]} {[echo 133]} {[echo 134]} {[echo 135]} {[echo 136]} {[echo 137]} {[echo 138]} {[echo 139]} {[echo 140]} {[echo 141]} {[echo 142]} {[echo 143]} {[echo 144]} {[echo 145]} {[echo 146]} {[echo 147]} {[echo 148]} {[echo 149]} {[echo 150]} {[echo 151]} {[echo 152]} {[echo 153]} {[echo 154]} {[echo 155]} {[echo 156]} {[echo 157]} {[echo 158]} {[echo 159]} {[echo 160]} {[echo 161]} {[echo 162]} {[echo 163]} {[echo 164]} {[echo 165]} {[echo 166]} {[echo 167]} {[echo 168]} {[echo 169]} {[echo 170]} {[echo 171]} {[echo 172]} {[echo 173]} {[echo 174]} {[echo 175]} {[echo 176]} {[echo 177]} {[echo 178]} {[echo 179]} {[echo 180]} {[echo 181]} {[echo 182]} {[echo 183]} {[echo 184]} {[echo 185]} {[echo 186]} {[echo 187]} {[echo 188]} {[echo 189]} {[echo 190]} {[echo 191]} {[echo 192]} {[echo 193]} {[echo 194]} {[echo 195]} {[echo 196]} {[echo 197]} {[echo 198]} {[echo 199]} {[echo 200]} {[echo 201]} {[echo 202]} {[echo 203]} {[echo 204]} {[echo 205]} {[echo 206]} {[echo 207]} {[echo 208]} {[echo 209]} {[echo 210]} {[echo 211]} {[echo 212]} {[echo 213]} {[echo 214]} {[echo 215]} {[echo 216]} {[echo 217]} {[echo 218]} {[echo 219]} {[echo 220]} {[echo 221]} {[echo 222]} {[echo 223]} {[echo 224]} {[echo 225]} {[echo 226]} {[echo 227]} {[echo 228]} {[echo 229]} {[echo 230]} {[echo 231]} {[echo 232]} {[echo 233]} {[echo 234]} {[echo 235]} {[echo 236]} {[echo 237]} {[echo 238]} {[echo 239]} {[echo 240]} {[echo 241]} {[echo 242]} {[echo 243]} {[echo 244]} {[echo 245]} {[echo 246]} {[echo 247]} {[echo 248]} {[echo 249]} {[echo 250]} {[echo 251]} {[echo 252]} {[echo 253]} {[echo 254]} {[echo 255]}}}'''.replace('\n', ' ')
    
    def std_bitshift_right(self):
        return '''service std_bitshift_right { jump (std_input2) { {std_output1 = std_input1} {std_output1 = std_input1 >> 1} {std_output1 = std_input1 >> 2} {std_output1 = std_input1 >> 3} {std_output1 = std_input1 >> 4} {std_output1 = std_input1 >> 5} {std_output1 = std_input1 >> 6} {std_output1 = std_input1 >> 7}}}'''.replace('\n', ' ')

    def std_bitshift_left(self):
        return '''service std_bitshift_left { jump (std_input2) { {std_output1 = std_input1} {std_output1 = std_input1 << 1} {std_output1 = std_input1 << 2} {std_output1 = std_input1 << 3} {std_output1 = std_input1 << 4} {std_output1 = std_input1 << 5} {std_output1 = std_input1 << 6} {std_output1 = std_input1 << 7}}}'''.replace('\n', ' ')
    
    def std_rng(self):
        return '''service std_rng {std_rng = std_rng + 1 std_rng = std_rng ^ (std_rng << 7) std_rng = std_rng ^ (std_rng >> 5) std_rng = std_rng ^ (std_rng << 3)} service std_entropy_rng { std_rng = std_rng + 1}'''.replace('\n', ' ')

    def std_multiply(self):
        return '''service std_multiply {
	std_output1 = 0
	if std_input2 > std_input1 {
		std_temp1 = std_input2
		std_temp2 = std_input1
	}
	else {
		std_temp1 = std_input1
		std_temp2 = std_input2
	}
	@std_multiply2
}

service std_multiply2 {
	if std_temp2 != 0 {
		std_temp3 = std_temp2 & 1
		if std_temp3 == 1 {
			std_output1 = std_output1 + std_temp1
		}
		std_temp1 = std_temp1 << 1
		std_temp2 = std_temp2 >> 1
		@std_multiply2
	}
}'''.replace('\n', ' ')

    def std_divide(self):
        return '''service std_divide {
	std_output1 = 0
	std_temp1 = std_input1
	std_temp2 = std_input2
	@std_divide2
}

service std_divide2 {
	if (std_temp2 != 0) {
		if (std_temp1 >= std_temp2) {
			std_temp1 = std_temp1 - std_temp2
			std_output1 = std_output1 + 1
			@std_divide2
		} else {
			std_output2 = std_temp1
		}
	} else {
		std_output1 = 0 /* clamp to zero */
	}
}'''.replace('\n', ' ')

    def std_pow(self):
        return '''service std_pow {
	if (std_input2 == 0) {
		std_output1 = 1
	}
	else {
        std_temp4 = std_input1
		std_temp5 = std_input2
		@std_pow2
	}
}

service std_pow2 {
	if (std_temp5 == 1) {
		std_output1 = std_temp4
	} else {
		@std_pow_multiply
        std_temp5 = std_temp5 - 1
        std_temp4 = std_output1
		@std_pow2
	}
}

service std_pow_multiply {
	std_output1 = 0
	if std_temp4 > std_input1 {
		std_temp2 = std_input1
	}
	else {
        std_temp2 = std_temp4
		std_temp4 = std_input1
	}
	@std_pow_multiply2
}

service std_pow_multiply2 {
	if std_temp2 != 0 {
		std_temp3 = std_temp2 & 1
		if std_temp3 == 1 {
			std_output1 = std_output1 + std_temp4
		}
		std_temp4 = std_temp4 << 1
		std_temp2 = std_temp2 >> 1
		@std_pow_multiply2
	}
}
'''.replace('\n', ' ')

    def std_sqrt(self):
        return '''service std_sqrt {
	std_output1 = 0
	std_temp2 = 1 << 6 /* The second from top bit is set */
	std_temp3 = 0
	std_temp4 = std_input1
	@std_sqrt2
}

service std_sqrt2 {
	if (std_temp4 < std_temp2) {
		std_temp2 = std_temp2 >> 2
		@std_sqrt2
	} else {
		@std_sqrt3
	}
}

service std_sqrt3 {
	if (std_temp2 != 0) {
		std_temp3 = std_output1 + std_temp2
		if (std_temp4 < std_temp3) {
			std_output1 = std_output1 >> 1
		}
		else {
			std_temp4 = std_temp4 - (std_output1 + std_temp2)
			std_output1 = (std_output1 >> 1) + std_temp2
		}
		std_temp2 = std_temp2 >> 2
		@std_sqrt3
	}
}'''.replace('\n', ' ')