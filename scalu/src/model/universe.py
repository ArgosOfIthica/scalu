import math
import scalu.src.cli.arg_handling as arg_handler


class universe():

    def __init__(self):
        self.args = arg_handler.args
        self.computations = list()
        self.vars = list()
        self.known_aliases = list()
        self.alias_to_def = dict()
        self.picker = picker()
        self.constructs = dict()
        self.constant_constructs = list()
        self.initialized = False

    def initialize(self):
        self.initialized = True
        self.true = self.new_var()
        self.false = self.new_var()
        self.root = self.new_def('root')

    def add_alias(self, alias_type):
        alias_string = self.picker.new_alias()
        new_alias = alias(alias_string, alias_type)
        self.known_aliases.append(new_alias)
        return new_alias

    def new_def(self, alias_type):
        if not self.initialized:
            self.initialize()
        alias_string = self.picker.new_alias()
        new_alias = alias(alias_string, alias_type)
        new_computation = definition(new_alias)
        self.alias_to_def[new_alias] = new_computation
        self.known_aliases.append(new_alias)
        self.computations.append(new_computation)
        return new_computation

    def new_var(self):
        alias_string = self.picker.new_alias()
        new_alias = alias(alias_string, 'stateful')
        self.known_aliases.append(new_alias)
        self.vars.append(new_alias)
        return new_alias

    def host_def(self, host , extension_type):
        new_computation = self.new_def(extension_type)
        host.extend(new_computation.alias)
        return new_computation

    def set_var(self, host_compute, var, target):
        if is_definition(target):
            target = target.alias
        host_compute.extend(self.set_variable_internal(var, target).alias)

    def set_variable_internal(self, var, target):
        if target not in self.vars:
            target_wrapper = self.new_def('set_target')
            target_wrapper.extend(target)
            target_wrapper = target_wrapper.alias
        else:
            target_wrapper = target
        new_transform = state_transform(var)
        if var.type == 'stateful':
            new_transform.alias = var
        else:
            raise Exception('invalid alias for var')
        new_transform.extend(target_wrapper)
        var_wrapper = self.new_def('set_var')
        var_wrapper.extend(new_transform)
        return var_wrapper

class computation():

    def __init__(self, alias_object):
        self.alias = alias_object
        self.commands = list()

    def extend(self, command):
        self.commands.append(command)

class definition(computation):

    def extend(self, command):
        if isinstance(command, definition):
            raise Exception('definitions cannot extend definitions')
        else:
            self.commands.append(command)

class state_transform(computation):
    pass


class alias():

    def __init__(self, string, compile_type):
        self.string = string
        self.type = compile_type
        self.identity = self.string + self.type

class bind():

    def __init__(self, key, compute):
        self.key = key
        self.compute = compute

class source_command():

    def __init__(self, string):
        self.string = string


def get_bin(value, word_size):
    return format(int(value), 'b').zfill(int(word_size))

class variable():

    def __init__(self, global_object, var):
        uni = global_object.universe
        self.value = var.value
        self.word_size = var.word_size
        self.bool_string = get_bin(var.value, var.word_size)
        self.bits = list()
        self.set_true = list()
        self.set_false = list()
        for bit in range(int(var.word_size)):
            self.bits.append( uni.new_var())
            self.set_true.append(uni.new_def('set_true'))
            uni.set_var(self.set_true[bit], self.bits[bit], uni.true)
            self.set_false.append(uni.new_def('set_false'))
            uni.set_var(self.set_false[bit], self.bits[bit], uni.false)
            if self.bool_string[bit] == '0':
                uni.root.extend(self.set_false[bit].alias)
            elif self.bool_string[bit] == '1':
                uni.root.extend(self.set_true[bit].alias)
            else:
                raise Exception('is not valid boolean string')
        if arg_handler.args.debug:
            print('creating var ' + var.name)

class picker():

    def __init__(self):
        self.args = arg_handler.args
        self.symbols = list()
        self.current_use = 1
        lower_case_letters = range(97,123)
        numbers = range(48,58)
        for x in numbers:
            self.symbols.append(chr(x))
        for x in lower_case_letters:
            self.symbols.append(chr(x))

    def new_alias_list(self, count):
        return tuple(self.new_alias() for alias in range(count))

    def new_alias(self):
        RESERVED_PREFIX = self.args.aliasprefix
        revolutions = int(math.log(self.current_use, len(self.symbols))) + 1
        new_alias = list()
        for x in range(0, revolutions):
            selected = int((self.current_use / int((len(self.symbols) ** x)) % len(self.symbols)))
            new_alias = [self.symbols[selected]] + new_alias
        new_alias = ''.join(new_alias)
        new_alias = RESERVED_PREFIX + new_alias
        self.current_use += 1
        return new_alias

    def reset(self):
        self.current_use = 1
        return self

def is_computation(arg):
    return isinstance(arg, computation)

def is_definition(arg):
    return isinstance(arg, definition)

def is_alias(arg):
    return isinstance(arg, alias)

def is_source_command(arg):
    return isinstance(arg, source_command)

def is_bind(arg):
    return isinstance(arg, bind)

def is_var(arg):
    return isinstance(arg, state_transform)
