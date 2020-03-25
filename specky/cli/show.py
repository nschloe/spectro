import sys

from ..__about__ import __version__
from .._main import show as main_show


def show(argv=None):
    # Parse command line arguments.
    parser = _get_parser()
    args = parser.parse_args(argv)
    main_show(args.filename, channel=args.channel, outfile=args.outfile)


def _get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description=("Show spectrum of audio file"),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("filename", type=str, help="audio file to analyze")

    parser.add_argument(
        "-c",
        "--channel",
        default=None,
        type=int,
        help="only show one particular channel (default: show all channels)",
    )

    parser.add_argument(
        "-o",
        "--outfile",
        default=None,
        type=str,
        help="output file (default: show on screen)",
    )

    version_text = "\n".join(
        [
            "specky {} [Python {}.{}.{}]".format(
                __version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            "Copyright (c) 2020 Nico Schlömer",
        ]
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=version_text,
        help="display version information",
    )

    return parser
