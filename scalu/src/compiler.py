import scalu.src.preprocess.preprocess as preprocess
import scalu.src.frontend.frontend as frontend_manager
import scalu.src.backend.backend as backend_manager
import scalu.src.preprocess.macro as preprocess_manager

class compiler():

    def compile(self, program):
        expanded_program = preprocess_manager.compile(program)
        enriched_syntax_tree = frontend_manager.compile(expanded_program)
        compiled_file_directives = backend_manager.compile(enriched_syntax_tree)
        return compiled_file_directives

    def text_compile(self, program):
        expanded_program = preprocess_manager.compile(program)
        enriched_syntax_tree = frontend_manager.compile(program)
        compiled_file_directives = backend_manager.compile(enriched_syntax_tree)
        text_blob = ''
        for host in compiled_file_directives.host_files:
            text_blob += host.content
        return text_blob
