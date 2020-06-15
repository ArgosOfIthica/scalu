





class universe():

	def __init__():
		self.computations = list()
		self.known_aliases = list()
		self.picker = picker()

	def add_computation(alias_type):
		alias_string = self.picker.new_alias()
		new_alias = alias(alias_string, alias_type)
		new_computation = computation(new_alias, command_list)


	def generate_anonymous_alias():



class computation():

	def __init__(alias_object, command_list):
		self.alias = alias_object
		self.commands = list()

class alias():

	def __init__(string, compile_type):
		self.string = string
		self.type = compile_type

class picker():

	def __init__(self):

		self.symbols = list()
		self.current_use = 1
		for x in range(48, 58):
			self.symbols.append(chr(x))
		for x in range(97, 123):
			self.symbols.append(chr(x))

	def new_alias_list(self, count):
		alias_list = list()
		for alias in range(count):
			alias_list.append(self.new_alias())
		return alias_list


	def new_alias(self):
		revolutions = int(math.log(self.current_use, len(self.symbols))) + 1
		new_alias = list()
		for x in range(0, revolutions):
			selected = int((self.current_use / int((len(self.symbols) ** x)) % len(self.symbols)))
			new_alias = [self.symbols[selected]] + new_alias
		new_alias = ''.join(new_alias)
		new_alias = '%' + new_alias  #using π here causes strange behavior
		self.current_use += 1
		return new_alias
