from pathlib import Path

# verify and return list of files in a directory
def dir_list(input_directory):
    if not input_directory.exists():
        input_directory.mkdir()
    files = list(input_directory.glob('**/*.scalu'))
    return files

def handle(input):
    files = []
    if not input:
        # use scalu_in/ in current directory by default
        input_directory = Path('scalu_in/')
        files = dir_list(input_directory)
    elif Path(input).is_dir():
        input_directory = Path(input)
        files = dir_list(input_directory)
    else:
        # just read file when input is not a directory
        if not Path(input).exists():
            raise Exception("{} doesn't exist!".format(input))
        files.append(Path(input))

    string_blob = ''
    for f in files:
        string_blob += f.read_text() + '\n'

    return string_blob
