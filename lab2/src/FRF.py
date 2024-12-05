import numpy as np

def compute_FRF(time, amplitude, min_freq = 0, max_freq = 50) :
    frequencies = np.fft.fftfreq(len(time), d=time[1]-time[0])
    idx_freq    = np.where((frequencies > min_freq) & (frequencies < max_freq))[0]
    frequencies = frequencies[idx_freq]
    fft_values  = np.fft.fft(amplitude)
    magnitudes  = np.abs(fft_values)
    magnitudes  = magnitudes[idx_freq]
    return magnitudes, frequencies
