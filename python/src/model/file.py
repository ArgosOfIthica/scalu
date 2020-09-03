class file_container():

	def __init__(self, global_object, main_text):
		self.files = list()
		self.host_file = cfg_file('scalu', main_text)
		self.files.append(self.host_file)
		for event in global_object.maps.maps:
			if event.file is not None:
				new_file = cfg_file(event.file, '$' + event.string)
				self.files.append(new_file)

class cfg_file():

	def __init__(self, name, content):
		self.name = name
		self.content = content
		self.type = 'cfg'
