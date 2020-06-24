import backend.static as static_pass
from backend.alias import *

class backend_manager():

	def compile(self, global_object):
		alias_universe = universe()
		global_object.universe = alias_universe #TODO: delete universe assignment after correcting the model
		alias_universe = static_pass.compile(global_object)
		print(alias_universe)
		#header += bundle.header
		#sequence = bundle.sequence
