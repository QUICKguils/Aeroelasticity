"""Flutter identification with the half-power point method."""

from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from scipy.signal import find_peaks, peak_widths

import labdata as ld


def compute_fft_signals(extracted_signals):
    """Extract relevant signal portions, based on manual identification."""
    fft_signals = np.zeros(
        (extracted_signals.shape[0], extracted_signals.shape[1]),
        dtype=ld.ExtractedSignal
    )

    for id_signal, signal in enumerate(extracted_signals.flat):
        fft_pitch = fftshift(fft(signal.pitch))
        ampl_pitch = np.sqrt(fft_pitch.real**2 + fft_pitch.imag**2)[len(fft_pitch)//2:]
        fft_plunge = fftshift(fft(signal.plunge))
        ampl_plunge = np.sqrt(fft_plunge.real**2 + fft_plunge.imag**2)[len(fft_plunge)//2:]
        f_sample = fftshift(fftfreq(signal.var.shape[-1]))*ld.SAMPLING_FREQ_HZ
        f_sample = f_sample[len(f_sample)//2:]
        (id_run, id_bound) = np.unravel_index(id_signal, fft_signals.shape)
        fft_signals[id_run][id_bound] = ld.ExtractedSignal(ampl_pitch, ampl_plunge, f_sample)

    return fft_signals


class HPPresult(NamedTuple):
    signal: np.ndarray
    f_sample: np.ndarray
    fn_idx: int
    fn: float
    f1: float
    f2: float
    half_power: float
    damping: float


def compute_damping_half_power(signal, f_sample):
    """Compute the damping of a signal using the half-power point method."""
    fn_idx, _ = find_peaks(signal, prominence=200)
    halfpeaks_pitch = peak_widths(signal, fn_idx, rel_height=1/np.sqrt(2))
    fn = f_sample[fn_idx]
    f1, f2 = np.interp(
        [halfpeaks_pitch[2], halfpeaks_pitch[3]],
        np.arange(0, f_sample.shape[0]),
        f_sample
    )
    half_power = halfpeaks_pitch[1]
    damping = (f2 - f1) / (2*fn)

    return HPPresult(signal, f_sample, fn_idx, fn, f1, f2, half_power, damping)


def plot_half_power(res: HPPresult):
    plt.plot(res.f_sample, res.signal)
    plt.plot(res.fn, res.signal[res.fn_idx], 'x')
    plt.hlines(res.half_power, res.f1, res.f2, colors='C2')
    plt.show()


extracted_signals = ld.extract_signals(ld.EXTRACT_BOUNDS)
fft_signals = compute_fft_signals(extracted_signals)
signal = fft_signals[5][2]
print(signal)
hpp_res = compute_damping_half_power(signal.pitch, signal.var)
plot_half_power(hpp_res)
