from backend.static import static_generator
from backend.header import unwrapper
from visualize import visualizer

class backend_manager():
	header = ''
	body = ''

	def __init__(self):
		self.static_pass = static_generator()
		self.unwrapping_pass = unwrapper()
		self.visualizer = visualizer()

	def compile(self, ast):
		self.body = self.unwrapping_pass.compile(ast)
		self.visualizer.visualize_unwrapping(self.body)
		self.header = self.static_pass.compile(ast.resolution)
		return self.header
