from pathlib import Path


def glob_list(dir):
    return list(dir.glob('**/*.scalu'))

# find and return a list of scalu files from a list of paths
def get_files(input):
    files = []

    for f in input:
        path = Path(f)
        if path.is_dir():
            files += glob_list(path)
        elif path.is_file():
            files.append(path)
        else:
            raise Exception("{} doesn't exist or is not a valid input!".format(f))

    return files

def handle(input):
    # use scalu_in/ in the current directory by default
    if not input:
        input = 'scalu_in/'
        if not Path(input).exists():
            Path(input).mkdir()
    # input needs to always be a list for get_files()
    if type(input) != list:
        input = input.split()

    files = get_files(input)

    string_blob = ''
    for f in files:
        string_blob += f.read_text() + '\n'

    return string_blob
