import scalu.src.frontend.lexer.lexer as lexer
import scalu.src.frontend.parser.expect as parser
import scalu.src.visualize.visualize as visualize
import scalu.src.frontend.unwrapper.unwrapper as unwrapper
import scalu.src.cli.arg_handling as arg_handler


def compile(program_string: str):
    args = arg_handler.handle()
    #program_string = preprocess.preprocess(program_string)
    program_tokens = lexer.Tokenizer().tokenize(program_string)
    syntax_tree = parser.parse(program_tokens)
    if args.debug:
        visualize.visualize(syntax_tree)
    unwrapped_ast = unwrapper.unwrap(syntax_tree)
    if args.debug:
        print('**********')
        visualize.visualize_unwrapping(unwrapped_ast)
    return syntax_tree
