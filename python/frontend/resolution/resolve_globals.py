

def resolve(global_object):
	resolve_binding(global_object)
	resolve_mapping(global_object)



def resolve_binding(global_object):
	for sandbox in global_object.sandbox:
		for key in sandbox.bind:
			if key not in global_object.bind:
				global_object.bind[key] = sandbox.bind[key]
			else:
				resolution_error()

def resolve_mapping(global_object):
	events = global_object.bind.values()
	for sandbox in global_object.sandbox:
		for event_string in sandbox.map:
			event_key = None
			for event in events:
				if event_string == event.value:
					event_key = event
					break
			if event_key == None:
				resolution_error()
			elif event_key in global_object.map:
				global_object.map[event_key] += sandbox.map[event_string]
			else:
				global_object.map[event_key] = sandbox.map[event_string]


def resolution_error():
	raise Exception('Resolution error')

