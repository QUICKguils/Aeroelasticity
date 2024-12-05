import pandas as pd
import numpy as np
import scipy.io
import os
import re

def data_pull_airspeed(prefix, number_data, directory='../data/group3'):
    airspeed_data = {}
    
    for i in range(number_data + 1): 
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

def data_pull_0(data, acquisition_frequency) : 
    """
    At 0 airspeed a testing hammer is made to ecquite all the structure to see where is the peak
    """
    w = data[0.0]["y"]  # Extraction des données
    t = np.linspace(0, len(w)/acquisition_frequency, len(w))
    idx_first_shock  = np.where((t > 3) & (t < 6))[0]
    idx_second_shock = np.where((t > 10.3) & (t < 16))[0]
    idx_third_shock  = np.where((t > 20) & (t < 23))[0]

    time_first_shock  = np.linspace(0, t[idx_first_shock][-1] - t[idx_first_shock][0], len(idx_first_shock))
    time_second_shock = np.linspace(0, t[idx_second_shock][-1] - t[idx_second_shock][0], len(idx_second_shock))
    time_third_shock  = np.linspace(0, t[idx_third_shock][-1] - t[idx_third_shock][0], len(idx_third_shock))
    w_first_shock     = w[idx_first_shock]
    w_second_shock    = w[idx_second_shock]
    w_third_shock     = w[idx_third_shock]
    return {"First shock": (time_first_shock, w_first_shock), "Second shock": (time_second_shock, w_second_shock), "Third shock": (time_third_shock, w_third_shock)}
