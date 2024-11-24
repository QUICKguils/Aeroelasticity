"""Flutter identification of the half power point method."""

from typing import NamedTuple

import numpy as np
import matplotlib.pyplot as plt

import labdata as ld


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

