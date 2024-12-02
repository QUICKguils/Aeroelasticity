import PullData as pd


cylinder_diameter           = 125 # [mm]
stifness_flexion_horizontal = 40800 # N/m
acquisition_frequency       = 1000 # [Hz]
airspeed_data = pd.data_pull_airspeed('gr3_', 12)
print(airspeed_data[0.0]["w"].shape)