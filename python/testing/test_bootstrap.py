
from testing.frontend.parser.parser_test import TestParsing
import unittest

def test():
	loader = unittest.defaultTestLoader
	parsing = loader.loadTestsFromTestCase(TestParsing)
	runner = unittest.TextTestRunner()
	runner.run(parsing)
