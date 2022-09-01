import scalu.src.compiler as compiler
import scalu.testing.test_bootstrap as testing
import scalu.src.cli.arg_handling as arg_handler
import scalu.src.cli.input_handling as input_handler
import scalu.src.cli.output_handling as output_handler


def main():
    properties = arg_handler.handle()
    if properties.mode == 'compile':
        file_input = input_handler.handle(properties.input)
        text_output = scalu(file_input, properties)
        process_files = output_handler.handle(text_output, properties.output_dir)
    elif properties.mode == 'test':
        testing.test()
    elif properties.mode == 'help':
        pass


def scalu(program, properties):
    if properties.mode == 'compile':
        comp = compiler.compiler()
        output = comp.compile(program)
        return output
