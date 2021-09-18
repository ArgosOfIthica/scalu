import src.preprocess.preprocess as preprocess
import src.frontend.frontend as frontend_manager
import src.backend.backend as backend_manager

class compiler():

    def compile(self, program):
        enriched_syntax_tree = frontend_manager.compile(program)
        compiled_file_directives = backend_manager.compile(enriched_syntax_tree)
        return compiled_file_directives

    def text_compile(self, program):
        enriched_syntax_tree = frontend_manager.compile(program)
        compiled_file_directives = backend_manager.compile(enriched_syntax_tree)
        text_blob = ''
        for host in compiled_file_directives.host_files:
            text_blob += host.content
        return text_blob
