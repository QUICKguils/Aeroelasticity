"""Utilities for manipulating the lab data."""

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
