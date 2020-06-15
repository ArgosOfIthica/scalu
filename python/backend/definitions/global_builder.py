

def generate_binding(bind, event):
	return 'bind ' + bind + ' ' + event

def generate_mapping(event, services):
	mapping = 'alias ' + event + '"'
	for service in services:
		mapping += service.identifier + ';'
	mapping += '"'
	return mapping

