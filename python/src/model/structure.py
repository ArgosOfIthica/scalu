
import src.frontend.utility.utility as utility
import src.backend.model.universe as universe

class global_object():

	def __init__(self):
		self.sandbox = list()
		self.maps = map_collection()
		self.universe = universe.universe()
		self.universe.initialize()

	def resolve(self):
		for sandbox in self.sandbox:
			sandbox.resolve()
		self.maps.resolve()

class resolution_block():
	variable_lookup = dict()
	constant_lookup = dict()


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

	def resolve(self):
		for event in self.maps:
			for service_call in event.services:
				if is_service_call(service_call):
					service_call.resolve()


class sandbox():

	def __init__(self):
		self.name = ''
		self.resolution = resolution_block()
		self.services = list()


	def resolve(self):
		for service in self.services:
			for statement in service.sequence:
				if is_service_call(statement):
					statement.resolve()

class variable():

	def __init__(self, name=''):
		self.name = name
		self.type = 'int'
		self.value = '0'
		self.word_size = '8'

class constant(variable):

	def __init__(self, value='0'):
		self.name = value
		self.type = 'int'
		self.word_size = '8'
		if int(value) < 2**int(self.word_size) and int(value) >= 0:
			self.value = value
		else:
			raise Exception('illegal value declaration:' + value + ' . Number not within bounds of the word size')

class service():

	def __init__(self):
		self.name = ''
		self.sequence = list()

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


	def __init__(self, sandbox):
		self.sandbox = sandbox

	def resolve(self):
		matching_service = self.get_service()
		self.identifier = matching_service

	def get_service(self):
		for service in self.sandbox.services:
			if self.identifier == service.name:
				return service
		raise Exception('service call cannot be resolved')

class source_call(statement):

	def __init__(self):
		self.arg = [None]



class if_statement():

	def __init__(self):
		self.true_service = None
		self.false_service = None
		self.condition = None

class operator():
	identity = ''
	output = ''
	arg = list()

class unary_operator(operator):

	def __init__(self):
		self.arg = [None]

class binary_operator(operator):

	def __init__(self):
		self.arg =  [None] * 2

class conditional(operator):

	def __init__(self):
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

def is_conditional(arg):
	return isinstance(arg, conditional)
