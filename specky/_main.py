from colorama import Fore, Back, Style
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy
import os
from pydub import AudioSegment
from scipy import signal


def show(filename, min_freq=1.0e-2, window_length_s=0.05):
    track = AudioSegment.from_file(filename)

    out = numpy.array(track.get_array_of_samples()).reshape(-1, track.channels)

    if window_length_s is None:
        nperseg = None
    else:
        nperseg = int(round(window_length_s * track.frame_rate))

    # overlap = 0.5
    # noverlap = int(round(overlap * window_length_samples))

    for k in range(out.shape[1]):
        f, t, Sxx = signal.spectrogram(
            out[:, k],
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

        # # Which row surpasses the average first?
        # log_Sxx = numpy.log10(Sxx)
        # avg_log_Sxx = numpy.average(log_Sxx)
        # count = numpy.sum(log_Sxx > avg_log_Sxx, axis=1)
        # k = numpy.where(count > log_Sxx.shape[1] / 4)[0][-1]

        plt.subplot(1, out.shape[1], k + 1)
        plt.pcolormesh(
            t, f, Sxx, norm=colors.LogNorm(vmin=min_freq, vmax=Sxx.max()),
        )
        plt.title(f"Channel {k + 1}")
        if k == 0:
            plt.ylabel("Frequency [Hz]")
        plt.xlabel("Time [sec]")
        plt.colorbar()

    plt.gcf().suptitle(f"{filename} ({track.channels} channels, {track.frame_rate} Hz)")
    plt.show()


def check(filename, min_freq=1.0e-2, window_length_s=0.05, channel=0):
    track = AudioSegment.from_file(filename)

    out = numpy.array(track.get_array_of_samples()).reshape(-1, track.channels)

    if window_length_s is None:
        nperseg = None
    else:
        nperseg = int(round(window_length_s * track.frame_rate))

    # Use the first channel by default
    f, t, Sxx = signal.spectrogram(
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
    if os.path.splitext(filename)[-1].lower() == ".wav":
        if f[k] > 19000:
            print(f"{Fore.GREEN}{filename} seems good.{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED}{filename} is WAV, but has max frequency "
                f"about {f[k]:.0f} Hz. Check with speck-show.{Style.RESET_ALL}"
            )
    # elif os.path.splitext(filename)[-1].lower() == ".mp3":
    #     pass
    else:
        print(f"{Style.DIM}Don't know what to expect for {filename}.{Style.RESET_ALL}")
