import unittest
import scalu.src.compiler as compiler

class TestOperators(unittest.TestCase):

    def setUp(self):
        self.declaration = False
        self.compiler = compiler.compiler()
        self.blueprint_full_chain = 'sandbox test1 bind {k: test_event} map {test_event: @test_service} service test_service {} '
        self.blueprint_two_chain = 'sandbox test1 bind {k: test_event} map {test_event: @test_service} service test_service '
        self.blueprint_one_chain = 'sandbox test1 bind{k: test_event} map '
        if self.declaration:
            print(self._testMethodName)

    @unittest.expectedFailure
    def test_number_too_large(self):
        program = self.blueprint_two_chain + '{a = 512}'
        print(self.compiler.text_compile(program))

    def test_greater_than(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    if (7 > 5) {[echo true]} else {[echo false]}
                                                    if (a > 5) {[echo true]} else {[echo false]}
                                                    if (7 > b) {[echo true]} else {[echo false]}
                                                    if (a > b) {[echo true]} else {[echo false]}
                                                    }'''
        self.compiler.text_compile(program)

    def test_less_than(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    if (7 < 5) {[echo true]} else {[echo false]}
                                                    if (a < 5) {[echo true]} else {[echo false]}
                                                    if (7 < b) {[echo true]} else {[echo false]}
                                                    if (a < b) {[echo true]} else {[echo false]}
                                                    }'''
        self.compiler.text_compile(program)

    def test_greater_than_or_equal(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    if (7 >= 5) {[echo true]} else {[echo false]}
                                                    if (a >= 5) {[echo true]} else {[echo false]}
                                                    if (7 >= b) {[echo true]} else {[echo false]}
                                                    if (a >= b) {[echo true]} else {[echo false]}
                                                    }'''
        self.compiler.text_compile(program)

    def test_less_than_or_equal(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    if (7 <= 5) {[echo true]} else {[echo false]}
                                                    if (a <= 5) {[echo true]} else {[echo false]}
                                                    if (7 <= b) {[echo true]} else {[echo false]}
                                                    if (a <= b) {[echo true]} else {[echo false]}
                                                    }'''
        self.compiler.text_compile(program)

    def test_bitwise_negation(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    if (7 <= 5) {[echo true]} else {[echo false]}
                                                    if (a <= 5) {[echo true]} else {[echo false]}
                                                    if (7 <= b) {[echo true]} else {[echo false]}
                                                    if (a <= b) {[echo true]} else {[echo false]}
                                                    }'''
        self.compiler.text_compile(program)

    def test_bitwise_and(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    c = 7 & 5
                                                    c = a & 5
                                                    c = 7 & b
                                                    c = a & b
                                                    }'''
        self.compiler.text_compile(program)

    def test_bitwise_or(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    c = 7 | 5
                                                    c = a | 5
                                                    c = 7 | b
                                                    c = a | b
                                                    }'''
        self.compiler.text_compile(program)

    def test_bitwise_xor(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    c = 7 ^ 5
                                                    c = a ^ 5
                                                    c = 7 ^ b
                                                    c = a ^ b
                                                    }'''
        self.compiler.text_compile(program)

    def test_full_if(self):
        program = self.blueprint_two_chain + '{ a = 6 if (a == 5) {a = ?4 @true_branch} else {a = ?6 @false_branch}} service true_branch { [echo this is true] } service false_branch { [echo this is false]}'
        self.compiler.text_compile(program)

    def test_partial_if(self):
        program = self.blueprint_two_chain + '{ a = 5 if (a == 5) {a = ?4 @true_branch}} service true_branch { [echo this is true] }'
        self.compiler.text_compile(program)

    def test_elif(self):
        program = self.blueprint_two_chain + '{ a = 6 if (a == 5) {a = ?4 @true_branch} elif (a == 6) {a = ?6 @false_branch} else {[echo reached the else branch]}} service true_branch { [echo this is true] } service false_branch { [echo this is false]}'
        self.compiler.text_compile(program)

    def test_nested_jump(self):
        program = self.blueprint_two_chain + '{ a = 6 if (a == 5) {a = ?4 @true_branch} else \n{ if (a == 6) { @false_branch} else {[echo wrong answer 2]}}} \n service true_branch { [echo wrong answer 1] } service false_branch { [echo correct answer]}'
        self.compiler.text_compile(program)

    def test_inequality(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    if (7 != 5) {[echo true]} else {[echo false]}
                                                    if (a != 5) {[echo true]} else {[echo false]}
                                                    if (7 != b) {[echo true]} else {[echo false]}
                                                    if (a != b) {[echo true]} else {[echo false]}
                                                    }'''
        self.compiler.text_compile(program)

    def test_addition(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    c = 7 + 5
                                                    c = a + 5
                                                    c = 7 + b
                                                    c = a + b
                                                    }'''
        self.compiler.text_compile(program)

    def test_fast_addition(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    c = 7 +? 5
                                                    c = a +? 5
                                                    c = 7 +? b
                                                    c = a +? b
                                                    }'''
        self.compiler.text_compile(program)

    def test_subtraction(self):
        program = self.blueprint_two_chain + '''{a = 7 b = 5
                                                    c = 7 - 5
                                                    c = a - 5
                                                    c = 7 - b
                                                    c = a - b
                                                    }'''
        self.compiler.text_compile(program)

    def test_basic_binary_print(self):
        program = self.blueprint_two_chain + '{ a = 3 [echo is this 3?]}'
        self.compiler.text_compile(program)

    def test_binary_print(self):
        program = self.blueprint_two_chain + '{ a = 3 [echo is this 5?] a = ?5 [echo is this 7?] a = ?7 a = 9 [echo is this 9?] a = ?a }'
        self.compiler.text_compile(program)

    def test_sandbox_access(self):
        program = 'sandbox one service s_one {var_one = two.var + 7} sandbox two service s_two {var = 7}'
        self.compiler.text_compile(program)

    @unittest.expectedFailure
    def test_fake_sandbox_access(self):
        program = 'sandbox one service s_one {var_one = three.var + 7} sandbox two service s_two {var = 7}'
        self.compiler.text_compile(program)

    def test_bitshift_left(self):
        program = self.blueprint_two_chain + '{ a = 4 << 3 }'
        self.compiler.text_compile(program)

    def test_bitshift_right(self):
        program = self.blueprint_two_chain + '{ a = 4 >> 3 }'
        self.compiler.text_compile(program)

    @unittest.expectedFailure
    def test_bitshift_left_overflow(self):
        program = self.blueprint_two_chain + '{ a = 4 << 10 }'
        self.compiler.text_compile(program)
