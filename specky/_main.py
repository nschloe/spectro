import pathlib

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy
from colorama import Fore, Style
from mutagen.mp3 import MP3
from pydub import AudioSegment
from scipy import signal


def show(
    filename,
    min_freq=1.0e-2,
    num_windows=None,
    num_frequencies=None,
    channel=None,
    outfile=None,
):
    track = AudioSegment.from_file(filename)

    assert track.channels is not None
    out = numpy.array(track.get_array_of_samples()).reshape(-1, track.channels)

    if channel is None:
        channels = range(out.shape[1])
    else:
        channels = [channel - 1]

    if num_windows is None:
        nperseg = None
    else:
        nperseg = int(round(track.duration_seconds / num_windows * track.frame_rate))

    for i, k in enumerate(channels):
        # Perhaps one can downsample this.
        # https://stackoverflow.com/q/60866162/353337
        f, t, Sxx = signal.spectrogram(
            out[:, k],
            fs=track.frame_rate,
            scaling="spectrum",
            mode="magnitude",
            nperseg=nperseg,
        )

        if num_frequencies is not None:
            # ditch some of the frequencies
            f_step = -(-f.shape[0] // num_frequencies)
            f = f[::f_step]
            Sxx = Sxx[::f_step]

        # Make sure all values are positive for the log scaling
        smallest_positive = numpy.min(Sxx[Sxx > 0])
        Sxx[Sxx < smallest_positive] = smallest_positive

        plt.subplot(1, len(channels), i + 1)
        plt.pcolormesh(
            t,
            f,
            Sxx,
            norm=colors.LogNorm(vmin=min_freq, vmax=Sxx.max()),
        )
        plt.title(f"Channel {k + 1}")
        if k == 0:
            plt.ylabel("Frequency [Hz]")
        plt.xlabel("Time [sec]")
        plt.colorbar()

    plt.gcf().suptitle(f"{filename} ({track.channels} channels, {track.frame_rate} Hz)")
    if outfile is None:
        plt.show()
    else:
        plt.savefig(outfile, transparent=True, bbox_inches="tight")


def check(path, **kwargs):
    path = pathlib.Path(path)
    if path.is_file():
        _check_file(path, **kwargs)
        return

    assert path.is_dir()
    for p in path.glob("**/*"):
        if p.suffix in [".mp3", ".wav", ".flac"]:
            _check_file(p, **kwargs)
    return


def _check_file(filename, window_length_s=0.05, channel=0):
    track = AudioSegment.from_file(filename)

    assert track.channels is not None
    out = numpy.array(track.get_array_of_samples()).reshape(-1, track.channels)

    if window_length_s is None:
        nperseg = None
    else:
        nperseg = int(round(window_length_s * track.frame_rate))

    # Use the first channel by default
    f, _, Sxx = signal.spectrogram(
        out[:, channel],
        fs=track.frame_rate,
        scaling="spectrum",
        mode="magnitude",
        # nperseg=window_length_samples
        nperseg=nperseg,
        # noverlap=noverlap
    )
    # Make sure all values are positive for the log scaling
    smallest_positive = numpy.min(Sxx[Sxx > 0])
    Sxx[Sxx < smallest_positive] = smallest_positive
    # Which row surpasses the average first?
    log_Sxx = numpy.log10(Sxx)
    avg_log_Sxx = numpy.average(log_Sxx)
    count = numpy.sum(log_Sxx > avg_log_Sxx, axis=1)
    k = numpy.where(count > log_Sxx.shape[1] / 8)[0][-1]

    # What do we expect?
    # https://stackoverflow.com/a/287944/353337
    filename = pathlib.Path(filename)
    if filename.suffix in [".wav", ".flac"]:
        if f[k] > 19000:
            print(f"{Fore.GREEN}{filename} seems good.{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}{filename} is WAV, but has max frequency "
                f"about {f[k]:.0f} Hz. Check with specky-show.{Style.RESET_ALL}"
            )
    elif filename.suffix == ".mp3":
        mp3_file = MP3(filename)
        bitrate = int(mp3_file.info.bitrate / 1000)
        bitrate_to_min_max_freq = {
            0: 0,
            16: 4000,
            64: 10000,
            128: 15000,
            192: 16000,
            320: 18000,
        }

        for key, val in bitrate_to_min_max_freq.items():
            if bitrate < key:
                break
            expected_max_freq = val

        if f[k] > expected_max_freq:
            print(
                f"{Fore.GREEN}{filename} seems good [{bitrate} kbps].{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.RED}{filename} is MP3 [{bitrate} kbps], but has max frequency "
                f"about {f[k]:.0f} Hz. Check with speck-show.{Style.RESET_ALL}"
            )

    else:
        print(f"{Style.DIM}Don't know what to expect for {filename}.{Style.RESET_ALL}")
