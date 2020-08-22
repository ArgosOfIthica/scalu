from pathlib import Path

def handle(output_string):
	output_directory = Path('../scalu_out')
	if not output_directory.exists():
		output_directory.mkdir()
	for child in output_directory.iterdir():
		child.unlink()
	output = Path('../scalu_out/scalu.cfg')
	output.touch()
	output.write_text(output_string)
