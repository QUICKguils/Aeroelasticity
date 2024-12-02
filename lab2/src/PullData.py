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