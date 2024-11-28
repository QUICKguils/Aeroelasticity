from scipy.signal import hilbert
import numpy as np

def extract_envelope(data) : 
    analytic_signal = hilbert(data)
    amplitude_envelope = np.abs(analytic_signal)
    return amplitude_envelope

def criteria_stability(data, envelope) :
    time_centroid = (np.sum(envelope @ data['time'][:-1])) / np.sum(envelope)
    stability_criteria = 1/time_centroid - 2/data['time'][-1]

    return stability_criteria

def get_speed_stab(data) :
    speed_stab = {}
    for i in data.keys():
        pitch_stab_matrix  = []
        plunge_stab_matrix = []
        for j in data[i].keys():
            pitch_envelope  = extract_envelope(data[i][j]["pitch"])[:-1]
            stab_pitch      = criteria_stability(data[i][j], pitch_envelope)
            plunge_envelope = extract_envelope(data[i][j]["plunge"])[:-1]
            stab_plunge     = criteria_stability(data[i][j], plunge_envelope)
            pitch_stab_matrix.append(stab_pitch)
            plunge_stab_matrix.append(stab_pitch)
        speed_stab[i] = {"pitch": pitch_stab_matrix, "plunge": plunge_stab_matrix}
    return speed_stab