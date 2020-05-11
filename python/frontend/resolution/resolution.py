from frontend.resolution.resolve_sandbox import resolver

class resolution():

	def resolve(self, global_object):
		global_object.sandbox = [self.resolve_sandbox(sandbox) for sandbox in global_object.sandbox]
		return global_object

	def resolve_sandbox(self, sandbox):
		new_resolver = resolver()
		return new_resolver.resolve(sandbox)
