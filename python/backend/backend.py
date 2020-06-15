import backend.static as static_pass
from backend.sequencer import sequence_generator

class backend_manager():

	def __init__(self):
		self.sequence_pass = sequence_generator()

	def compile(self, global_object):
		alias_universe = universe()
		alias_universe = static_pass.compile(new_universe, global_object)
		print(header)
		bundle = self.sequence_pass.generate_sequence(global_object)
		#header += bundle.header
		#sequence = bundle.sequence
		return header #+ sequence
