"""Flutter identification with the half power point method."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq

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
        f_sample = fftshift(fftfreq(signal.var_sample.shape[-1]))*ld.SAMPLING_FREQ_HZ
        f_sample = f_sample[len(f_sample)//2:]
        (id_run, id_bound) = np.unravel_index(id_signal, fft_signals.shape)
        fft_signals[id_run][id_bound] = ld.ExtractedSignal(ampl_pitch, ampl_plunge, f_sample)

    return fft_signals


extracted_signals = ld.extract_signals(ld.EXTRACT_BOUNDS)
fft_signals = compute_fft_signals(extracted_signals)

plt.plot(fft_signals[5][2].var_sample, np.sqrt(fft_signals[5][2].pitch.real**2 +fft_signals[5][2].pitch.imag**2))
plt.show()
