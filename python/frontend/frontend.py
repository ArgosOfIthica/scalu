import frontend.lexer.lexer as lexer
import frontend.parser.parser as parser
#from visualize import visualizer
#from frontend.resolution.resolution import resolution
#from frontend.unwrapper.unwrapper import unwrapper



class frontend_manager():


	def __init__(self):
		self.debug = False
		#self.resolver = resolution()
		#self.visualizer = visualizer()
		#self.unwrapper = unwrapper()

	def compile(self, program_string):
		program_tokens = lexer.tokenize(program_string)
		syntax_tree = parser.parse(program_tokens)
		'''enriched_syntax_tree = self.resolver.resolve(syntax_tree)
		if self.debug:
			self.visualizer.visualize(enriched_syntax_tree)
		unwrapped_ast = self.unwrapper.unwrap(enriched_syntax_tree)
		if self.debug:
			self.visualizer.visualize_unwrapping(unwrapped_ast)
		return enriched_syntax_tree'''
