import scalu.src.compiler as compiler
import scalu.testing.test_bootstrap as testing
import scalu.src.cli.arg_handling as arg_handler
import scalu.src.cli.input_handling as input_handler
import scalu.src.cli.output_handling as output_handler


def main():
    args = arg_handler.handle()
    if args.mode[0] == 'compile':
        file_input = input_handler.handle(args.input)
        text_output = scalu(file_input, args)
        output_handler.handle(text_output, args.output_dir, args.remove)
    elif args.mode[0] == 'test':
        testing.test()

def scalu(program, args):
    comp = compiler.compiler()
    output = comp.compile(program)
    return output
