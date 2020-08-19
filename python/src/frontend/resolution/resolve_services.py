
import src.frontend.utility.utility as utility
import src.model.structure as model


def resolve(sandbox):
	for event in sandbox.map:
		for service in sandbox.map[event]:
			if model.is_service_call(service):
				resolve_service_call(sandbox, service)
	for service in sandbox.service:
		resolve_service(sandbox, service)

	return sandbox

def resolution_error():
	raise Exception("Resolution error")


def resolve_service(sandbox, service):
	for statement in service.sequence:
		if model.is_service_call(statement):
			resolve_service_call(sandbox, statement)

def resolve_service_call(sandbox, call):
	call.identifier = resolve_service_call_write(sandbox, call.identifier)

def resolve_service_call_write(sandbox, call_identifier):
	for service in sandbox.service:
		if call_identifier == service.name:
			return service
	resolution_error()
