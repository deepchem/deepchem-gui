from __future__ import print_function, absolute_import, division

import sys
import argparse

from ..version import version as  __version__
from . import parser_server


def main():
    help = 'deepchem-gui is a visualization tool for deep-learning models in Chemistry.'
    p = argparse.ArgumentParser(description=help)
    p.add_argument(
        '-V', '--version',
        action='version',
        version='deepchem-gui %s' % __version__,
    )
    sub_parsers = p.add_subparsers(
        metavar='command',
        dest='cmd',
    )

    parser_server.configure_parser(sub_parsers)

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    args = p.parse_args()
    args_func(args, p)


def args_func(args, p):
    try:
        args.func(args, p)
    except RuntimeError as e:
        sys.exit("Error: %s" % e)
    except Exception as e:
        if e.__class__.__name__ not in ('ScannerError', 'ParserError'):
            message = """\
An unexpected error has occurred with deepchem-gui (version %s), please
consider sending the following traceback to the deepchem-gui GitHub issue tracker at:
        https://github.com/deepchem/deepchem-gui/issues
"""
            print(message % __version__, file=sys.stderr)
        raise # as if we did not catch it
