import src.compiler as compiler
import testing.test_bootstrap as testing
import sys
import src.cli.arg_handling as arg_handler
import src.cli.input_handling as input_handler
import src.cli.output_handling as output_handler


def main():
    properties = arg_handler.handle(sys.argv)
    if properties.mode == 'compile':
        file_input = input_handler.handle()
        text_output = scalu(file_input, properties)
        process_files = output_handler.handle(text_output)
    elif properties.mode == 'test':
        testing.test()
    elif properties.mode == 'help':
        pass


def scalu(program, properties):
    if properties.mode == 'compile':
        comp = compiler.compiler()
        output = comp.compile(program)
        return output

if __name__ == "__main__":
    main()
