
from testing.frontend.parser.parser_test import TestParsing
from testing.frontend.parser.operator_test import TestOperators
from testing.preprocess.preprocess_test import TestPreprocess
import unittest

def test():
	loader = unittest.defaultTestLoader
	parsing = loader.loadTestsFromTestCase(TestParsing)
	operators = loader.loadTestsFromTestCase(TestOperators)
	preprocessing = loader.loadTestsFromTestCase(TestPreprocess)
	runner = unittest.TextTestRunner()
	runner.run(parsing)
	runner.run(operators)
	#runner.run(preprocessing)
