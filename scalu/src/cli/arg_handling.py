import argparse

def handle():
    prop = properties()

    parser = argparse.ArgumentParser(
            description="an event-based programming language and compiler targeting config files in Valve's Source Engine"
            )
    parser.add_argument(
            'mode',
            action='store',
            choices=['compile', 'test'],
            help='set the mode',
            nargs=1,
            type=str
            )
    parser.add_argument(
            '--input',
            '-i',
            action='store',
            default='',
            dest='input',
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
    parser.add_argument(
            '--local',
            '-l',
            action='store_true',
            default=False,
            dest='local',
            help='use relative input/output directories'
            )

    args = parser.parse_args()

    if not args:
        raise Exception('scalu must be provided with a command to run: compile, test, help, etc')

    prop.mode = args.mode[0]
    prop.input = args.input
    prop.output_dir = args.output_dir

    # use relative paths to mimick old behavior when specified
    if args.local:
        prop.input = '../scalu_in'
        prop.output_dir = '../scalu_out'

    return prop


class properties():

    def __init__(self):
        self.mode = ''
        self.input = ''
        self.output_dir = ''
