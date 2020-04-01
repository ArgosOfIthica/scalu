from backend.definitions.vbuilder import build_variable

class static_generator():

	header = ''

	def compile(self, res):
		for var_name in res.variable_lookup:
			var = res.variable_lookup[var_name]
			self.header += build_variable(var.name, var.word_size, var.value)
		for const_name in res.constant_lookup:
			const = res.constant_lookup[const_name]
			self.header += build_variable(const.name, const.word_size, const.value)
		return self.header
