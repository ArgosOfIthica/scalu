import backend.generation.abstract_generation as gen
import backend.emission.emission as emission


def compile(global_object):
	computation_tree = gen.compile(global_object)
	config = emission.emit(computation_tree, global_object.universe)
	return config
