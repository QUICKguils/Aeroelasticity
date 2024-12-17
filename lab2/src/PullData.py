import pandas as pd
import numpy as np
import FRF as frf
import scipy.io
import os
import re
import matplotlib.pyplot as plt

def data_pull_airspeed(prefix, number_data, directory='../data/group3'):
    airspeed_data = {}
    
    for i in range(number_data ): 
        file_path = os.path.join(directory, f"{prefix}{i}.dat")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        airspeed_line = lines[0].strip()
        match = re.match(r"Airspeed (\d+(\.\d+)?)", airspeed_line)
        if match:
            airspeed = float(match.group(1))
        else:
            raise ValueError(f"Invalid airspeed format in file: {file_path}")
        
        y_values, w_values = [], []
        for line in lines[1:]:
            try:
                y, w = map(float, line.strip().split())
                y_values.append(y)
                w_values.append(w)
            except ValueError:
                continue  

        airspeed_data[airspeed] = {'y': np.array(y_values), 'w': np.array(w_values)}
    
    return airspeed_data    

def data_pull_gr13_0(data, acquisition_frequency) : 
    """
    At 0 airspeed a testing hammer is made to ecquite all the structure to see where is the peak
    """
    y = data[0.0]["y"]  # Extraction des données
    t = np.linspace(0, len(y)/acquisition_frequency, len(y))
    idx_first_shock  = np.where((t > 3) & (t < 6))[0]
    idx_second_shock = np.where((t > 10.3) & (t < 16))[0]
    idx_third_shock  = np.where((t > 20) & (t < 23))[0]

    time_first_shock  = np.linspace(0, t[idx_first_shock][-1] - t[idx_first_shock][0], len(idx_first_shock))
    time_second_shock = np.linspace(0, t[idx_second_shock][-1] - t[idx_second_shock][0], len(idx_second_shock))
    time_third_shock  = np.linspace(0, t[idx_third_shock][-1] - t[idx_third_shock][0], len(idx_third_shock))
    y_first_shock     = y[idx_first_shock]
    y_second_shock    = y[idx_second_shock]
    y_third_shock     = y[idx_third_shock]
    return {"First shock": (time_first_shock, y_first_shock), "Second shock": (time_second_shock, y_second_shock), "Third shock": (time_third_shock, y_third_shock)}

def data_pull_common1_0(data, acquisition_frequency):
    y = data[0]["y"]
    t = np.linspace(0, len(y)/acquisition_frequency, len(y))
    idx_first_shock  = np.where((t > 8.83) & (t < 14))[0]
    time_first_shock = np.linspace(0, t[idx_first_shock][-1] - t[idx_first_shock][0], len(idx_first_shock))
    y_first_shock    = y[idx_first_shock]
    return {"First shock": (time_first_shock, y_first_shock)}

def data_pull_common2_0(data, acquisition_frequency):
    y = data[0]["y"]
    t = np.linspace(0, len(y)/acquisition_frequency, len(y))
    
    idx_first_shock  = np.where((t > 7.3) & (t < 8.5))[0]
    time_first_shock = np.linspace(0, t[idx_first_shock][-1] - t[idx_first_shock][0], len(idx_first_shock))
    y_first_shock    = y[idx_first_shock]
    
    idx_second_shock  = np.where((t > 12.9) & (t < 15))[0]
    time_second_shock = np.linspace(0, t[idx_second_shock][-1] - t[idx_second_shock][0], len(idx_second_shock))
    y_second_shock    = y[idx_second_shock]

    idx_third_shock  = np.where((t > 18.8) & (t < 21))[0]
    time_third_shock  = np.linspace(0, t[idx_third_shock][-1] - t[idx_third_shock][0], len(idx_third_shock))
    y_third_shock     = y[idx_third_shock]

    return {"First shock": (time_first_shock, y_first_shock), "Second shock": (time_second_shock, y_second_shock), "Third shock": (time_third_shock, y_third_shock)}

def data_pull_common3_0(data, acquisition_frequency):
    
    y = data[0]["y"]
    t = np.linspace(0, len(y)/acquisition_frequency, len(y))
    
    idx_first_shock  = np.where((t > 14.28) & (t < 18))[0]
    time_first_shock = np.linspace(0, t[idx_first_shock][-1] - t[idx_first_shock][0], len(idx_first_shock))
    y_first_shock    = y[idx_first_shock]
    
    idx_second_shock  = np.where((t > 22.59) & (t < 25))[0]
    time_second_shock = np.linspace(0, t[idx_second_shock][-1] - t[idx_second_shock][0], len(idx_second_shock))
    y_second_shock    = y[idx_second_shock]

    return {"First shock": (time_first_shock, y_first_shock), "Second shock": (time_second_shock, y_second_shock)}




def extract_max_amplitude_displacement(data) :
    keys = list(data.keys())[1:] # pas prendre le 0
    A = np.zeros(len(keys))
    for i, U in enumerate(keys):
        y = data[U]["y"]
        max_arg = np.argmax(y)
        A[i] = y[max_arg]
    return A

def extract_max_amplitude_speed_wake(data) :
    keys = list(data.keys())[1:] # pas prendre le 0
    A = np.zeros(len(keys))
    for i, U in enumerate(keys):
        w = data[U]["w"]
        max_arg = np.argmax(w)
        A[i] = w[max_arg]
    return A
def extract_frequency_wake(data, acquisition_frequency) :
    """
    Extract frequency of the wake in this case the fct is just use an argmax, like work in this data
    """
    keys = list(data.keys())[1:]
    w = np.zeros(len(keys))
    for i, U in enumerate(keys):
        speed_wake = data[U]["w"]
        t = np.linspace(0, len(speed_wake)/acquisition_frequency, len(speed_wake))
        w_mag, w_freq = frf.compute_FRF(t, speed_wake)
        idx = np.argmax(w_mag)
        w[i] = w_freq[idx]
    return w

def extract_RMS(data, acquisition_frequency) :
    keys = list(data.keys())[1:]
    y_rms = np.zeros(len(keys))
    for i, U in enumerate(keys):
        y = data[U]["y"]
        y_sum = np.sum(y**2)
        y_rms[i] = np.sqrt( (1/len(y)) * y_sum) 
    return y_rms





