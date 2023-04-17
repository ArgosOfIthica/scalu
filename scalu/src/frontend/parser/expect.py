import scalu.src.model.structure as model
import scalu.src.frontend.utility.utility as utility
import scalu.src.model.consumer as consume
import re

def parse(tokens):
    consumer_obj = consume.consumer(tokens)
    return global_context(consumer_obj)


def global_context(consumer):
    new_global_object = model.global_object()
    consumer.global_object = new_global_object
    while consumer.is_sandbox():
        new_sandbox = expect_sandbox(consumer)
    if consumer.token() == '':
        new_global_object.resolve()
        new_global_object.current_sandbox = None
        return new_global_object
    else:
        consume.parsing_error(consumer)


def expect_sandbox(consumer):
    consumer.consume('sandbox')
    new_sandbox = consumer.global_object.sandbox.declare(consumer.token())
    consumer.current_sandbox = new_sandbox
    consumer.consume()
    while consumer.is_block():
        block_type = consumer.token()
        if block_type == 'service':
            new_block = expect_service_block(consumer)
        elif block_type == 'map':
            new_block = expect_map_block(consumer)
        elif block_type == 'bind':
            new_block = expect_bind_block(consumer)
        elif block_type == 'file':
            new_block = expect_file_block(consumer)
        else:
            consume.parsing_error(consumer, 'invalid block type error')
    return new_sandbox


def expect_bind_block(consumer):
    binding = consumer.global_object.maps
    consumer.consume('bind')
    consumer.consume('{')
    while consumer.is_not_end_block():
        new_key = consumer.token()
        consumer.consume()
        consumer.consume(':')
        new_event = model.event(consumer.token())
        consumer.consume()
        new_event.add_key(new_key)
        binding.add(new_event)
    consumer.consume('}')
    return binding

def expect_map_block(consumer):
    mapping = consumer.global_object.maps
    consumer.consume('map')
    consumer.consume('{')
    while consumer.is_not_end_block():
        new_event = model.event(consumer.token())
        consumer.consume()
        consumer.consume(':')
        call = expect_call(consumer)
        new_event.services.append(call)
        mapping.add(new_event)
    consumer.consume('}')
    return mapping

def expect_file_block(consumer):
    file_map = consumer.global_object.maps
    consumer.consume('file')
    consumer.consume('{')
    while consumer.is_not_end_block():
        new_file = consumer.token()
        consumer.consume()
        consumer.consume(':')
        new_event = model.event(consumer.token())
        consumer.consume()
        new_event.add_file(new_file)
        file_map.add(new_event)
    consumer.consume('}')
    return file_map

def expect_service_block(consumer, named=True):
    new_block = None
    if named:
        consumer.consume('service')
        new_block = consumer.current_sandbox.services.declare(consumer.use_if_name())
    else:
        new_block = model.service()
        new_block.name = ''
        new_block.is_anonymous = True
        new_block.declared = True
        consumer.current_sandbox.services.append(new_block)
    consumer.consume('{')
    while consumer.is_not_end_block():
        if consumer.is_variable_assignment() or consumer.is_sandboxed_assignment():
            new_assignment = expect_assignment(consumer)
            new_block.sequence.append(new_assignment)
        elif consumer.is_service_call():
            new_service_call = expect_service_call(consumer)
            new_block.sequence.append(new_service_call)
        elif consumer.is_source_call():
            new_source_call = expect_source_call(consumer)
            new_block.sequence.append(new_source_call)
        elif consumer.is_if():
            new_if = expect_if(consumer)
            new_block.sequence.append(new_if)
        elif consumer.is_jump():
            new_jump = expect_jump(consumer)
            new_block.sequence.append(new_jump)
        else:
            consume.parsing_error(consumer, 'invalid statement error')
    consumer.consume('}')
    return new_block

def empty_service(consumer):
    new_block = model.service()
    new_block.name = ''
    new_block.is_anonymous = True
    new_block.declared = True
    consumer.current_sandbox.services.append(new_block)
    return new_block

def expect_if(consumer):
    new_if = model.if_statement()
    consumer.consume('if')
    if consumer.is_subexpression():
        consumer.consume('(')
        new_if.condition = expect_conditional(consumer)
        consumer.consume(')')
    else:
        new_if.condition = expect_conditional(consumer)
    new_if.true_service = expect_service_block(consumer, False)
    if consumer.is_else():
        consumer.consume('else')
        new_if.false_service = expect_service_block(consumer, False)

    else:
        new_if.false_service = empty_service(consumer)
    return new_if

