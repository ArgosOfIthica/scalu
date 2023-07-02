
import scalu.src.frontend.utility.utility as utility
import scalu.src.model.universe as universe
import math as math
import scalu.src.cli.arg_handling as arg_handler

def get_max_word_size():
    return arg_handler.handle().forcewordsize

class rd_obj():

    def __init__(self):
        self.name = ''
        self.declared = False

    def declaration_collision(self):
        pass

    def validate_specific(self):
        pass

class rd_list(list):

    def setup(self, obj_constructor):
        self.obj_constructor = obj_constructor
        return self

    def reference(self, obj_string, constructor_override=None):
        if obj_string in [x.name for x in self]:
            return self.get_object(obj_string)
        else:
            if constructor_override is not None:
                new_obj = constructor_override()
            else:
                new_obj = self.obj_constructor()
            new_obj.name = obj_string
            new_obj.declared = False
            self.append(new_obj)
            return new_obj

    def declare(self, obj_string, constructor_override=None):
        if obj_string in [x.name for x in self]:
            declared_obj = self.get_object(obj_string)
            if declared_obj.declared:
                declared_obj.declaration_collision()
                raise Exception('object collision')
            else:
                declared_obj.declared = True
                return declared_obj
        else:
            if constructor_override is not None:
                new_obj = constructor_override()
            else:
                new_obj = self.obj_constructor()
            new_obj.name = obj_string
            new_obj.declared = True
            self.append(new_obj)
            return new_obj

    def get_object(self, obj_string):
        for obj in self:
            if obj_string == obj.name:
                return obj
        raise Exception('object not accessible')

    def validate(self):
        for obj in self:
            if not obj.declared:
                raise Exception(obj.name + ' has not been declared')
            obj.validate_specific()

class global_object():

    def __init__(self):
        self.sandbox = rd_list().setup(sandbox)
        self.maps = map_collection()
        self.universe = universe.universe()
        self.universe.initialize()

    def resolve(self):
        self.sandbox.validate()
        for sandbox in self.sandbox:
            sandbox.variables.validate()
            sandbox.services.validate()


class map_collection():

    def __init__(self):
        self.maps = list()

    def add(self, event):
        if self.non_colliding_keys(event) and self.non_colliding_files(event):
            if event.string in [x.string for x in self.maps]:
                old_event = self.return_matching_event(event)
                self.merge_events(old_event, event)
            else:
                self.maps.append(event)
        else:
            raise Exception('Cannot add event "' + event.string + '" to collection, key "' + event.key + '" already in collection. The same key cannot be bound to multiple events.')

    def return_matching_event(self, event):
        for maps in self.maps:
            if event.string == maps.string:
                return maps

    def non_colliding_keys(self, event):
        if event.key is None or event.key not in [x.key for x in self.maps]:
            return True
        else:
            raise Exception('Cannot add event "' + event.string + '" to collection, key "' + event.key + '" already in collection. The same key cannot be bound to multiple events.')

    def non_colliding_files(self, event):
        if event.file is None or event.file not in [x.file for x in self.maps]:
            return True
        else:
            raise Exception('Cannot add event "' + event.string + '" to collection, file "' + event.file + '" already in collection. The same file cannot be bound to multiple events.')

    def merge_events(self, old_event, new_event):
        if new_event.key is not None:
            old_event.key = new_event.key
        if new_event.file is not None:
            old_event.file = new_event.file
        old_event.services = old_event.services + new_event.services

class sandbox(rd_obj):

    def __init__(self):
        rd_obj.__init__(self)
        self.variables = rd_list().setup(variable)
        self.services = rd_list().setup(service)
        self.min_word_size = '2'
        self.max_word_size = get_max_word_size()
    
    def validate_specific(self):
        for variable in self.variables:
            self.min_word_size = str(max(int(self.min_word_size), int(variable.min_word_size)))
        for variable in self.variables:
            variable.word_size = self.min_word_size

class variable(rd_obj):

    def __init__(self, name=''):
        rd_obj.__init__(self)
        self.name = name
        self.type = 'int'
        self.value = '0'
        self.word_size = get_max_word_size()
        self.min_word_size = '2'

    def set_value(self, value):
        if int(value) < 2**int(self.word_size) and int(value) >= 0:
            self.value = value
            self.min_word_size = utility.calc_min_word_size(self.min_word_size, value)
        else:
            raise Exception('illegal value declaration:' + value + ' . Number not within bounds of the word size')

class constant(variable):

    def __init__(self, value='0'):
        variable.__init__(self, value)
        self.set_value(value)

class service(rd_obj):

    def __init__(self):
        rd_obj.__init__(self)
        self.sequence = list()
        self.is_anonymous = False

class event():

    def __init__(self, string):
        self.string = string
        self.key = None
        self.file = None
        self.services = list()

    def add_key(self, key_string):
        if self.key == None:
            self.key = key_string
        else:
            raise Exception('event "' + self.string + '" already has key "' + self.key + '". Cannot assign "' + key_string + '" to "' + self.string + '"')

    def add_file(self, file_string):
        if self.file == None:
            self.file = file_string
        else:
            raise Exception('event "' + self.string + '" already has file "' + self.file + '". Cannot assign "' + file_string + '" to "' + self.string + '"')


class statement():

    def __init__(self):
        self.identifier = ''
        self.arg = list()

class assignment(statement):

    def __init__(self):
        self.arg = [None]

class service_call(statement):


    def __init__(self):
        self.identifier = ''

class source_call(statement):

    def __init__(self):
        self.arg = [None]

class if_statement():

    def __init__(self):
        self.true_service = None
        self.false_service = None
        self.condition = None

class jump_statement():

    def __init__(self):
        self.var = None
        self.services = list()

    def update_word(self):
        service_count = len(self.services)
        self.var.min_word_size = utility.calc_min_word_size(self.var.min_word_size, service_count - 1)

class operator():

    def __init__(self):
        identity = ''
        output = ''
        arg = list()

class unary_operator(operator):

    def __init__(self):
        operator.__init__(self)
        self.arg = [None]

class binary_operator(operator):

    def __init__(self):
        operator.__init__(self)
        self.arg =  [None] * 2

class conditional(operator):

    def __init__(self):
        operator.__init__(self)
        self.arg = [None] * 2

def is_assignment(arg):
    return isinstance(arg, assignment)

def is_service_call(arg):
    return isinstance(arg, service_call)

def is_operator(arg):
    return isinstance(arg, operator)

def is_unary_operator(arg):
    return isinstance(arg, unary_operator)

def is_binary_operator(arg):
    return isinstance(arg, binary_operator)

def is_variable(arg):
    return isinstance(arg, variable)

def is_constant(arg):
    return isinstance(arg, constant)

def is_literal_value(arg):
    return isinstance(arg, literal_value)

def is_source_call(arg):
    return isinstance(arg, source_call)

def is_key(arg):
    return isinstance(arg, key)

def is_if_statement(arg):
    return isinstance(arg, if_statement)

def is_jump_statement(arg):
    return isinstance(arg, jump_statement)

def is_conditional(arg):
    return isinstance(arg, conditional)
