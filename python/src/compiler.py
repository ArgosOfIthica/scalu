
import src.frontend.frontend as frontend_manager
import src.backend.backend as backend_manager

class compiler():

	def compile(self, program):
		enriched_syntax_tree = frontend_manager.compile(program)
		compiled_program = backend_manager.compile(enriched_syntax_tree)
		print(compiled_program)
		return compiled_program
