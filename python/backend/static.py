from backend.definitions.vbuilder import build_variable
from backend.definitions.global_builder import *



def compile(universe, global_object):
	header = alias(
	for key in global_object.bind:
		header += generate_binding(key.value, global_object.bind[key].value) + '\n'
	for event in global_object.map:
		header += generate_mapping(event.value, global_object.map[event]) + '\n'
	for sandbox in global_object.sandbox:
		res = sandbox.resolution
		for var_name in res.variable_lookup:
			var = res.variable_lookup[var_name]
			header += build_variable(var.name, var.word_size, var.value)
		for const_name in res.constant_lookup:
			const = res.constant_lookup[const_name]
			header += build_variable(const.name, const.word_size, const.value)
		return header


def build_header(universe, global_object):
	header = computation(
