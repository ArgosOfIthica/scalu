from backend.static import static_generator
from visualize import visualizer

class backend_manager():
	header = ''
	body = ''

	def __init__(self):
		self.static_pass = static_generator()

	def compile(self, ast):
		self.header = self.static_pass.compile(ast.resolution)
		return self.header
