import src.frontend.lexer.lexer as lexer
import src.frontend.parser.parser as parser
import src.preprocess.preprocess as preprocess
import src.visualize.visualize as visualize
import src.frontend.unwrapper.unwrapper as unwrapper


def compile(program_string):
    debug = False
    #program_string = preprocess.preprocess(program_string)
    program_tokens = lexer.tokenize(program_string)
    syntax_tree = parser.parse(program_tokens)
    if debug:
        visualize.visualize(syntax_tree)
    unwrapped_ast = unwrapper.unwrap(syntax_tree)
    if debug:
        print('**********')
        visualize.visualize_unwrapping(unwrapped_ast)
    return syntax_tree
