import scalu.src.cli.arg_handling as arg_handler
import scalu.src.model.universe as model
import scalu.src.backend.instructions.instruction as instr_handler
import scalu.src.model.structure as structure


def compile(global_object):
    build_services(global_object)
    build_events(global_object)
    build_bindings(global_object)
    return global_object.universe


def build_services(global_object):
    uni = global_object.universe
    for sandbox in global_object.sandbox:
        global_object.current_sandbox = sandbox
        for service in sandbox.services:
            prebuild_service(global_object, service)
        for service in sandbox.services:
            compute = uni.constructs[service]
            compute = build_service(global_object, service, compute)
    global_object.current_sandbox = None


def build_bindings(global_object):
    uni = global_object.universe
    for event in global_object.maps.maps:
        if event.key is not None:
            event_compute = uni.constructs[event]
            uni.root.extend(model.bind(event.key, event_compute))

def build_events(global_object):
    uni = global_object.universe
    for event in global_object.maps.maps:
        event_def = uni.new_def('event')
        build_event_prefix(event, event_def)
        if event.string == 'boot':
            uni.root.extend(event_def.alias)
        uni.constructs[event] = event_def
        for service_call in event.services:
            if structure.is_source_call(service_call):
                new_source_command = model.source_command(service_call.arg[0])
                event_def.extend(new_source_command)
            else:
                event_def.extend(uni.constructs[service_call.identifier].alias)

def build_event_prefix(event, event_def):
    args = arg_handler.args
    if event.string[0] == '+' or event.string[0] == '-':
        event_def.alias.string = event.string[0] + args.eventprefix + event.string[1:]
    else:
        event_def.alias.string = args.eventprefix + event.string

def prebuild_service(global_object, service):
    uni = global_object.universe
    service_def = uni.new_def('service')
    uni.constructs[service] = service_def
    return service_def


def build_service(global_object, service, definition):
    uni = global_object.universe
    for statement in service.sequence:
        if structure.is_source_call(statement):
            new_source_command = model.source_command(statement.arg[0])
            definition.extend(new_source_command)
        elif structure.is_service_call(statement):
            call_compute = uni.constructs[statement.identifier]
            definition.extend(call_compute.alias)
        elif structure.is_operator(statement):
            instr_handler.handle_instruction(global_object, definition, statement)
        elif structure.is_if_statement(statement):
            instr_handler.handle_conditional(global_object, definition, statement)
        elif structure.is_jump_statement(statement):
            instr_handler.handle_jump(global_object, definition, statement)
        else:
            raise Exception('error: an impossible statement has been created')
    return definition
