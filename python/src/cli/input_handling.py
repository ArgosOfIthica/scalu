from pathlib import Path

def handle():
	input_directory = Path('../scalu_in')
	if not input_directory.exists():
		input_directory.mkdir()
	string_blob = ''
	files = list(input_directory.glob('**/*.scalu'))
	for f in files:
		string_blob += f.read_text() + '\n'
	return string_blob



