import PullData as pd
import FRF as frf
import VizData as vd
import numpy as np
import matplotlib.pyplot as plt
import dimensionless_conversion as dc
import SDOF_method as sm


cylinder_diameter           = 125   # [mm]
stifness_flexion_horizontal = 40800 # [N/m]
acquisition_frequency       = 1000  # [Hz]


data_gr13 = pd.data_pull_airspeed('gr3_', 13)
airspeed_lab  = np.array(list(data_gr13.keys())[1:])
data_gr_0        = pd.data_pull_gr13_0(data_gr13, acquisition_frequency)
for i in (data_gr_0.keys()):
    magnitudes, frequencies = frf.compute_FRF(data_gr_0[i][0], data_gr_0[i][1], max_freq=40)
    vd.viz_FRF_0(magnitudes, frequencies, path = f"../figures/gr3/FRF_0_{i}.pdf")
magnitudes, frequencies = frf.compute_FRF(data_gr_0["First shock"][0], data_gr_0["First shock"][1], max_freq=40)
damping_gr_3 = sm.compute_peak_picking_method(magnitudes, frequencies, plot=True, path="../figures/gr3")

# for i in airspeed_lab:
#     t = np.linspace(0, len(data_gr13[i]["y"])/acquisition_frequency, len(data_gr13[i]["y"]))
#     magnitudes, frequencies = frf.compute_FRF(t, data_gr13[i]["y"])
#     plt.figure()
#     plt.plot(frequencies, magnitudes)
#     plt.title(f"FRF for airspeed {i}")
#     plt.xlabel("Frequency [Hz]")
#     plt.ylabel("Magnitude [dB]")
#     plt.show()


data_common1 = pd.data_pull_airspeed('common1_', 10, directory='../data/common1')
airspeed_comon1 = np.array(list(data_common1.keys())[1:])
data_com1_0 = pd.data_pull_common1_0(data_common1, acquisition_frequency)
nbr_shock = 1
for i in (data_com1_0.keys()):
    magnitudes, frequencies = frf.compute_FRF(data_com1_0[i][0], data_com1_0[i][1], max_freq=40)
    vd.viz_FRF_0(magnitudes, frequencies, path = f"../figures/common1/FRF_0_{nbr_shock}.pdf")
    nbr_shock += 1
magnitudes, frequencies = frf.compute_FRF(data_com1_0["First shock"][0], data_com1_0["First shock"][1])
damping_common_1        = sm.compute_peak_picking_method(magnitudes, frequencies, plot=True, path="../figures/common1")


data_common2 = pd.data_pull_airspeed('common2_', 13, directory='../data/common2')
airspeed_comon2 = np.array(list(data_common2.keys())[1:])
data_com2_0 = pd.data_pull_common2_0(data_common2, acquisition_frequency)
nbr_shock = 1
for i in (data_com2_0.keys()):
    magnitudes, frequencies = frf.compute_FRF(data_com2_0[i][0], data_com2_0[i][1], max_freq=40)
    vd.viz_FRF_0(magnitudes, frequencies, path = f"../figures/common2/FRF_0_{nbr_shock}.pdf")
    nbr_shock += 1
magnitudes, frequencies = frf.compute_FRF(data_com2_0["Third shock"][0], data_com2_0["Third shock"][1])
damping_common_2 = sm.compute_peak_picking_method(magnitudes, frequencies, plot=True, path="../figures/common2")


data_common3    = pd.data_pull_airspeed('common3_', 13, directory='../data/common3')
airspeed_comon3 = np.array(list(data_common3.keys()))[1:]
data_com3_0     = pd.data_pull_common3_0(data_common3, acquisition_frequency)
nbr_shock       = 1
for i in (data_com3_0.keys()):
    magnitudes, frequencies = frf.compute_FRF(data_com3_0[i][0], data_com3_0[i][1])
    vd.viz_FRF_0(magnitudes, frequencies, path = f"../figures/common3/FRF_0_{nbr_shock}.pdf")
    nbr_shock += 1