def expect_jump(consumer):
    new_jump = model.jump_statement()
    consumer.consume('jump')
    if consumer.is_subexpression():
        consumer.consume('(')
        new_jump.var = expect_jump_identifier(consumer)
        consumer.consume(')')
    else:
        new_jump.var = expect_jump_identifier(consumer)
    consumer.consume('{')
    while consumer.is_not_end_block():
        new_jump.services.append(expect_service_block(consumer, False))
    consumer.consume('}')
    return new_jump


def expect_jump_identifier(consumer):
    sandbox = ''
    if consumer.is_sandboxed_assignment():
        sandbox = consumer.use_if_name()
        consumer.consume('.')
    if sandbox == '':
        sandbox = consumer.current_sandbox
    else:
        sandbox = consumer.global_object.sandbox.reference(sandbox)
    identifier = consumer.use_if_name()
    var = sandbox.variables.reference(identifier)
    return var


def expect_call(consumer):
    if consumer.is_service_call():
        return expect_service_call(consumer)
    elif consumer.is_source_call():
        return expect_source_call(consumer)
    else:
        consume.parsing_error(consumer, 'invalid call error')

def expect_source_call(consumer):
    new_source_call = model.source_call()
    consumer.consume('[')
    new_source_call.arg[0] = consumer.token().replace("\]", "]")
    new_source_call.identifier = '[' + consumer.token() + ']'
    consumer.consume()
    consumer.consume(']')
    return new_source_call

def expect_service_call(consumer):
    consumer.consume('@')
    new_service_call = model.service_call()
    new_service_call.identifier = consumer.current_sandbox.services.reference(consumer.use_if_name())
    return new_service_call


def expect_assignment(consumer):
    new_assignment = model.assignment()
    new_assignment.identifier = expect_assignment_identifier(consumer)
    consumer.consume('=')
    new_assignment.arg[0] = expect_expression(consumer)
    return new_assignment


def expect_assignment_identifier(consumer):
    sandbox = ''
    if consumer.is_sandboxed_assignment():
        sandbox = consumer.use_if_name()
        consumer.consume('.')
    if sandbox == '':
        sandbox = consumer.current_sandbox
    else:
        sandbox = consumer.global_object.sandbox.reference(sandbox)
    identifier = consumer.use_if_name()
    var = sandbox.variables.reference(identifier)
    if not var.declared:
        return sandbox.variables.declare(identifier)
    else:
        return var

def expect_p_expression(consumer):
    consumer.consume('(')
    new_expression = expect_expression(consumer)
    consumer.consume(')')
    return new_expression

def expect_expression_atomic(consumer):
    if consumer.is_unop():
        return expect_unop(consumer)
    elif consumer.is_subexpression():
        return expect_p_expression(consumer)
    elif consumer.token_is_value():
        return expect_value(consumer)
    else:
        consumer.parsing_error(consumer, 'invalid expression atomic error')

def expect_expression(consumer):
    new_expression = expect_expression_atomic(consumer)
    if consumer.is_binop():
        new_expression = expect_binop(consumer, new_expression)
    return new_expression

def expect_value(consumer):
    sandbox = ''
    if consumer.is_sandboxed_assignment():
        sandbox = consumer.use_if_name()
        consumer.consume('.')
    if sandbox == '':
        sandbox = consumer.current_sandbox
    else:
        sandbox = consumer.global_object.sandbox.reference(sandbox)
    value = consumer.token()
    consumer.consume()
    if utility.token_is_name(value):
        return sandbox.variables.reference(value)
    elif utility.token_is_numeric(value):
        v_const = sandbox.variables.reference(value, model.constant)
        v_const.set_value(value)
        v_const.declared = True
        return v_const
    else:
        consume.parsing_error(consumer, 'invalid variable error')

def expect_conditional(consumer):
    new_cond = model.conditional()
    new_cond.arg[0] = expect_value(consumer)
    new_cond.identity = consumer.retrieve_and_use_conditional()
    new_cond.arg[1] = expect_value(consumer)
    return new_cond


def expect_unop(consumer):
    new_unop = model.unary_operator()
    new_unop.identity = consumer.retrieve_and_use_unary_identity()
    new_unop.arg[0] = expect_expression(consumer)
    return new_unop


def expect_binop(consumer, chain):
    new_binop = model.binary_operator()
    new_binop.arg[0] = chain
    new_binop.identity = consumer.retrieve_and_use_binary_identity()
    new_binop.arg[1] = expect_expression(consumer)
    return new_binop


