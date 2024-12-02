"""Utilities for manipulating the lab data."""

import pathlib
from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from scipy import io

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150

ROOT_DIR = pathlib.Path(__file__).parent.parent
FPATH_DATA = ROOT_DIR / "res" / "DATAG2_v7"
DATA = io.loadmat(str(FPATH_DATA))["exp_data"][0]

SAMPLING_FREQ_HZ = 201.03
SAMPLING_TSTEP = 1/SAMPLING_FREQ_HZ


def get_run(id_run):
    """Extract lab data for the desired airspeed run."""
    run = DATA[id_run]
    pitch = run[0].flatten()
    plunge = run[1].flatten()
    airspeed = run[2].flatten()[0]
    n_sample = plunge.size

    return (pitch, plunge, airspeed, n_sample)


def plot_raw_acceleration(id_run, *, publish=False) -> None:
    """Plot the raw accelerometer data for the desired airspeed run."""
    (pitch, plunge, airspeed, _) = get_run(id_run)

    fig, (ax_pitch, ax_plunge) = plt.subplots(2, 1, figsize=(5.5, 3.5), layout="constrained")
    if not(publish):
        fig.suptitle(f"Response to an external impulsion ($U_\\infty$ = {airspeed} m/s)")

    ax_pitch.plot(pitch, linewidth=0.5)
    ax_pitch.set_ylabel(r"$\ddot{\alpha}$/(rad/s²)")

    ax_plunge.plot(plunge, linewidth=0.5)
    ax_plunge.set_ylabel(r"$\ddot{h}$/(m/s²)")
    ax_plunge.set_xlabel("Sample index")

    fig.show()


def plot_time_acceleration(id_run, *, publish=False) -> None:
    """Plot the time vs accelerations for the desired airspeed run."""
    (pitch, plunge, airspeed, n_sample) = get_run(id_run)
    t_sample = np.linspace(0, n_sample*SAMPLING_TSTEP, n_sample)

    fig, (ax_pitch, ax_plunge) = plt.subplots(2, 1, figsize=(5.5, 3.5), layout="constrained")
    if not(publish):
        fig.suptitle(f"Response to an external impulsion ($U_\\infty$ = {airspeed} m/s)")

    ax_pitch.plot(t_sample, pitch, linewidth=0.5)
    ax_pitch.set_ylabel(r"$\ddot{\alpha}$/(rad/s²)")

    ax_plunge.plot(t_sample, plunge, linewidth=0.5)
    ax_plunge.set_ylabel(r"$\ddot{h}$/(m/s²)")
    ax_plunge.set_xlabel("Record time (s)")

    fig.show()


class ExtractedSignal(NamedTuple):
    """Represent a signal extracted from the lab data."""
    id: int             # Label of the signal, in its run
    id_run: int         # Label of the run
    airspeed: float     # Airspeed of the run
    pitch: np.ndarray   # pitch data
    plunge: np.ndarray  # plunge data
    var: np.ndarray     # Abscissa of the pitch and plunge signals


# Manully identify the relevant portions of the acceleration signals.
# This array gives the lower and upper indexes of three of these portions,
# for each run/airspeed.
EXTRACT_BOUNDS = np.array([
    [[1650,  2000],  [2975,  3300],  [4185,  4500]],
    [[3523,  3900],  [4626,  4850],  [5633,  5900]],
    [[3737,  4000],  [4717,  5000],  [5538,  5800]],
    [[3322,  3600],  [4050,  4300],  [4687,  5000]],
    [[4457,  4800],  [6143,  6500],  [8239,  8600]],
    [[11200, 11700], [13640, 14100], [14370, 14974]],
    [[2600,  4800],  [5394,  7000],  [7667,  9396]],
    [[3000,  3600],  [3000,  3600],  [3000,  3600]],
])


def get_extracted_signals(extract_bounds):
    """Extract relevant signal portions, based on manual identification."""
    extracted_signals = np.zeros(extract_bounds.shape[:2], dtype=ExtractedSignal)

    for i_run, bounds in enumerate(extract_bounds):
        (pitch, plunge, airspeed, _) = get_run(i_run)

        for i_bound, bound in enumerate(bounds):
            ti = bound[0]*SAMPLING_TSTEP
            tf = bound[1]*SAMPLING_TSTEP
            n_sample = np.abs(bound[1] - bound[0]) + 1
            t_portion = np.linspace(ti, tf, n_sample)
            pitch_portion = pitch[bound[0]:bound[1]+1]
            plunge_portion = plunge[bound[0]:bound[1]+1]
            extracted_signals[i_run][i_bound] = ExtractedSignal(
                id       = i_bound,
                id_run   = i_run,
                airspeed = airspeed,
                pitch    = pitch_portion,
                plunge   = plunge_portion,
                var      = t_portion
            )

    return extracted_signals


def plot_extracted_signals(signal: ExtractedSignal, *, publish=False) -> None:
    """Plot an extracted signal as a function of its record time."""
    fig, (ax_pitch, ax_plunge) = plt.subplots(2, 1, figsize=(5.5, 5.5), layout="constrained")
    if not(publish):
        fig.suptitle((
            "Extracted signals "
            f"(run: {signal.id_run}, "
            f"-- airspeed: {signal.airspeed} m/s)"
        ))

    ax_pitch.plot(signal.var, signal.pitch)
    ax_pitch.set_ylabel(r"$\ddot{\alpha}$/(rad/s²)")

    ax_plunge.plot(signal.var, signal.plunge)
    ax_plunge.set_ylabel(r"$\ddot{h}$/(m/s²)")
    ax_plunge.set_xlabel("Record time (s)")

    plt.show()


def _check_extracted_signals() -> None:
    """Plot the extracted signals for each run, to check their validity."""
    for signal_run in get_extracted_signals(EXTRACT_BOUNDS):
        fig, (ax_pitch, ax_plunge) = plt.subplots(2, 1, figsize=(5.5, 3.5), layout="constrained")
        fig.suptitle((
            "Extracted signals "
            f"(run: {signal_run[0].id_run}, "
            f"-- airspeed: {signal_run[0].airspeed} m/s)"
        ))
        ax_pitch.set_ylabel(r"$\ddot{\alpha}$/(rad/s²)")
        ax_plunge.set_ylabel(r"$\ddot{h}$/(m/s²)")
        ax_plunge.set_xlabel("Sample index")

        for signal in signal_run:
            ax_pitch.plot(signal.var, signal.pitch)
            ax_plunge.plot(signal.var, signal.plunge)

        plt.show()
