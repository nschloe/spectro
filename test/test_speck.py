import os

import specky


def test_cli_show():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(this_dir, "samples", "16.mp3")
    specky.cli.show([input_file])


def test_cli_check():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    input_file = os.path.join(this_dir, "samples", "16.mp3")
    specky.cli.check([input_file])
