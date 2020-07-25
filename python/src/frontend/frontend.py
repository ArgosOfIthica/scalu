import src.frontend.lexer.lexer as lexer
import src.frontend.parser.parser as parser
import src.visualize.visualize as visualize
import src.frontend.resolution.resolution as resolution
import src.frontend.unwrapper.unwrapper as unwrapper


def compile(program_string):
	debug = False
	program_tokens = lexer.tokenize(program_string)
	syntax_tree = parser.parse(program_tokens)
	enriched_syntax_tree = resolution.resolve(syntax_tree)
	if debug:
		visualize.visualize(enriched_syntax_tree)
	unwrapped_ast = unwrapper.unwrap(enriched_syntax_tree)
	if debug:
		visualize.visualize_unwrapping(unwrapped_ast)
	return enriched_syntax_tree
