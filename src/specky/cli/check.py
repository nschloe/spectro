import sys

from ..__about__ import __version__
from .._main import check as main_check


def check(argv=None):
    # Parse command line arguments.
    parser = _get_parser()
    args = parser.parse_args(argv)
    main_check(args.path)


def _get_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description=("Check spectrum of audio file"),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("path", type=str, help="audio file or directory to analyze")

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
