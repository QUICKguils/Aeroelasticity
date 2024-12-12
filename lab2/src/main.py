import PullData as pd
import FRF as frf
import VizData as vd
import numpy as np
import matplotlib.pyplot as plt
import dimensionless_conversion as dc


cylinder_diameter           = 125   # [mm]
stifness_flexion_horizontal = 40800 # [N/m]
acquisition_frequency       = 1000  # [Hz]


airspeed_data = pd.data_pull_airspeed('gr3_', 12)
airspeed_lab  = np.array(list(airspeed_data.keys())[1:])
data_0 = pd.data_pull_0(airspeed_data, acquisition_frequency)

# Doing the FRF for the first shock (First question)
magnitudes_1_shock, frequencies_1_shock = frf.compute_FRF(data_0["First shock"][0], data_0["First shock"][1])
magnitudes_2_shock, frequencies_2_shock = frf.compute_FRF(data_0["Second shock"][0], data_0["Second shock"][1])
magnitudes_3_shock, frequencies_3_shock = frf.compute_FRF(data_0["Third shock"][0], data_0["Third shock"][1])
vd.viz_FRF_0(magnitudes_1_shock, frequencies_1_shock, shock=1)
vd.viz_FRF_0(magnitudes_2_shock, frequencies_2_shock, shock=2)
vd.viz_FRF_0(magnitudes_3_shock, frequencies_3_shock, shock=3)

freq_structural   = 22
# question 2 calculate the mass  POTENTILLMENT AJOUTER LE DAMPING AVEC LA PEAK PICKING METHOD
mass_total     = stifness_flexion_horizontal/(2 * np.pi *freq_structural)**2
rho            = 1.225 # considere at sea level
mass_add_flow  = rho * np.pi * (cylinder_diameter * 1e-3)**2 / 4
mass_structure = mass_total - mass_add_flow
mass_ratio     = dc.compute_mass_ratio(mass_structure, mass_add_flow)
print(f"Mass structure: {mass_structure} kg")
print(f"Mass fluid    : {mass_add_flow} kg")
print(f"Mass total    : {mass_total} kg ")
print(f"Mass ratio    : {mass_ratio} kg")


# question 3
reduced_velocity   = dc.compute_reduced_velocity(airspeed_lab,cylinder_diameter * 1e-3, freq_structural)
rms_displacement   = pd.extract_RMS(airspeed_data, acquisition_frequency)
max_amp            = pd.extract_max_amplitude_displacement(airspeed_data)
vd.viz_RMS_reduced_velocity(reduced_velocity, rms_displacement)
vd.viz_amplitudeDisp_reduced_velocity(reduced_velocity, max_amp)



# question 4
mode_wake          = pd.extract_frequency_wake(airspeed_data, acquisition_frequency)
vd.viz_freqWake_reduced_velocity(reduced_velocity, mode_wake, freq_structural)

# question 5
vd.viz_freqWake_reduced_velocity_with_strual(reduced_velocity, mode_wake, freq_structural, strual_number=0.2)




