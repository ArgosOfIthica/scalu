
from testing.frontend.parser.parser_test import TestParsing
from testing.frontend.parser.operator_test import TestOperators
import unittest

def test():
	loader = unittest.defaultTestLoader
	parsing = loader.loadTestsFromTestCase(TestParsing)
	operators = loader.loadTestsFromTestCase(TestOperators)
	runner = unittest.TextTestRunner()
	runner.run(parsing)
	runner.run(operators)
