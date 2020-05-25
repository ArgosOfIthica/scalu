import frontend.resolution.resolve_sandbox as resolver


def resolve(global_object):
	global_object.sandbox = [resolve_sandbox(sandbox) for sandbox in global_object.sandbox]
	return global_object

def resolve_sandbox(sandbox):
	return resolver.resolve(sandbox)
