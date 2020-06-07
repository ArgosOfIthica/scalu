
from frontend.utility.utility import *
import model.structure as s
import frontend.service_definitions.service as core


def resolve(sandbox):
	for service in sandbox.service:
		resolve_service(sandbox, service)

	return sandbox

def resolution_error():
	raise Exception("Resolution error")


def resolve_service(sandbox, service):
	for statement in service.sequence:
		if s.is_service_call(statement):
			resolve_service_call(sandbox, statement)

def resolve_service_call(sandbox, call):
	call.identifier = resolve_service_call_write(sandbox, call.identifier)

def resolve_service_call_write(sandbox, call_identifier):
	if call_identifier in core.core_service_list():
		return core.get_service_object(call_identifier)
	for service in sandbox.service:
		if call_identifier == service.name:
			return service
	resolution_error()

