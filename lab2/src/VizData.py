import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150

def viz_FRF_0(amplitude, frequency, shock=1):
    plt.figure(figsize=(10, 4))
    plt.plot(frequency, amplitude)
    plt.xlabel(r"Fréquence [Hz]")
    plt.ylabel(r"Magnitude [m]")
    file_name = f"../figures/FRF_0_{shock}.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    plt.close() 
