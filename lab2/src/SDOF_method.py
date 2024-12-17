import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def compute_linear_interp(freq, H, sample):
    linear_interp = interp1d(freq, H, kind='linear')
    new_freq = np.linspace(freq[0], freq[-1], sample)
    new_H = linear_interp(new_freq)
    return new_freq, new_H

def compute_peak_picking_method(H, freq, plot=True, path="") :
    # Calculer l'amplitude du signal
    # Identifier l'indice du pic principal
    amplitude = np.abs(H) 
    main_peak_index = np.argmax(amplitude)
    main_peak_amplitude = H[main_peak_index]
    main_peak_freq      = freq[main_peak_index]
    mask            = (freq >= main_peak_freq - 2) & (freq <= main_peak_freq + 2)
    freq            = freq[mask]
    amplitude       = amplitude[mask]
    lin_freq, lin_H = compute_linear_interp(freq, amplitude, 10000)
    main_peak_index = np.argmax(lin_H)
    # print(np.min(lin_freq), print(np.max(lin_freq)))
    
    # Calculer le point de demi-puissance
    half_power_point = main_peak_amplitude / np.sqrt(2)
    
    # Trouver les fréquences aux points de demi-puissance autour du pic
    idx_Walpha = np.where(lin_H[:main_peak_index] <= half_power_point)[0][-1] if np.any(lin_H[:main_peak_index] < half_power_point) else KeyError("No value found")
    idx_Wbeta  = np.where(lin_H[main_peak_index:] <= half_power_point)[0][0] + main_peak_index if np.any(lin_H[main_peak_index:] < half_power_point) else  KeyError("No value found")
    
    f_Walpha = lin_freq[idx_Walpha]
    f_Wbeta = lin_freq[idx_Wbeta]
    damping = (f_Wbeta - f_Walpha) / (2 * main_peak_freq)
    if plot :
        save_path = f"{path}/peak_method.pdf"
        plt.figure(figsize=(8, 5))
        plt.plot(lin_freq, lin_H, color="darkblue", linewidth=1.5, label="Amplitude")
        plt.vlines([f_Walpha, f_Wbeta], ymin=0, ymax=lin_H[idx_Walpha], color="gray", linestyle="--", linewidth=1)
        
        # Annoter les fréquences omega_a, omega_b et la distance delta omega
        plt.text(f_Walpha - 0.07, half_power_point + half_power_point/10, r'$\omega_a$', ha='center', va='top', fontsize=14)
        plt.text(f_Wbeta + 0.07, half_power_point + half_power_point/10, r'$\omega_b$', ha='center', va='top', fontsize=14)
        plt.annotate(
        '', 
        xy=(f_Wbeta, half_power_point), 
        xytext=(f_Walpha, half_power_point),
        arrowprops=dict(arrowstyle='<->', color='black', lw=1.2)
        )
        plt.text((f_Walpha + f_Wbeta) / 2, half_power_point -half_power_point/10, r'$\Delta \omega$', 
            ha='center', va='bottom', fontsize=14)
        
        # Annoter le pic principal et le point de demi-puissance
        plt.scatter(main_peak_freq, main_peak_amplitude, color="crimson", label="Pic Principal", zorder=5)
        plt.scatter(f_Wbeta, half_power_point, color="#556B2F", label="Demi-puissance", zorder=5)
        plt.scatter(f_Walpha, half_power_point, color="#556B2F", zorder=5)
        plt.hlines(main_peak_amplitude, lin_freq[0], lin_freq[-1], color="black", linestyle=":", linewidth=1.5)
        plt.hlines(half_power_point, lin_freq[0], lin_freq[-1], color="black", linestyle=":", linewidth=1.5)
        plt.text(main_peak_freq +  1, main_peak_amplitude - half_power_point/10, r'$H^{max}_{rs(k)}$', va='center', fontsize=14)
        plt.text(main_peak_freq + 1, half_power_point - half_power_point/9, r'$\frac{H^{max}_{rs(k)}}{\sqrt{2}}$', va='center', fontsize=19)
        
        # plt.ylim(0, main_peak_amplitude + main_peak_amplitude/15)
        # plt.xlim(lin_freq[idx_Walpha] - 1, lin_freq[idx_Walpha] + 1)

        plt.xlabel("Frequency [Hz]", fontsize=15)
        plt.ylabel("Amplitude [m]", fontsize=15)

        # plt.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")
        plt.savefig(save_path, format="pdf", dpi=300)
        # plt.show()
        plt.close()
    return damping