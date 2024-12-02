# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:23:09 2024

@author: client
"""

import numpy as np
from matplotlib import pyplot as plt

#Value of airspeed, frequency and damping are exctracted from the part which Guilain did, he sent me the array 
#directly
airspeed = [ 0.,  6.4,  9.6, 12.1, 14.8, 16.4, 17.6, 18.8]

freq_pitch = [5.87315094, 3.9802236 , 3.95878739, 4.05638169, 3.96960046, 4.12022809, 4.21266915, 4.34840266]
damp_pitch = [0.1968341 , 0.35253705, 0.43572172, 0.2591396 , 0.18356842, 0.13735645, 0.04065066, 0.09792555]
        
freq_plunge = [3.84203642, 3.68240138, 3.72283668, 3.81620247, 3.96960046, 4.12022809, 4.21266915, 4.34840266]
damp_plunge = [0.21830033, 0.24961218, 0.23724552, 0.23669645, 0.17435217,0.14656658, 0.03197834, 0.10972819]

beta_pitch = np.zeros((len(airspeed)))
beta_plunge = np.zeros((len(airspeed)))
omega_pitch = np.zeros((len(airspeed)))
omega_plunge = np.zeros((len(airspeed)))
F = np.zeros((len(airspeed)))
for i in range(len(airspeed)):
    beta_pitch[i] = freq_pitch[i] * damp_pitch[i]
    omega_pitch[i] = freq_pitch[i] * (np.sqrt(1 - damp_pitch[i]**2))

    beta_plunge[i] = freq_plunge[i] * damp_plunge[i]
    omega_plunge[i] = freq_plunge[i] * (np.sqrt(1 - damp_plunge[i]**2))

    #F[i] = (((omega_pitch[i]**2 - omega_plunge[i]**2)/2) + ((beta_pitch[i]**2 - beta_plunge[i]**2)/2))**2 + 4*beta_pitch[i]*beta_plunge[i](((omega_pitch[i]**2 + omega_plunge[i]**2)/2) + 2*((beta_pitch[i]**2 + beta_plunge[i]**2)/2))**2 - (((beta_pitch[i] - beta_plunge[i])/(beta_pitch[i] + beta_plunge[i]))((omega_pitch[i]**2 - omega_plunge[i]**2)/2) + ((beta_pitch[i]**2 + beta_plunge[i]**2)/2)**2)**2
    
    F[i] = (
        (   
            ((omega_pitch[i]**2 - omega_plunge[i]**2) / 2)
            + ((beta_pitch[i]**2 - beta_plunge[i]**2) / 2)
        )**2
        + 4 * beta_pitch[i] * beta_plunge[i] 
            * (
                ((omega_pitch[i]**2 + omega_plunge[i]**2) / 2)
                + 2 * ((beta_pitch[i]**2 + beta_plunge[i]**2) / 2)
              )**2
        - (
            (((beta_pitch[i] - beta_plunge[i]) / (beta_pitch[i] + beta_plunge[i]))
             * ((omega_pitch[i]**2 - omega_plunge[i]**2) / 2)
             + ((beta_pitch[i]**2 + beta_plunge[i]**2) / 2)**2 )**2
          )
           )

rho = 1.225 #[kg/m^3]
dyn_press = np.zeros((len(airspeed)))
for i in range(len(airspeed)):
    dyn_press[i] = (rho * airspeed[i]**2)/2

"""With airspeed"""
plt.figure(figsize=(8, 6))    
plt.plot(airspeed, F, marker = 'o', linestyle = '-', color = 'b', linewidth = 0.5)
plt.xlabel("Airspeed [m/s]")
plt.ylabel("Flutter margin")
plt.axhline(y=0, color='brown', linestyle='--', label="Flutter boundary")
coefficients = np.polyfit(airspeed, F, 2)  # Régression quadratique (2 = degre)
trend = np.poly1d(coefficients)
x_trend = np.linspace(np.array(airspeed).min(), np.array(airspeed).max(), 500)  # Plus de points pour lisser la courbe
F_trend= trend(airspeed)
plt.scatter(airspeed, F, label="Data", color="blue")  # Points de données
plt.plot(airspeed, F_trend, label="Tendancy", color="green")  # Ligne de tendance
plt.plot(airspeed, F, marker = 'o', linestyle = '-', color = 'b', linewidth = 0.5)
plt.grid(True)  
plt.legend()
plt.savefig("Flutter_speed_airspeed.pdf", dpi=300, bbox_inches="tight")
plt.show()

"""With dynamic pressure"""
plt.figure(figsize=(8, 6))
plt.xlabel("Dynamic pressure [Pa]")
plt.ylabel("Flutter margin")
plt.axhline(y=0, color='brown', linestyle='--', label="Flutter boundary")
coefficients = np.polyfit(dyn_press, F, 1)  # Régression linéaire (1 = degré)
trend = np.poly1d(coefficients) 
F_trend= trend(dyn_press)
plt.scatter(dyn_press, F, label="Data", color="blue")  # Points de données
plt.plot(dyn_press, F_trend, label="Tendancy", color="green")  # Ligne de tendance
plt.plot(dyn_press, F, marker = 'o', linestyle = '-', color = 'b', linewidth = 0.5)
plt.grid(True)  
plt.legend()
plt.savefig("Flutter_speed_dyn_pressure.pdf", dpi=300, bbox_inches="tight")
plt.show()


















