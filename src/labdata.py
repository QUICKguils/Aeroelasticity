"""Utilities for manipulating the lab data."""

from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt
from scipy import io

# plt.rcParams['text.usetex'] = True
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
# plt.rcParams['figure.figsize'] = (6.34, 3.34)
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 200

LAB_DATA = io.loadmat(r"res\DATAG2_v7")["exp_data"][0]
SAMPLING_FREQ_HZ = 201.03
SAMPLING_TSTEP = 1/SAMPLING_FREQ_HZ


def get_run(id):
    """Extract lab data for the desired airspeed run."""
    run = LAB_DATA[id]
    pitch = run[0].flatten()
    plunge = run[1].flatten()
    airspeed = run[2].flatten()[0]
    n_sample = plunge.size

    return (pitch, plunge, airspeed, n_sample)


def plot_raw_acceleration(id):
    """Plot the raw accelerometer data for the desired airspeed run."""
    (pitch, plunge, airspeed, _) = get_run(id)

    fig = plt.figure()
    fig.supxlabel("Array index")
    fig.supylabel("Acceleration (m/s²)")
    gs = fig.add_gridspec(2, 1, hspace=0.3)
    (ax_pitch, ax_plunge) = gs.subplots()

    ax_pitch.plot(pitch)
    ax_pitch.set_title("Pitch")
    ax_plunge.plot(plunge)
    ax_plunge.set_title("Plunge")

    fig.show()


def plot_time_acceleration(id):
    """Plot the time vs accelerations for the desired airspeed run."""
    (pitch, plunge, airspeed, n_sample) = get_run(id)
    t_sample = np.linspace(0, n_sample*SAMPLING_TSTEP, n_sample)

    fig = plt.figure()
    fig.suptitle(f"Response to an external impulsion ($U_\\infty$ = {airspeed} m/s)")
    fig.supxlabel("Time (s)")
    fig.supylabel("Acceleration (m/s²)")
    gs = fig.add_gridspec(2, 1, hspace=0.3)
    (ax_pitch, ax_plunge) = gs.subplots()

    ax_pitch.plot(t_sample, pitch)
    ax_pitch.set_title("Pitch")
    ax_plunge.plot(t_sample, plunge)
    ax_plunge.set_title("Plunge")

    fig.show()


class ExtractedSignal(NamedTuple):
    pitch: np.ndarray
    plunge: np.ndarray
    t_sample: np.ndarray


# Manully identify the relevant portions of the acceleration signals.
# This array gives the lower and upper indexes of three of these portions,
# for each run/airspeed.
EXTRACT_BOUNDS = np.array([
    [[1650,  2000],  [2975,  3300],  [4185,  4500]],
    [[3523,  3900],  [4828,  4900],  [5633,  5900]],
    [[3737,  4000],  [4717,  5000],  [5538,  5800]],
    [[3322,  3600],  [4050,  4300],  [4687,  5000]],
    [[4457,  4800],  [6143,  6500],  [8239,  8600]],
    [[11200, 11700], [13640, 14100], [14370, 14500]],
    [[2600,  4800],  [5394,  7000],  [7667,  9250]],
    [[3000,  3600],  [3000,  3600],  [3000,  3600]],
])


def extract_accelerations(extract_bounds):
    """Extract relevant signal portions, based on manual identification."""
    extracted_signals = np.zeros(
        (extract_bounds.shape[0], extract_bounds.shape[1]),
        dtype=ExtractedSignal
    )

    for id_run, bounds in enumerate(extract_bounds):
        (pitch, plunge, airspeed, _) = ld.get_run(id_run)

        for id_bound, bound in enumerate(bounds):
            ti = bound[0]*ld.SAMPLING_TSTEP
            tf = bound[1]*ld.SAMPLING_TSTEP
            n_sample = np.abs(bound[1] - bound[0]) + 1
            t_portion = np.linspace(ti, tf, n_sample)
            pitch_portion = pitch[bound[0]:bound[1]+1]
            plunge_portion = plunge[bound[0]:bound[1]+1]
            extracted_signals[id_run][id_bound] = ExtractedSignal(pitch_portion, plunge_portion, t_portion)

    return extracted_signals
