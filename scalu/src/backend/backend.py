import scalu.src.backend.generation.abstract_generation as gen
import scalu.src.backend.emission.emission as emission
import scalu.src.minify.minify as minifier
import scalu.src.model.file as files
import scalu.src.cli.arg_handling as arg_handler


def compile(global_object):
    gen.compile(global_object)
    raw_program = emission.emission(global_object.universe)
    if arg_handler.args.debug:
        print(raw_program)
    minified_program = minifier.minify(raw_program, global_object.universe)
    file_directive = files.file_container(global_object, minified_program)
    return file_directive
