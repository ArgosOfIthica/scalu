from backend.static import static_generator
from backend.sequencer import sequence_generator
from visualize import visualizer

class backend_manager():

	def __init__(self):
		self.static_pass = static_generator()
		self.sequence_pass = sequence_generator()

	def compile(self, ast):
		header = self.static_pass.compile(ast.resolution)
		bundle = self.sequence_pass.generate_sequence(ast.sequence, set())
		header += bundle.header
		sequence = bundle.sequence
		return header + sequence
