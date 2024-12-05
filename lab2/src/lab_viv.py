# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:26:12 2024

@author: client
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

cylinder_diameter           = 125e-3 # [m]
stifness_flexion_horizontal = 40800 # N/m

data_list = []

# Loop charge of .dat files
for i in range(13):  
    file_name = f'../data/group3/gr3_{i}.dat'  
    data = pd.read_csv(file_name, delim_whitespace=True, header=None)
    if 'Airspeed' in data.iloc[0, 0]:
        # Supprimer la première ligne
        data = data.iloc[1:].reset_index(drop=True)
    data_list.append(data)

'''
# Verification
for i, data in enumerate(data_list):
    print(f"Data {i}:")
    print(data)
'''
    

# Données
airspeed = [0.0, 6.0, 9.2, 10.7, 11.9, 13.4, 14.2, 14.9, 16.2, 16.6, 18.8, 21.0, 23.9]
acq_freq = 1000 # [Hz]
 

def time_data(airspeed, acq_freq, data_list):
    #data_list est une liste de 13 element où chaque element est une matrice de n_lignes * 2 colonnes
    T = 1 / acq_freq  # period of sampling
    airspeed_len = len(airspeed) # The number of U_inf
    
    nb_points = np.zeros((airspeed_len)) #La liste reprenanat nombre de points de chaque vitesse
    total_time = np.zeros((len(nb_points))) #Le temps total de mesure de data de chaque vitesse
    
    for i in range(airspeed_len):
        nb_points[i] = int(len(data_list[i][0])) #Pour chaque vitesse, j'associe le nombre de points mesurés
        total_time[i] = nb_points[i]/acq_freq # in [s], pareil ici mais en temps
    
    discr_time = []
    for i in range(airspeed_len): #Je discretise le temps pour chaque U_inf
        time_vector = np.linspace(0, int((nb_points[i]-1)*T), int(nb_points[i]))
        print(len(time_vector))
        discr_time.append(time_vector)
        
    
    for i in range(airspeed_len): #Ici je veux plot
        data = np.array(data_list[i][0]) # J'extrait les données y de la i-ème vitesse U_inf
        float_data = [float(item) for item in data] #Je transforme les données en float
        sampled_time = discr_time[i][::10] #Pour facilement tracer, je prends tous les 10 elements
        sampled_data = float_data[::10]  # Pareil ici, un point sur 10
        print(i)
        plt.plot(sampled_time, sampled_data, label=f"U = {airspeed[i]} m/s")
        plt.xlabel("Time (s)")
        plt.ylabel("y-displacements")
        plt.title("y-displacement wrt to time of simulation")
        plt.legend()
        plt.grid(True)
        plt.show()
        
    
        # FFT computation
        fft_result = np.fft.fft(data)  # FFT des données originales (pas sous-échantillonnées i-e on ne prend pas tous les 10 elements)
        fft_amplitude = np.abs(fft_result)  # Amplitude (modulus)
        fft_frequencies = np.fft.fftfreq(len(data), d=T)  # Associate frequencies

        # I take only positve frequencies
        positive_freqs = fft_frequencies[:len(fft_frequencies) // 2]
        positive_amplitude = fft_amplitude[:len(fft_amplitude) // 2]
        
        # Identifier la fréquence du plus haut pic
        peak_index = np.argmax(positive_amplitude)
        peak_frequency = positive_freqs[peak_index]
        peak_amplitude = positive_amplitude[peak_index]

        # Display du pic de fréquence
        print(f"Peak frequency for U = {airspeed[i]} m/s is {peak_frequency:.2f} Hz with amplitude {peak_amplitude:.2f}")

        # Frequency spectrum drawing
        plt.figure(figsize=(10, 5))
        plt.plot(fft_frequencies[:len(fft_frequencies) // 2],  # Positve frequencies
                 fft_amplitude[:len(fft_amplitude) // 2],  # Positive amplitudes
                 label=f"U = {airspeed[i]} m/s")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude")
        plt.title(f"Frequency Spectrum for U = {airspeed[i]} m/s")
        plt.legend()
        plt.grid(True)
        plt.show()

    return nb_points, total_time, discr_time

nb, tot, discr_time = time_data(airspeed, acq_freq, data_list)
print(nb, tot, discr_time)
    
    
    
    
           








   
'''
U_r = np.zeros((len(airspeed)))
for i in range(len(airspeed)):
    U_r[i] = airspeed[i]/(acquisition_frequency*cylinder_diameter) #Je ne sais pas si c'est la bonne frequence !!!
   
# data_list[i] show the i-ieme data files of our group
# data_list[i][0] shows the composant y of the velocity of the i-ieme data files
# data_list[i][1] shows the composant w of the velocity of the i-ieme data files

"""Extraction of the rms amplitude"""
y_rms = np.zeros((len(airspeed)))
for i in range(len(airspeed)):
    y_sum = 0
    for j in range(len(data_list[i][0])):
        y_sum +=  float(data_list[i][0][j]) * float(data_list[i][0][j])  
    y_rms[i] = np.sqrt( (1/len(data_list[i][0])) * y_sum)  * 1e3   # I multiply by 1e3 to better interprete values          

"""Extraction of the maximum amplitude"""
y_max = np.zeros((len(airspeed)))
for i in range(len(airspeed)):
    data_list[i][0] = [float(chaine) for chaine in data_list[i][0]] #cast string in float
    max_ = max(data_list[i][0])
    min_ = min(data_list[i][0])
    print(max_, min_)
    if (abs(max_) > abs(min_)): 
        y_max[i] = max_*1e3
    else : 
        y_max[i] = min_*1e3


plt.figure(figsize=(8, 6))    
plt.xlabel("Reduced velocity U_r [m/s]")
plt.ylabel("Maximum displacement [mm]")
plt.scatter(U_r, y_max, label="Data", color="blue")  # Points de données
plt.plot(U_r, y_max, marker = 'o', linestyle = '-', color = 'b', linewidth = 0.5)
plt.grid(True)  
plt.legend()
plt.savefig("maximum_displacement.pdf", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(8, 6))    
plt.xlabel("Reduced velocity U_r [m/s]")
plt.ylabel("RMS displacement [mm]")
plt.scatter(U_r, y_rms, label="Data", color="blue")  # Points de données
plt.plot(U_r, y_rms, marker = 'o', linestyle = '-', color = 'b', linewidth = 0.5)
plt.grid(True)  
plt.legend()
plt.savefig("rms_displacement.pdf", dpi=300, bbox_inches="tight")
plt.show()

"""Next VIVI speed"""
Strouhal = 0.2
frequency = 22 # [Hz]
U = (2e3 * cylinder_diameter)/Strouhal
U_r_next = U/(frequency*cylinder_diameter) #Ici je dois herhcher la bonne frequence
'''




