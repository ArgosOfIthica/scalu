import unittest
import scalu.src.preprocess.macro as macro

class TestPreprocess(unittest.TestCase):

    def setUp(self):
        self.declaration = False
        if self.declaration:
            print(self._testMethodName)

    def test_no_macros(self):
        program_text = 'banana split'
        self.assertEqual(macro.compile(program_text), program_text)
    
    def test_preserves_splits(self):
        program_text = 'banana \n split'
        self.assertEqual(macro.compile(program_text), program_text)

    def test_macro_write(self):
        program_text = '#write #scalu_language##'
        self.assertEqual(macro.compile(program_text), 
        'python3')
    
    def test_macro_def(self):
        program_text = '#def var my_var is a string###write this #my_var##'
        self.assertEqual(macro.compile(program_text),
        'this is a string')
    
    def test_total_reset(self):
        program_text = '#def var my_var test_string###reset ###write #my_var##'
        self.assertEqual(macro.compile(program_text),
        '')