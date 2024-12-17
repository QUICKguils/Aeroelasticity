import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from scipy.interpolate import interp1d

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
plt.rcParams['font.size'] = 15
plt.rcParams['figure.dpi'] = 150

color_list = [
    "#1f77b4",  # Bleu (standard, agréable pour les graphiques)
    "#ff7f0e",  # Orange (chaleureux et visible)
    "#2ca02c",  # Vert (équilibré)
    "#d62728",  # Rouge (contrasté)
    "#9467bd",  # Violet (subtil et élégant)
    "#8c564b",  # Marron (neutre et sérieux)
    "#e377c2",  # Rose (dynamique)
    "#7f7f7f",  # Gris (sophistiqué et neutre)
    "#bcbd22",  # Vert-jaune (vivant)
    "#17becf",  # Cyan (frais et lumineux)
    "#ff9896",  # Rose clair (soft contrast)
    "#c5b0d5",  # Violet clair (épuré)
    "#9edae5",  # Cyan clair (moderne)
    "#f7b6d2",  # Rose pastel (doux)
    "#ffbb78",  # Orange pastel (chaleur)
]

def viz_FRF_0(amplitude, frequency, path="../figures/"):
    plt.figure(figsize=(10, 4))
    plt.plot(frequency, amplitude)
    plt.xlim(min(frequency), max(frequency))
    plt.ylim(min(amplitude), max(amplitude) + 0.05)
    plt.xticks([0, 10, 20, 22, 30, 40, 50])
    plt.xlabel(r"Frequency [Hz]", fontsize=17)
    plt.ylabel(r"Magnitude [m]", fontsize=17)
    plt.savefig(path, dpi=150, bbox_inches='tight')
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
    file_name = "../figures/gr3/freqWake_reduced_velocity.pdf"
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
    file_name = f"../figures/gr3/amplitudeDisp_reduced_velocity.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()

def viz_amplitudeWake_reduced_velocity(reduced_velocity, amplitude, strual_number = 0.2):
    plt.figure(figsize=(10, 4))
    plt.scatter(reduced_velocity, amplitude, color='royalblue', edgecolors='royalblue', facecolors='none')
    plt.xlim(0, max(reduced_velocity) + 0.5)
    # plt.ylim(min(amplitude), max(amplitude) + 0.005)
        # Theoretical lock-in range vertical line
    plt.vlines(1/strual_number, min(amplitude) - 3, max(amplitude) + 3, color='black', linestyle='dashdot')
    
    # Adding vertical text for the vertical line
    plt.text(1/strual_number + 0.2, min(amplitude) + 0.0055, 
            r"Theoretical Lock-in Range", rotation=90, fontsize=9, color='black', va='center')
    plt.xlabel(r"$U_r$ [-]", fontsize=17)
    plt.ylabel(r"$A_{max}$ [m/s]", fontsize=17)
    plt.xticks([0, 2, 4, 5, 6, 8])
    file_name = f"../figures/gr3/amplitudeWake_reduced_velocity.pdf"
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
    file_name = f"../figures/gr3/RMS_reduced_velocity.pdf"
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
    file_name = "../figures/gr3/freqWake_reduced_velocityStouhal.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()

def viz_freqWake_reduced_velocity(reduced_velocity, mode_wake, freq_structural, freq_structure_speed, strual_number = 0.2 ):
    plt.figure(figsize=(10, 5))
    # Scatter plot
    plt.scatter(reduced_velocity, mode_wake, color='royalblue', edgecolors='royalblue', facecolors='none', label='Mode Wake')
    plt.scatter(reduced_velocity, freq_structure_speed, color='red', label='Structural frequency', marker='x')
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
    file_name = "../figures/gr3/freqWake_reduced_velocity.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()


def viz_freqWake_reduced_velocity_damping(different_damp) :
    type_marker = ['o', 'v', '^', 'd', '+', 'p', '*']
    plt.figure(figsize=(10, 5)) 
    for i, key in enumerate(different_damp.keys()):
        plt.scatter(
            different_damp[key]["reduce_velocity"],
            different_damp[key]["mode_wake"],
            label=fr"$\eta$ : {different_damp[key]['damp']*100:.2f} [%]",
            edgecolors=color_list[i],
            facecolors='none',
            marker=type_marker[i],
        )
    
    plt.xlabel(r"$U_r$ [-]", fontsize=17)
    plt.ylabel(r"$f_{vs}$ [Hz]", fontsize=17)
    plt.legend()
    plt.xticks([0, 2, 4, 5, 6, 8])
    plt.yticks([10, 15, 20, 22, 25, 30, 35])
    # plt.xlim(0, 8)
    # plt.ylim(10, 35)
    file_name = "../figures/freqWake_reduced_velocity_damping_freq.pdf"
    plt.savefig(file_name, dpi=150, bbox_inches='tight')
    # plt.show()
    plt.close()

def viz_freqWake_reduced_velocity_amplitude(different_damp) :
    plt.figure(figsize=(10, 5))
    # Générer une palette de couleurs
    type_marker = ['o', 'v', '^', 'd', '+', 'p', '*']
    for i, key in enumerate(different_damp.keys()):
        # Extraire les données
        velocities = np.array(different_damp[key]["reduce_velocity"])
        amplitudes = np.array(different_damp[key]["amplitude"])
        plt.scatter(
            velocities,
            amplitudes,
            label=fr" $\eta$ : {different_damp[key]['damp']*100:.2f} [%]",
            edgecolors=color_list[i],
            facecolors='none',
            marker=type_marker[i],
        )
        
    # plt.scatter(different_damp["Common 1"]["reduce_velocity"], different_damp["Common 1"]["amplitude"], label="Common 1", edgecolors=color_list[0], facecolors='none')
    # plt.scatter(different_damp["Common 2"]["reduce_velocity"], different_damp["Common 2"]["amplitude"], label=f" = {different_damp[key]['damp']*100:.2f} [%]", edgecolors=color_list[1], facecolors='none')
    plt.xlabel(r"$U_r$ [-]", fontsize=17)
    plt.ylabel(r"$f_{vs}$ [Hz]", fontsize=17)
    plt.legend()
    path = "../figures/freqWake_reduced_velocity_damping_amplitude.pdf"
    # plt.show()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()


