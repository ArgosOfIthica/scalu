import src.frontend.resolution.resolve_services as services
import src.frontend.resolution.resolve_globals as bindings


def resolve(global_object):
	global_object.sandbox = [resolve_sandbox(sandbox) for sandbox in global_object.sandbox]
	bindings.resolve(global_object)
	return global_object

def resolve_sandbox(sandbox):
	return services.resolve(sandbox)
