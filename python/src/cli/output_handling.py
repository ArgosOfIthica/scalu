from pathlib import Path

def handle(output_files):
	output_directory = Path('../scalu_out')
	if not output_directory.exists():
		output_directory.mkdir()
	for child in output_directory.iterdir():
		child.unlink()
	for cfg in output_files.files:
		output = Path('../scalu_out/' + cfg.name + '.' + cfg.type)
		output.touch()
		output.write_text(cfg.content)

