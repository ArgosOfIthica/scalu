


def resolution(global_object):

	def resolution_error():
		raise Exception("Resolution error")

	def resolve_block(block):
		build_sequence = list()
		constant_sequence = list()
		
		def variable_declaration_is_unique(name):
			return len(set(build_sequence)) == len(build_sequence)

		for ele in block.sequence:
			if ele.identity == "variable":
				if variable_declaration_is_unique(ele.name):
					build_sequence.append(ele.name)
					if ele.is_literal:
						constant_sequence.append(ele.value)
				else:
					resolution_error()


			elif ele.identity == "assignment":
				if ele.is_literal and (ele.destination in build_sequence):
					constant_sequence.append(ele.value)
				elif (not (ele.source in build_sequence and ele.destination in build_sequence)):
					resolution_error()
				else:
					resolution_error()

	resolve_block(global_object)
	return global_object