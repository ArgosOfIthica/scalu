import src.backend.generation.abstract_generation as gen
import src.backend.emission.emission as emission


def compile(global_object):
	universe = gen.compile(global_object)
	config = emission.emission(universe)
	return config
