import argparse

def handle():
    parser = argparse.ArgumentParser(
            description="an event-based programming language and compiler \
                targeting config files in Valve's Source Engine",
            prog='scalu'
            )
    parser.add_argument(
            'mode',
            action='store',
            choices=['compile', 'test'],
            help='set the mode',
            nargs=1,
            )
    parser.add_argument(
            '--input',
            '-i',
            action='store',
            default='',
            dest='input',
            nargs='+',
            help='specify input files/directories'
            )
    parser.add_argument(
            '--output',
            '-o',
            action='store',
            default='',
            dest='output_dir',
            help='specify output directory'
            )

    args = parser.parse_args()

    if not args:
        raise Exception('scalu must be provided with a command to run: compile, test, etc')

    return args
