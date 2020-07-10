import backend.static as static_pass
from backend.alias import *
from backend.emitter import emission

class backend_manager():

	def compile(self, global_object):
		alias_universe = universe()
		global_object.universe = alias_universe #TODO: delete universe assignment after correcting the model
		header = static_pass.compile(global_object)
		config = emission(header, alias_universe)
		print(config)
