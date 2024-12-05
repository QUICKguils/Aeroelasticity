import PullData as pd
import FRF as frf
import VizData as vd
import numpy as np
import matplotlib.pyplot as plt


cylinder_diameter           = 125   # [mm]
stifness_flexion_horizontal = 40800 # [N/m]
acquisition_frequency       = 1000  # [Hz]


airspeed_data = pd.data_pull_airspeed('gr3_', 12)
data_0 = pd.data_pull_0(airspeed_data, acquisition_frequency)

magnitudes_1_shock, frequencies_1_shock = frf.compute_FRF(data_0["First shock"][0], data_0["First shock"][1])
magnitudes_2_shock, frequencies_2_shock = frf.compute_FRF(data_0["Second shock"][0], data_0["Second shock"][1])
magnitudes_3_shock, frequencies_3_shock = frf.compute_FRF(data_0["Third shock"][0], data_0["Third shock"][1])
vd.viz_FRF_0(magnitudes_1_shock, frequencies_1_shock, shock=1)
vd.viz_FRF_0(magnitudes_2_shock, frequencies_2_shock, shock=2)
vd.viz_FRF_0(magnitudes_3_shock, frequencies_3_shock, shock=3)

