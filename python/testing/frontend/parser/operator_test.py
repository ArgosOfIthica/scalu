import unittest
import src.compiler as compiler

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
		program = self.blueprint_two_chain + '{a = 7 if (a > 5) {[echo true]} else {[echo false]}}'
		self.compiler.text_compile(program)

	def test_less_than(self):
		program = self.blueprint_two_chain + '{a = 7 if (a < 5) {[echo true]} else {[echo false]}}'
		self.compiler.text_compile(program)

	def test_greater_than_or_equal(self):
		program = self.blueprint_two_chain + '{a = 7 if (a >= 5) {[echo true]} else {[echo false]}}'
		self.compiler.text_compile(program)

	def test_less_than_or_equal(self):
		program = self.blueprint_two_chain + '{a = 7 if (a <= 5) {[echo true]} else {[echo false]}}'
		self.compiler.text_compile(program)

	def test_bitwise_negation(self):
		program = self.blueprint_two_chain + '{ [echo input is] old_number = ?73  [echo output is] new_number = ?(!old_number) }'
		self.compiler.text_compile(program)

	def test_bitwise_and(self):
		program = self.blueprint_two_chain + '{ [echo input1 is] input1 = ?15 [echo input2 is] input2 = ?62 [echo output is] output = ?(input1 & input2) }'
		self.compiler.text_compile(program)

	def test_bitwise_or(self):
		program = self.blueprint_two_chain + '{ [echo input1 is] input1 = ?15 [echo input2 is] input2 = ?62 [echo output is] output = ?(input1 | input2) }'
		self.compiler.text_compile(program)

	def test_full_jump(self):
		program = self.blueprint_two_chain + '{ a = 6 if (a == 5) {a = ?4 @true_branch} else {a = ?6 @false_branch}} service true_branch { [echo this is true] } service false_branch { [echo this is false]}'
		self.compiler.text_compile(program)

	def test_partial_jump(self):
		program = self.blueprint_two_chain + '{ a = 5 if (a == 5) {a = ?4 @true_branch}} service true_branch { [echo this is true] }'
		self.compiler.text_compile(program)

	def test_nested_jump(self):
		program = self.blueprint_two_chain + '{ a = 6 if (a == 5) {a = ?4 @true_branch} else \n{ if (a == 6) { @false_branch} else {[echo wrong answer 2]}}} \n service true_branch { [echo wrong answer 1] } service false_branch { [echo correct answer]}'
		self.compiler.text_compile(program)

	def test_inequality(self):
		program = self.blueprint_two_chain + '{ a = 4 if (a != 2) { [echo correct]} else {[echo wrong]}}'
		self.compiler.text_compile(program)

	def test_addition(self):
		program = self.blueprint_two_chain + '{a = 12 + 10}'
		self.compiler.text_compile(program)

	def test_subtraction(self):
		program = self.blueprint_two_chain + '{a = 32 - 7}'
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