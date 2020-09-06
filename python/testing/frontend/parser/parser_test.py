import unittest
import src.compiler as compiler

class TestParsing(unittest.TestCase):

	def setUp(self):
		self.declaration = False
		self.compiler = compiler.compiler()
		self.blueprint_full_chain = 'sandbox test1 bind {k: test_event} map {test_event: @test_service} service test_service {} '
		self.blueprint_two_chain = 'sandbox test1 bind {k: test_event} map {test_event: @test_service} service test_service '
		self.blueprint_one_chain = 'sandbox test1 bind{k: test_event} map '
		if self.declaration:
			print(self._testMethodName)

	def test_empty_program(self):
		program = 'sandbox test'
		self.compiler.text_compile(program)

	def test_service(self):
		program = 'sandbox test service test_service{} '
		self.compiler.text_compile(program)

	def test_multiple_services(self):
		program = 'sandbox test service test_service1{} service test_service2{} service test_service3{}'
		self.compiler.text_compile(program)

	def test_full_control(self):
		program = 'sandbox test service test_service1{} map {test_event: @test_service1} bind {null: test_event}'
		self.compiler.text_compile(program)

	def test_commutative_order(self):
		program = 'sandbox test map {test_event: @test_service1} service test_service1{}  bind {null: test_event}'
		self.compiler.text_compile(program)
		program = 'sandbox test bind {null: test_event} map {test_event: @test_service1} service test_service1{}  '
		self.compiler.text_compile(program)

	@unittest.expectedFailure
	def test_fail_on_missing_event(program):
		program = 'sandbox test bind {null: missing_event} map {some_other_event: @test_service1} service test_service1{}'
		self.compiler.text_compile(program)

	def test_nonmutual_binding_success(self):
		program = 'sandbox test bind { a : test_event1 b : test_event2 } map {test_event1: @test_service1 test_event2: @test_service2} service test_service1{} service test_service2{}'
		self.compiler.text_compile(program)

	@unittest.expectedFailure
	def test_mutual_binding_failure(self):
		program = 'sandbox test bind { a : test_event1 a : test_event2 } map {test_event1: @test_service1 test_event2: @test_service2} service test_service1{} service test_service2{}'
		self.compiler.text_compile(program)

	@unittest.expectedFailure
	def test_mutual_sandbox_failure(self):
		program = 'sandbox test service test_service1{} map {test_event: @test_service1} bind {null: test_event} sandbox test2 map {test_event: @test_service1} bind {null2: test_event2}'
		self.compiler.text_compile(program)

	def test_nonmutual_sandbox_success(self):
		program = 'sandbox test service test_service1{} map {test_event: @test_service1} bind {null: test_event} sandbox test2 map {test_event2: @test_service1} bind {null2: test_event2} service test_service1 {}'
		self.compiler.text_compile(program)

	@unittest.expectedFailure
	def test_sandbox_rejects_shared_binding(self):
		program = self.blueprint_full_chain + 'sandbox test2 bind {k: other_event} map {other_event: @test_service2} service test_service2 {}'
		self.compiler.text_compile(program)

	def test_sandbox_accepts_shared_events(self):
		program = self.blueprint_full_chain + 'sandbox test2 map {test_event: @test_service2} service test_service2{[echo second service]}'
		self.compiler.text_compile(program)

	def test_can_output_bindless_event(self):
		program = 'sandbox test map{my_event: @test_service} service test_service{[echo execute test service]}'
		self.compiler.text_compile(program)

	def test_comments(self):
		program = 'sandbox test /* this is a comment; sandbox test2 service */ service test_service{}'
		self.compiler.text_compile(program)

	@unittest.expectedFailure
	def test_comments_dont_nest(self):
		program = 'sandbox test /* comment /* more comment service */ */ service test_service{}'
		self.compiler.text_compile(program)

	def test_console_command_in_event(self):
		program = self.blueprint_one_chain + '{ test_event: [echo test_console_command_in_event] }'
		self.compiler.text_compile(program)

	def test_console_command_in_service(self):
		program = self.blueprint_two_chain + '{ a = 7 [echo test_console_command_in_service] }'
		self.compiler.text_compile(program)

	def test_service_call(self):
		program = self.blueprint_two_chain + '{ a = 3 @test_service2} service test_service2 { [echo old input was] a = ?a [echo new ouput is] a = ?5 }'
		self.compiler.text_compile(program)

	def test_event_file(self):
		program = 'sandbox test map { test_event: @test_service } service test_service { [test] } file { scout : test_event }'
		self.compiler.text_compile(program)

	def test_event_boot(self):
		program = 'sandbox test map { boot: @test_service } service test_service {[test]}'
		self.compiler.text_compile(program)

	def test_bifurcation(self):
		program = 'sandbox test map {+test_event : @test_service -test_event : @test_service_2} service test_service {[echo 1]} service test_service_2 {[echo 2]}'
		self.compiler.text_compile(program)

	@unittest.expectedFailure
	def test_lexer_comments_terminate(self):
		program = '/*'
		self.compiler.text_compile(program)
