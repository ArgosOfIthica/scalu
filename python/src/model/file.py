import math

class file_container():

	def __init__(self, global_object, main_text):
		self.buffers()
		self.files = list()
		self.host_files = self.create_host_files('scalu', main_text)
		for event in global_object.maps.maps:
			if event.file is not None:
				new_file = cfg_file(event.file, '$' + event.string)
				self.files.append(new_file)

	def buffers(self):
		#Maximum size of a .cfg file is 1 Mebibyte = 1024 kibibytes = 1048576 bytes
		#Execution buffer is 40 bytes, enough room to execute a long file name
		self.RAW_ALLOCATION = 1048576
		self.EXECUTION_BUFFER = 40
		self.ACTUAL_ALLOCATION = self.RAW_ALLOCATION - self.EXECUTION_BUFFER

	def create_host_files(self, name, raw_string):
		self.recursively_create_content(raw_string)
		for i in range(len(self.files)):
			if i != 0:
				self.files[i].name = name + str(i)
			else:
				self.files[i].name = name
			if i != len(self.files) - 1:
				self.files[i].content += '\nexec ' + name + str(i + 1)


	def recursively_create_content(self, raw_string):
		if len(raw_string) > self.ACTUAL_ALLOCATION:
			lines = raw_string.split('\n')
			file_1 = lines[:int(len(lines)/2)]
			file_1_string = '\n'.join(file_1)
			self.recursively_create_content(file_1_string)
			file_2 = lines[int(len(lines)/2):]
			file_2_string = '\n'.join(file_2)
			self.recursively_create_content(file_2_string)
		else:
			file_obj = cfg_file('placeholder', raw_string)
			self.files.append(file_obj)


class cfg_file():

	def __init__(self, name, content):
		self.name = name
		self.content = content
		self.type = 'cfg'

