from frontend.lexer import lexer
from frontend.parser.parser import parser
from visualize import visualizer
from frontend.resolution import resolver
from frontend.unwrapper import unwrapper



class frontend_manager():
	debug = True

	def __init__(self):
		self.lexer = lexer()
		self.parser = parser()
		self.resolver = resolver()
		self.visualizer = visualizer()
		self.unwrapper = unwrapper()

	def compile(self, program_string):
		program_tokens = self.lexer.tokenize(program_string)
		syntax_tree = self.parser.parse(program_tokens)
		enriched_syntax_tree = self.resolver.resolve(syntax_tree)
		if self.debug:
			self.visualizer.visualize(enriched_syntax_tree)
		unwrapped_ast = self.unwrapper.unwrap(enriched_syntax_tree)
		if self.debug:
			self.visualizer.visualize_unwrapping(unwrapped_ast)
		return enriched_syntax_tree
