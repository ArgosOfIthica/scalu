import src.backend.generation.abstract_generation as gen
import src.backend.emission.emission as emission
import src.minify.minify as minifier
import src.model.file as files


def compile(global_object):
	debug = False
	gen.compile(global_object)
	raw_program = emission.emission(global_object.universe)
	if debug:
		return raw_program
	minified_program = minifier.minify(raw_program, global_object.universe)
	file_directive = files.file_container(global_object, minified_program)
	return file_directive
