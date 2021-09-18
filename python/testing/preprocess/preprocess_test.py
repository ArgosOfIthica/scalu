import unittest
import src.preprocess.preprocess as preprocess

class TestPreprocess(unittest.TestCase):

    def setUp(self):
        self.declaration = False
        if self.declaration:
            print(self._testMethodName)

    def test_no_macros(self):
        program_text = 'banana split'
        self.assertEqual(preprocess.preprocess(program_text), program_text)
    
    def test_preserves_splits(self):
        program_text = 'banana \n split'
        self.assertEqual(preprocess.preprocess(program_text), program_text)

    def test_macro_declare(self):
        program_text = '#deep #my_macro banana banana #save hello'
        self.assertEqual(preprocess.preprocess(program_text), 
        'hello')
