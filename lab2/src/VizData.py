import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 15
plt.rcParams['figure.dpi'] = 150

def viz_FRF_0(amplitude, frequency, shock=1):
    plt.figure(figsize=(10, 4))
    plt.plot(frequency, amplitude)
    plt.xlim(min(frequency), max(frequency))
    plt.ylim(min(amplitude), max(amplitude) + 0.05)
    plt.xticks([0, 10, 20, 22, 30, 40, 50])
    plt.xlabel(r"Frequency [Hz]", fontsize=17)
    plt.ylabel(r"Magnitude [m]", fontsize=17)
    file_name = f"../figures/FRF_0_{shock}.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close() 

def viz_freqWake_reduced_velocity(reduced_velocity, mode_wake, freq_structural, strual_number = 0.2):
    plt.figure(figsize=(10, 5))
    # Scatter plot
    plt.scatter(reduced_velocity, mode_wake, color='royalblue', edgecolors='royalblue', facecolors='none', label='Mode Wake')

    # Axes labels
    plt.xlabel(r"$U_r$ [-]", fontsize=17)
    plt.ylabel(r"$f_{vs}$ [Hz]", fontsize=17)
    
    # Structural frequency horizontal line
    plt.hlines(freq_structural, 0, max(reduced_velocity) + 0.5, color='black', linestyle='dashdot', label='Structural frequency')
    
    # Theoretical lock-in range vertical line
    plt.vlines(1/strual_number, min(mode_wake) - 3, max(mode_wake) + 3, color='black', linestyle='dashdot')
    
    # Adding vertical text for the vertical line
    plt.text(1/strual_number - 0.3, min(mode_wake) +4, 
             r"Theoretical Lock-in Range", rotation=90, fontsize=9, color='black', va='center')
    plt.text(0.1, freq_structural + 0.8, 
             r"Structural frequency", fontsize=10, color='black', va='center')
    
    plt.xticks([0, 2, 4, 5, 6, 8])
    plt.yticks([10, 15, 20, 22, 25, 30, 35])
    plt.xlim(0, max(reduced_velocity) + 0.5)
    plt.ylim(min(mode_wake) - 3, max(mode_wake) + 3)
    # Save and show the plot
    file_name = "../figures/freqWake_reduced_velocity.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()

def viz_amplitudeDisp_reduced_velocity(reduced_velocity, amplitude, strual_number = 0.2):
    plt.figure(figsize=(10, 4))
    plt.scatter(reduced_velocity, amplitude, color='royalblue', edgecolors='royalblue', facecolors='none')
    plt.xlim(0, max(reduced_velocity) + 0.5)
    plt.ylim(min(amplitude), max(amplitude) + 0.005)
        # Theoretical lock-in range vertical line
    plt.vlines(1/strual_number, min(amplitude) - 3, max(amplitude) + 3, color='black', linestyle='dashdot')
    
    # Adding vertical text for the vertical line
    plt.text(1/strual_number + 0.2, min(amplitude) + 0.0055, 
            r"Theoretical Lock-in Range", rotation=90, fontsize=9, color='black', va='center')
    plt.xlabel(r"$U_r$ [-]", fontsize=17)
    plt.ylabel(r"$A_{max}$ [m]", fontsize=17)
    plt.xticks([0, 2, 4, 5, 6, 8])
    plt.yticks([0, 0.005, 0.010, 0.015, 0.020])
    file_name = f"../figures/amplitudeDisp_reduced_velocity.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()


def viz_RMS_reduced_velocity(reduced_velocity, rms_displacement, strual_number = 0.2):
    plt.figure(figsize=(10, 4))
    plt.scatter(reduced_velocity, rms_displacement*1e3, color='royalblue', edgecolors='royalblue', facecolors='none')
    plt.xlim(0, max(reduced_velocity) + 0.5)
    plt.ylim(min(rms_displacement), max(rms_displacement) + 5)
    plt.xlabel(r"Reduced Velocity $U_r$ [-]", fontsize=17)
    plt.ylabel(r"RMS displacement [mm]", fontsize=17)
    plt.xticks([0, 2, 4, 5, 6, 8])
    plt.yticks([0, 5, 10, 15, 20])
    file_name = f"../figures/RMS_reduced_velocity.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()


def viz_freqWake_reduced_velocity_with_strual(reduced_velocity, mode_wake, freq_structural, strual_number = 0.2):
    plt.figure(figsize=(10, 5))
    # Scatter plot
    plt.scatter(reduced_velocity, mode_wake, color='royalblue', edgecolors='royalblue', facecolors='none', label='Mode Wake')

    # Axes labels
    plt.xlabel(r"$U_r$ [-]", fontsize=17)
    plt.ylabel(r"$f_{vs}$ [Hz]", fontsize=17)
    plt.plot(np.insert(reduced_velocity, 0, 0), np.insert(reduced_velocity, 0, 0)*strual_number*freq_structural, color='black', linestyle='dashdot')
    # Structural frequency horizontal line
    plt.hlines(freq_structural, 0, max(reduced_velocity) + 0.5, color='black', linestyle='dashdot', label='Structural frequency')
    
    # Theoretical lock-in range vertical line
    plt.vlines(1/strual_number, min(mode_wake) - 3, max(mode_wake) + 3, color='black', linestyle='dashdot')
     
    # Adding vertical text for the vertical line
    plt.text(1/strual_number - 0.3, min(mode_wake) +4, 
             r"Theoretical Lock-in Range", rotation=90, fontsize=9, color='black', va='center')
    plt.text(0.1, freq_structural + 0.8, 
             r"Structural frequency", fontsize=10, color='black', va='center')
    
    
    plt.xticks([0, 2, 4, 5, 6, 8])
    plt.yticks([10, 15, 20, 22, 25, 30, 35])
    plt.xlim(0, max(reduced_velocity) + 0.5)
    plt.ylim(min(mode_wake) - 3, max(mode_wake) + 3)
    # Save and show the plot
    file_name = "../figures/freqWake_reduced_velocityStouhal.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()