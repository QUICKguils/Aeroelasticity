"""Flutter identification with the half-power point method (HPPM)."""

from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftshift, fftfreq
from scipy.signal import peak_widths

import labdata as ld


def get_fft_signals(extracted_signals):
    """Get the FFTs of extracted signals."""
    fft_signals = np.zeros(extracted_signals.shape, dtype=ld.ExtractedSignal)

    for i_run, signal_run in enumerate(extracted_signals):
        for i_signal, signal in enumerate(signal_run):
            fft_pitch = fftshift(fft(signal.pitch))
            ampl_pitch = np.sqrt(fft_pitch.real**2 + fft_pitch.imag**2)[len(fft_pitch)//2:]
            fft_plunge = fftshift(fft(signal.plunge))
            ampl_plunge = np.sqrt(fft_plunge.real**2 + fft_plunge.imag**2)[len(fft_plunge)//2:]
            f_sample = fftshift(fftfreq(signal.var.shape[-1]))*ld.SAMPLING_FREQ_HZ
            f_sample = f_sample[len(f_sample)//2:]
            fft_signals[i_run][i_signal] = ld.ExtractedSignal(
                id       = i_signal,
                id_run   = i_run,
                airspeed = signal.airspeed,
                pitch    = ampl_pitch,
                plunge   = ampl_plunge,
                var      = f_sample
            )

    return fft_signals


class HppmResult(NamedTuple):
    """Computed quantities from the half-power point method."""
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
    # NOTE: this is more robust with np.argmax
    fn_idx = np.argmax(fft_sample)
    halfpeaks_pitch = peak_widths(fft_sample, [fn_idx], rel_height=1/np.sqrt(2))
    fn = freq_sample[fn_idx]
    f1, f2 = np.interp(
        [halfpeaks_pitch[2][0], halfpeaks_pitch[3][0]],
        np.arange(0, len(freq_sample)),
        freq_sample
    )
    half_power = halfpeaks_pitch[1][0]
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
    """FFTs of an ExtractedSignal, with its HPPM computed quantities."""
    fft: ld.ExtractedSignal
    pitch: HppmResult
    plunge: HppmResult


def get_hppm_signals(fft_signals):
    """Get the HHPM results of extracted signals."""
    hppm_signals = np.zeros(fft_signals.shape, dtype=HppmSignal)

    for i_run, signal_run in enumerate(fft_signals):
        for i_signal, signal in enumerate(signal_run):
            hppm_pitch = half_power_point_method(signal.pitch, signal.var)
            hppm_plunge = half_power_point_method(signal.plunge, signal.var)
            hppm_signals[i_run][i_signal] = HppmSignal(
                fft    = signal,
                pitch  = hppm_pitch,
                plunge = hppm_plunge,
            )

    return hppm_signals


def plot_half_power(hppm_signal: HppmSignal, *, publish=False) -> None:
    """Plot the amplitude FFT of accelerations with its HPPM computed quantities."""
    fig, (ax_pitch, ax_plunge) = plt.subplots(2, 1, figsize=(5.5, 4), layout="constrained")
    if not(publish):
        fig.suptitle((
            "Half-power point method"
            f" (run: {hppm_signal.fft.id_run}"
            f" -- airspeed: {hppm_signal.fft.airspeed} m/s)"
        ))

    ax_pitch.plot(hppm_signal.fft.var, hppm_signal.fft.pitch)
    ax_pitch.plot(hppm_signal.pitch.fn, hppm_signal.fft.pitch[hppm_signal.pitch.fn_idx], 'x')
    ax_pitch.hlines(hppm_signal.pitch.half_power, hppm_signal.pitch.f1, hppm_signal.pitch.f2, colors='C2')
    ax_pitch.set_ylabel(r"$\|\mathrm{FFT}(\ddot{\alpha})\|$/(rad/s²)")

    ax_plunge.plot(hppm_signal.fft.var, hppm_signal.fft.plunge)
    ax_plunge.plot(hppm_signal.plunge.fn, hppm_signal.fft.plunge[hppm_signal.plunge.fn_idx], 'x')
    ax_plunge.hlines(hppm_signal.plunge.half_power, hppm_signal.plunge.f1, hppm_signal.plunge.f2, colors='C2')
    ax_plunge.set_ylabel(r"$\|\mathrm{FFT}(\ddot{h})\|$/(m/s²)")
    ax_plunge.set_xlabel("Signal frequency (Hz)")

    fig.show()


def extract_freq_damp(hppm_signals):
    airspeeds = np.zeros(hppm_signals.shape)
    freq_pitch = np.zeros(hppm_signals.shape)
    damp_pitch = np.zeros(hppm_signals.shape)
    freq_plunge = np.zeros(hppm_signals.shape)
    damp_plunge = np.zeros(hppm_signals.shape)

    for i_run, signal_run in enumerate(hppm_signals):
        for i_signal, signal in enumerate(signal_run):
            airspeeds[i_run][i_signal]   = hppm_signals[i_run][i_signal].fft.airspeed
            freq_pitch[i_run][i_signal]  = hppm_signals[i_run][i_signal].pitch.fn
            damp_pitch[i_run][i_signal]  = hppm_signals[i_run][i_signal].pitch.damping
            freq_plunge[i_run][i_signal] = hppm_signals[i_run][i_signal].plunge.fn
            damp_plunge[i_run][i_signal] = hppm_signals[i_run][i_signal].plunge.damping

    return (airspeeds, freq_pitch, damp_pitch, freq_plunge, damp_plunge)


def plot_freq_damp(airspeeds, freq_pitch, damp_pitch, freq_plunge, damp_plunge, *, publish=False) -> None:
    fig, (ax_freq, ax_damp) = plt.subplots(2, 1, figsize=(5.5, 5), layout="constrained")
    if not(publish):
        fig.suptitle(("Half-power point method"))

    ax_freq.scatter(airspeeds, freq_pitch, marker="x", label="Pitch")
    ax_freq.scatter(airspeeds, freq_plunge, marker="+", label="Plunge")
    ax_freq.set_ylabel(r"$\omega_{\mathrm{n}}/\mathrm{Hz}$")
    ax_freq.legend()

    ax_damp.scatter(airspeeds, damp_pitch, marker="x", label="Pitch")
    ax_damp.scatter(airspeeds, damp_plunge, marker="+", label="Plunge")
    ax_damp.set_ylabel(r"$\zeta$")
    ax_damp.set_xlabel(r"$U_\infty/(\mathrm{m/s})$")

    fig.show()


if __name__ == '__main__':
    extracted_signals = ld.get_extracted_signals(ld.EXTRACT_BOUNDS)
    fft_signals = get_fft_signals(extracted_signals)
    hppm_signals = get_hppm_signals(fft_signals)
    plot_freq_damp(*extract_freq_damp(hppm_signals), publish=True)
