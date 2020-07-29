import src.backend.generation.abstract_generation as gen
import src.backend.emission.emission as emission
import src.minify.minify as minifier


def compile(global_object):
	uni = gen.compile(global_object)
	raw_program = emission.emission(uni)
	minified_program = minifier.minify(raw_program, uni)
	return minified_program
