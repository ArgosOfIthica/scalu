
from frontend.parser.structure import unary_operator
from frontend.parser.structure import service


class core_service_resolver():

	def core_service_list(self):
		return ('bprint')


	def get_service_object(self, identity):
		service_map = {
			'bprint': self.bprint
		}
		return service_map[identity]

	class bprint(service):
		name = 'bprint'
		arg = ['target']