magnitudes, frequencies = frf.compute_FRF(data_com3_0["Second shock"][0], data_com3_0["Second shock"][1])
damping_common_3 = sm.compute_peak_picking_method(magnitudes, frequencies, plot=True, path="../figures/common3")

print("##############################################")
print("###############  Damping  ####################")
print("##############################################")


print(f"Common 1: {damping_common_1*100} [%]")
print(f"Common 2: {damping_common_2*100} [%]")
print(f"Common 3: {damping_common_3*100} [%]")
print(f"Group 3 : {damping_gr_3*100} [%]")  


freq_structural   = 22
freq_damp1        = 22
freq_damp2        = 23
freq_damp3        = 21.5
# question 2 calculate the mass  POTENTILLMENT AJOUTER LE DAMPING AVEC LA PEAK PICKING METHOD
mass_total     = stifness_flexion_horizontal/(2 * np.pi * freq_structural)**2

print(f"Mass total    : {mass_total} [kg] ")



# question 3
reduced_velocity   = dc.compute_reduced_velocity(airspeed_lab,cylinder_diameter * 1e-3, freq_structural)
rms_displacement   = pd.extract_RMS(data_gr13, acquisition_frequency)
max_amp            = pd.extract_max_amplitude_displacement(data_gr13)
vd.viz_RMS_reduced_velocity(reduced_velocity, rms_displacement)
vd.viz_amplitudeDisp_reduced_velocity(reduced_velocity, max_amp)



# question 4
mode_wake          = pd.extract_frequency_wake(data_gr13, acquisition_frequency)
max_amp_wake       = pd.extract_max_amplitude_speed_wake(data_gr13)
freq_structure_speed = [10.12, 13.79, 18.04, 20.4, 21.88, 21.76, 21.82, 22.35, 22.41, 22.35, 21.82, 34]
vd.viz_freqWake_reduced_velocity(reduced_velocity, mode_wake, freq_structural, freq_structure_speed, strual_number=0.2)


# question 5
vd.viz_freqWake_reduced_velocity_with_strual(reduced_velocity, mode_wake, freq_structural, freq_structure_speed, strual_number=0.2)

# question 6 Damping different 
mode_wake_common1 = pd.extract_frequency_wake(data_common1, acquisition_frequency)
reduced_velocity_common1 = dc.compute_reduced_velocity(airspeed_comon1,cylinder_diameter * 1e-3, freq_damp1)
max_amp_common1 = pd.extract_max_amplitude_displacement(data_common1)


mode_wake_common2 = pd.extract_frequency_wake(data_common2, acquisition_frequency)
reduced_velocity_common2 = dc.compute_reduced_velocity(airspeed_comon2,cylinder_diameter * 1e-3, freq_damp2)
max_amp_common2 = pd.extract_max_amplitude_displacement(data_common2)


mode_wake_common3 = pd.extract_frequency_wake(data_common3, acquisition_frequency)
reduced_velocity_common3 = dc.compute_reduced_velocity(airspeed_comon3,cylinder_diameter * 1e-3, freq_damp3)
max_amp_common3 = pd.extract_max_amplitude_displacement(data_common3)


different_damp = {"Damp2" : {"reduce_velocity" : reduced_velocity_common2, "mode_wake" : mode_wake_common2, "damp" : damping_common_2, "amplitude" : max_amp_common2},
                  "Damp3" : {"reduce_velocity" : reduced_velocity_common3, "mode_wake" : mode_wake_common3, "damp": damping_common_3, "amplitude" : max_amp_common3}}

vd.viz_freqWake_reduced_velocity_damping(different_damp)
vd.viz_freqWake_reduced_velocity_amplitude(different_damp)


# Addimentionalise parameters
vd.viz_freqWake_reduced_velocity_with_strual(reduced_velocity, mode_wake, freq_structural, freq_structure_speed, strual_number=0.2, adimentionalise=True)
vd.viz_amplitudeDisp_reduced_velocity(reduced_velocity, max_amp, diametre_cylindre=cylinder_diameter*1e-3)









