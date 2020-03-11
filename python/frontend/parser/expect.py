"""
EBNF

block = { statement }
statement = assignment | service_call
service_call = ename '(' { vname [,]} ')'
assignment = vname '=' exp
exp = ( p_exp | exp binop exp | unop exp | value)
p_exp = '(' exp ')'
binop = '=' | '|' | '&'
unop = '~'

"""
from frontend.parser.structure import *
import re


class recursive_descent():


	def __init__(self, tokens):
		self.consumer = consumer(tokens)


	def parse(self):
		return self.global_context()



	def global_context(self):
		global_object = self.expect_block()
		return global_object


	def expect_block(self):
		new_block = block()
		while self.consumer.is_not_end_block():
			if self.consumer.is_variable_assignment():
				new_assignment = self.expect_assignment()
				new_block.sequence.append(new_assignment)
			elif self.consumer.is_service_call():
				new_service_call = self.expect_service_call()
				new_block.sequence.append(new_service_call)
			else:
				parsing_error(self.consumer)
		return new_block


	def expect_service_call(self):
		new_service_call = service_call()
		new_service_call.identifier = self.consumer.use_if_name()
		self.consumer.consume('(')
		while self.consumer.is_not_end_service_call():
			arg = self.expect_expression()
			new_service_call.arg.append(arg)
			if self.consumer.is_not_end_service_call():
				self.consumer.consume(',')
		self.consumer.consume(')')
		return new_service_call



	def expect_assignment(self):
		new_assignment = assignment()
		new_assignment.identifier = self.expect_assignment_write()
		new_assignment.arg[0] = self.expect_expression()
		return new_assignment

	def expect_assignment_write(self):
		write = self.consumer.use_if_name()
		self.consumer.consume('=')
		return write


	def expect_p_expression(self):
		self.consumer.consume('(')
		new_expression = self.expect_expression()
		self.consumer.consume(')')
		return new_expression

	def expect_expression(self):
		new_expression = ''

		if self.consumer.is_unop():
			new_expression = self.expect_unop()

		elif self.consumer.is_subexpression():
			new_expression = self.expect_p_expression()

		elif self.consumer.is_unchained_value():
			new_expression = self.consumer.token()
			self.consumer.consume()

		else:
			new_expression = self.expect_binop()

		while self.consumer.is_binop():
			new_expression = self.expect_binop(new_expression)
			#this handles the case of binary "chaining" where order of operations is ambiguous.
			#the expression is nested into the first argument of a binary operation object.
			#this nesting produces left-to-right evaluation without operator precedence.


		return new_expression


	def expect_argument(self):
		arg = ''
		if self.consumer.is_subexpression():
			arg = self.expect_p_expression()
		elif self.consumer.token_is_value():
			arg = self.consumer.token()
			self.consumer.consume()
		else:
			parsing_error(self.consumer)
		return arg

	def expect_unop(self):
		new_unop = unary_operator()
		new_unop.identity = self.consumer.retrieve_identity()
		self.consumer.consume()
		new_unop.arg[0] = self.expect_argument()
		return new_unop

	def expect_binop(self, chain=None):
		new_binop = binary_operator()
		if chain is None:
			new_binop.arg[0] = self.expect_argument()
		else:
			new_binop.arg[0] = chain
		if self.consumer.is_binop():
			new_binop.identity = self.consumer.retrieve_identity()
			self.consumer.consume()
		else:
			parsing_error(parser)
		new_binop.arg[1] = self.expect_argument()
		return new_binop


