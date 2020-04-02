
from frontend.parser.structure import unary_operator
from frontend.parser.structure import service


class core_service_resolver():

	def __init__(self):
		self.s_bprint = self.bprint()

	def core_service_list(self):
		return ('bprint')


	def get_service_object(self, identity):
		service_map = {
			'bprint': self.s_bprint
		}
		return service_map[identity]

	class bprint(service):
		name = 'bprint'
		arg = 1

		def definition(self, args):
			i_bprint = unary_operator()
			i_bprint.identity = 'bprint'
			i_bprint.arg[0] = args[0].identifier
			i_bprint.output = args[0].identifier
			return i_bprint


