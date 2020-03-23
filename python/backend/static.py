from backend.definitions.vbuilder import build_variable

class static_generator():

	header = ''

	def compile(self, res_block):
		for var_name in res_block.variable_lookup:
			var = res_block.variable_lookup[var_name]
			self.header += build_variable(var.name, var.word_size, var.value)
		for const_name in res_block.constant_lookup:
			const = res_block.constant_lookup[const_name]
			self.header += build_variable(const.name, const.word_size, const.value)
		return self.header
