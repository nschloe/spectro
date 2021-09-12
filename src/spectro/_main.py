import pathlib
from typing import Optional

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy
from mutagen.mp3 import MP3
from pydub import AudioSegment
from rich.console import Console
from scipy import signal


def show(
    filename: str,
    min_freq: float = 1.0e-2,
    num_windows: Optional[int] = None,
    num_frequencies: Optional[int] = None,
    channel: Optional[int] = None,
    outfile: Optional[str] = None,
):
    track = AudioSegment.from_file(filename)

    assert track.channels is not None
    out = numpy.array(track.get_array_of_samples()).reshape(-1, track.channels)

    channels = range(out.shape[1]) if channel is None else [channel - 1]

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
            shading="auto",
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


def _check_file(filename, window_length_s: float = 0.05, channel: int = 0):
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

    console = Console()

    # What do we expect?
    # https://stackoverflow.com/a/287944/353337
    filename = pathlib.Path(filename)
    if filename.suffix in [".wav", ".flac"]:
        if f[k] > 19000:
            console.print(f"[green]{filename} seems good.")
        else:
            console.print(
                f"[red]{filename} is WAV, but has max frequency "
                f"about {f[k]:.0f} Hz. Check with spectro show."
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
            console.print(f"[green]{filename} seems good [{bitrate} kbps].")
        else:
            console.print(
                f"[red]{filename} is MP3 [{bitrate} kbps], but has max frequency "
                f"about {f[k]:.0f} Hz. Check with speck-show."
            )

    else:
        console.print(f"[italic]Don't know what to expect for {filename}.")
