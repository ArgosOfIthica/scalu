import src.backend.generation.abstract_generation as gen
import src.backend.emission.emission as emission
import src.minify.minify as minifier


def compile(global_object):
	debug = False
	uni = gen.compile(global_object)
	raw_program = emission.emission(uni)
	if debug:
		return raw_program
	else:
		minified_program = minifier.minify(raw_program, uni)
		return minified_program
