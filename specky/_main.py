import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy
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
