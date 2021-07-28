import argparse
from importlib import metadata
from sys import version_info

from . import _main


def main(argv=None):
    parent_parser = argparse.ArgumentParser(
        description="Audio spectrum analysis.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parent_parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=_get_version_text(),
        help="display version information",
    )

    subparsers = parent_parser.add_subparsers(
        title="subcommands", dest="command", required=True
    )

    parser = subparsers.add_parser(
        "show", help="Show frequency spectrum", aliases=["s"]
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
        "-w",
        "--num-windows",
        default=300,
        type=int,
        help="number of windows (x-axis resolution, default: 300)",
    )
    parser.add_argument(
        "-f",
        "--num-frequencies",
        default=300,
        type=int,
        help="number of frequencies (y-axis resolution, default: 300)",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        default=None,
        type=str,
        help="output file (default: show on screen)",
    )
    parser.set_defaults(
        func=lambda args: _main.show(
            args.filename,
            num_windows=args.num_windows,
            num_frequencies=args.num_frequencies,
            channel=args.channel,
            outfile=args.outfile,
        )
    )

    parser = subparsers.add_parser("check", help="Check frequency range", aliases=["c"])
    parser.add_argument("path", type=str, help="audio file or directory to analyze")
    parser.set_defaults(func=lambda args: _main.check(args.path))

    args = parent_parser.parse_args(argv)

    return args.func(args)


def _get_version_text():
    __version__ = metadata.version("spectro")
    python_version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    return "\n".join(
        [
            f"spectro {__version__} [Python {python_version}]",
            "Copyright (c) 2020-2021 Nico Schlömer",
        ]
    )
