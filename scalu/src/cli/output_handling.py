from pathlib import Path

def handle(output_files, output_directory):
    # use scalu_out in current directory by default
    if not output_directory:
        output_directory = 'scalu_out/'

    output_directory = Path(output_directory)

    if not output_directory.exists():
        output_directory.mkdir()

    for child in output_directory.iterdir():
        child.unlink()

    for cfg in output_files.files:
        output = output_directory.joinpath(cfg.name + '.' + cfg.type)
        output.touch()
        output.write_text(cfg.content)

