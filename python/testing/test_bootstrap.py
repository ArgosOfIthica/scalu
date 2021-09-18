
from testing.frontend.parser.parser_test import TestParsing
from testing.frontend.parser.operator_test import TestOperators
from testing.preprocess.preprocess_test import TestPreprocess
import src.compiler as compiler
from native.interpreter import native_console
import unittest

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
	con = native_console()
	program = ''
	with open('native/test.scalu', 'r') as file:
		program = file.read()
	program = compiler.compiler().text_compile(program)
	result = con.parse_input(program).parse_input('$test_event').pop_output_buffer()
	print(result)