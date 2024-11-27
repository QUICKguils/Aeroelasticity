"""Flutter identification with the half-power point method (HPPM)."""

from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from scipy.signal import find_peaks, peak_widths

import labdata as ld


def compute_fft_signals(extracted_signals):
    """Extract relevant signal portions, based on manual identification."""
    fft_signals = np.zeros(extracted_signals.shape[:2], dtype=ld.ExtractedSignal)

    for id_signal, signal in enumerate(extracted_signals.flat):
        fft_pitch = fftshift(fft(signal.pitch))
        ampl_pitch = np.sqrt(fft_pitch.real**2 + fft_pitch.imag**2)[len(fft_pitch)//2:]
        fft_plunge = fftshift(fft(signal.plunge))
        ampl_plunge = np.sqrt(fft_plunge.real**2 + fft_plunge.imag**2)[len(fft_plunge)//2:]
        f_sample = fftshift(fftfreq(signal.var.shape[-1]))*ld.SAMPLING_FREQ_HZ
        f_sample = f_sample[len(f_sample)//2:]
        (id_run, id_bound) = np.unravel_index(id_signal, fft_signals.shape)
        fft_signals[id_run][id_bound] = ld.ExtractedSignal(
            id       = id_bound,
            id_run   = id_run,
            airspeed = signal.airspeed,
            pitch    = ampl_pitch,
            plunge   = ampl_plunge,
            var      = f_sample
        )

    return fft_signals


class HppmResult(NamedTuple):
    fn_idx: int
    fn: float
    f1: float
    f2: float
    half_power: float
    damping: float


def half_power_point_method(fft_sample: np.ndarray, freq_sample: np.ndarray) -> HppmResult:
    """Apply the half-power point method to a given signal and its frequency sample."""

    # fn_idx, _ = find_peaks(fft_sample, prominence=200)
    # halfpeaks_pitch = peak_widths(fft_sample, fn_idx, rel_height=1/np.sqrt(2))
    # TODO: maybe more robust with max
    fn_idx = np.argmax(fft_sample)
    halfpeaks_pitch = peak_widths(fft_sample, [fn_idx], rel_height=1/np.sqrt(2))
    fn = freq_sample[fn_idx]
    f1, f2 = np.interp(
        [halfpeaks_pitch[2], halfpeaks_pitch[3]],
        np.arange(0, len(freq_sample)),
        freq_sample
    )
    half_power = halfpeaks_pitch[1]
    damping = (f2 - f1) / (2*fn)

    return HppmResult(
        fn_idx      = fn_idx,
        fn          = fn,
        f1          = f1,
        f2          = f2,
        half_power  = half_power,
        damping     = damping
    )


class HppmSignal(NamedTuple):
        fft: ld.ExtractedSignal
        pitch: HppmResult
        plunge: HppmResult


def get_hppm_signal(fft_signal: ld.ExtractedSignal) -> HppmSignal:
    hppm_pitch = half_power_point_method(fft_signal.pitch, fft_signal.var)
    hppm_plunge = half_power_point_method(fft_signal.plunge, fft_signal.var)

    return HppmSignal(
        fft    = fft_signal,
        pitch  = hppm_pitch,
        plunge = hppm_plunge,
    )


def plot_half_power(hppm_signal: HppmSignal, fig=None):
    """Plot the amplitude FFT of accelerations with HPPM computed quantities."""

    fig = plt.figure()
    fig.suptitle((
        "Half-power point method"
        f" (run: {signal_run[0].id_run}"
        f" -- airspeed: {signal_run[0].airspeed} m/s)"
    ))
    fig.supxlabel("Frequency (Hz)")
    fig.supylabel("Acceleration FFT amplitude")
    gs = fig.add_gridspec(2, 1, hspace=0.3)
    (ax_pitch, ax_plunge) = gs.subplots()

    ax_pitch.plot(hppm_signal.fft.var, hppm_signal.fft.pitch)
    ax_pitch.plot(hppm_signal.pitch.fn, hppm_signal.fft.pitch[hppm_signal.pitch.fn_idx], 'x')
    ax_pitch.hlines(hppm_signal.pitch.half_power, hppm_signal.pitch.f1, hppm_signal.pitch.f2, colors='C2')
    ax_pitch.set_title("Pitch")
    ax_plunge.plot(hppm_signal.fft.var, hppm_signal.fft.plunge)
    ax_plunge.plot(hppm_signal.plunge.fn, hppm_signal.fft.plunge[hppm_signal.plunge.fn_idx], 'x')
    ax_plunge.hlines(hppm_signal.plunge.half_power, hppm_signal.plunge.f1, hppm_signal.plunge.f2, colors='C2')
    ax_plunge.set_title("Plunge")

    fig.show()


if __name__ == '__main__':
    extracted_signals = ld.extract_signals(ld.EXTRACT_BOUNDS)
    fft_signals = compute_fft_signals(extracted_signals)

    # for id_run, signal_run in enumerate(extracted_signals):
    #     for id_signal, signal in enumerate(signal_run):
    #         plt.plot(signal.var, signal.plunge)
    #         plt.title(f"run: {id_run} -- signal: {id_signal}")
    #     plt.show()

    for signal_run in fft_signals:
        for signal in signal_run:
            hppm_signal = get_hppm_signal(signal)
            print(
                hppm_signal.pitch.fn,
                hppm_signal.pitch.f1,
                hppm_signal.pitch.f2,
                hppm_signal.pitch.damping
            )

    # check one freq
    plot_half_power(get_hppm_signal(fft_signals[1][0]))
