import pathlib

import spectro

this_dir = pathlib.Path(__file__).resolve().parent


def test_cli_show():
    input_file = this_dir / "samples" / "16.mp3"
    spectro.cli.main(["show", str(input_file)])


def test_cli_check():
    input_file = this_dir / "samples" / "16.mp3"
    spectro.cli.main(["check", str(input_file)])
