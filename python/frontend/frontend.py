import frontend.lexer.lexer as lexer
import frontend.parser.parser as parser
import visualize as visualize
import frontend.resolution.resolution as resolution
#from frontend.unwrapper.unwrapper import unwrapper



class frontend_manager():


	def __init__(self):
		self.debug = True
		#self.unwrapper = unwrapper()

	def compile(self, program_string):
		program_tokens = lexer.tokenize(program_string)
		syntax_tree = parser.parse(program_tokens)
		enriched_syntax_tree = resolution.resolve(syntax_tree)
		if self.debug:
			visualize.visualize(enriched_syntax_tree)
		'''unwrapped_ast = self.unwrapper.unwrap(enriched_syntax_tree)
		if self.debug:
			self.visualizer.visualize_unwrapping(unwrapped_ast)
		return enriched_syntax_tree'''
