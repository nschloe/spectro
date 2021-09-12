<p align="center">
  <a href="https://github.com/nschloe/spectro"><img alt="spectro" src="https://nschloe.github.io/spectro/spectro-logo.svg" width="50%"></a>
  <p align="center">Delicious audio file spectrograms.</p>
</p>

[![PyPi Version](https://img.shields.io/pypi/v/spectro.svg?style=flat-square)](https://pypi.org/project/spectro)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/spectro.svg?style=flat-square)](https://pypi.org/pypi/spectro/)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/spectro.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/spectro)
[![PyPi downloads](https://img.shields.io/pypi/dm/spectro.svg?style=flat-square)](https://pypistats.org/packages/spectro)

[![gh-actions](https://img.shields.io/github/workflow/status/nschloe/spectro/ci?style=flat-square)](https://github.com/nschloe/spectro/actions?query=workflow%3Aci)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/spectro.svg?style=flat-square)](https://codecov.io/gh/nschloe/spectro)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

spectro is a collection of easy-to-use Python and command-line tools for analyzing audio
files. Install from [PyPi](https://pypi.org/project/spectro/) with
```
pip install spectro
```
and use with
```bash
spectro show filename.mp3                # shows the wave spectrum of the audio file
spectro check {dirname or filename.mp3}  # checks if the audio file is worse than it pretends to be
```
See `-h` for their respective command-line arguments.

The quality of MP3 files is typically determined by their bitrate. For audio files, *128
kbps* (kilobit per second) is considered low quality, *320 kbps* is considered high
quality. It is of course possible to re-encode a low-quality MP3 with a higher bitrate
or even a WAV file. spectro can help singling out those foul eggs.

Here is the `spectro show` output of a [sample
file](https://nschloe.github.io/spectro/Yamaha-V50-Ride-Pattern-120bpm.wav) (only first
channel shown):

<img src="https://nschloe.github.io/spectro/wav.png" width="100%"> | <img src="https://nschloe.github.io/spectro/320.png" width="100%"> | <img src="https://nschloe.github.io/spectro/256.png" width="100%">
:-------------------:|:------------------:|:--------------:|
Full-quality WAV     |  320 kbps MP3      |  256 kbps MP3  |
<img src="https://nschloe.github.io/spectro/192.png" width="100%"> | <img src="https://nschloe.github.io/spectro/128.png" width="100%"> | <img src="https://nschloe.github.io/spectro/96.png" width="100%">
|  192 kbps MP3      |  128 kbps MP3  |  96 kbps MP3  |
<img src="https://nschloe.github.io/spectro/64.png" width="100%"> | <img src="https://nschloe.github.io/spectro/32.png" width="100%"> | <img src="https://nschloe.github.io/spectro/16.png" width="100%">
|  64 kbps MP3      |  32 kbps MP3  |  16 kbps MP3  |
