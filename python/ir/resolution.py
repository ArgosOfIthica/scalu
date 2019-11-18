
import copy

def resolve(global_object):
	
	class resolution_block():
		variable_lookup = dict()
		constant_lookup = set()

	def resolution_error():
		raise Exception("Resolution error")

	def analyze_block(block):
		res = resolution_block()
		def validate_block():
			for ele in block.sequence:
				if ele.identity == "variable":
					if ele.name not in res.variable_lookup:
						res.variable_lookup[ele.name] = ele
					else:
						resolution_error()
				elif ele.identity == "assignment":
					if ele.is_literal and (ele.destination in res.variable_lookup):
						res.constant_lookup.add((res.variable_lookup[ele.destination].type, ele.source))
					elif (not (ele.source in res.variable_lookup and ele.destination in res.variable_lookup)):
						resolution_error()
					else:
						resolution_error()
				else:
					resolution_error()
		
		def resolve_block():
			for ele in block.sequence:
				if ele.identity == "assignment":
					if ele.is_literal:
						ele.destination = res.variable_lookup[ele.destination]
						literal = copy.deepcopy(ele.destination)
						literal.name = ele.source
						literal.value = ele.source
						ele.source = literal
					else:
						ele.destination = res.variable_lookup[ele.destination]
						ele.source = res.variable_lookup[ele.source]
		validate_block()
		resolve_block()
	analyze_block(global_object)
	return global_object