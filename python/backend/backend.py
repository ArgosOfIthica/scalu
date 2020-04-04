from backend.static import static_generator
from backend.sequencer import sequence_generator
from visualize import visualizer

class backend_manager():
	header = ''
	body = ''

	def __init__(self):
		self.static_pass = static_generator()
		self.sequence_pass = sequence_generator()

	def compile(self, ast):
		self.header = self.static_pass.compile(ast.resolution)
		self.body = self.sequence_pass.generate_sequence(ast.sequence, set())
		return self.header + self.body
