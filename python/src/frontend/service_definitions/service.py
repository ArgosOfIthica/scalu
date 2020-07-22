
import src.model.structure as model



def core_service_list():
	return ('bprint')


def get_service_object(identity):
	service_map = {
		'bprint': bprint()
	}
	return service_map[identity]

class bprint(model.service):
	name = 'bprint'
	arg = 1

	def definition(self, args):
		i_bprint = unary_operator()
		i_bprint.identity = 'bprint'
		i_bprint.arg[0] = args[0].identifier
		i_bprint.output = args[0].identifier
		return i_bprint


