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
    parser.add_argument(
        '--noremove',
        '-n',
        action='store_false',
        default=True,
        dest='remove',
        help='don\'t remove files from output directory when compiling'
    )
    parser.add_argument(
        '--eventprefix',
        action='store',
        default='$',
        nargs='?',
        const='',
        dest='eventprefix',
        help='Experimental: specify the event prefix'
    )
    parser.add_argument(
        '--aliasprefix',
        action='store',
        default='%',
        nargs='?',
        const='',
        dest='aliasprefix',
        help='Experimental: specify the prefix used for internal aliases'
    )
    parser.add_argument(
        '--forcewordsize',
        action='store',
        default='8',
        nargs='?',
        const='',
        dest='forcewordsize',
        help='Experimental: force a maximum word size.'
    )
    parser.add_argument(
        '--enablemacros',
        action='store',
        default=False,
        nargs='?',
        const='',
        dest='enablemacros',
        help='Unstable: enable compile time macros.'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        dest='debug',
        help='Unused: run in debug mode'
    )

    args = parser.parse_args()

    if not args:
        raise Exception('scalu must be provided with a command to run: compile, test, etc')

    return args

args = handle()