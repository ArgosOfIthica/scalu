
from scalu.testing.frontend.parser.parser_test import TestParsing
from scalu.testing.frontend.parser.operator_test import TestOperators
from scalu.testing.preprocess.preprocess_test import TestPreprocess
import scalu.src.compiler as compiler
from scalu.native.interpreter import native_console
import unittest
import scalu.src.cli.arg_handling as arg_handler

def test():
    test_interpreter()
    loader = unittest.defaultTestLoader
    parsing = loader.loadTestsFromTestCase(TestParsing)
    operators = loader.loadTestsFromTestCase(TestOperators)
    preprocessing = loader.loadTestsFromTestCase(TestPreprocess)
    runner = unittest.TextTestRunner()
    runner.run(parsing)
    runner.run(operators)
    #runner.run(preprocessing)

def test_interpreter(verbose=True):
    args = arg_handler.handle()
    con = native_console()
    program = ''
    with open('scalu/native/test.scalu', 'r') as file:
        program = file.read()
    program = compiler.compiler().text_compile(program)
    result = con.parse_input(program).parse_input(args.eventprefix + 'test_event').pop_output_buffer()
    result += con.stats()
    print(result)
