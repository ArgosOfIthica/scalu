from frontend.lexer import lexer
from frontend.parser.expect import parse
from frontend.resolution import resolve



class frontend_manager():

	def __init__(self):
		self.lexer = lexer()
		self.parser = parser()
	#	self.resolver = resolver()

	def compile(self, program_string):
		program_tokens = self.lexer.tokenize(program_string)
		syntax_tree = self.parser.parse(program_tokens)
		#enriched_syntax_tree = self.resolver.resolve(syntax_tree)
		#return enriched_syntax_tree
