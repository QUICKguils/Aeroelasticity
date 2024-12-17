import matplotlib.pyplot as plt
import numpy as np


# plt.rcParams['text.usetex'] = True
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
# plt.rcParams['figure.figsize'] = (6.34, 3.34)
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 200


def viz_speed_stabWithenvelope(speed_stab) :
    x = []
    y = []
    for i in speed_stab.keys():
        for j in speed_stab[i]["pitch"]:
            x.append(i)
            y.append(j)

    x = np.array(x)
    y = np.array(y)
    coeffs = np.polyfit(x, y, 2) 
    poly_fit = np.poly1d(coeffs)  
    x_fit = np.linspace(min(x), max(x), 500) 
    y_fit = poly_fit(x_fit)
    plt.figure()
    for i in speed_stab.keys():
        for j in speed_stab[i]["pitch"]:
            plt.scatter(i, j,facecolors='none', edgecolors='#4169E1')
    plt.scatter(20, 30, facecolors='none', edgecolors='#4169E1', label=r"Experimental Data")
    plt.plot(x_fit, y_fit, color="#808000", label=r"2nd Order curve Fit")
    plt.hlines(0, 0, 20, color="#800020", linestyles="dashdot", label=r"Flutter Boundary")
    plt.xlabel(r"Speed [m/s]")
    plt.legend()
    plt.ylabel(r"Stability criteria [$s^{-1}$]")
    plt.xlim(0, 19)
    plt.ylim(np.min(y) - 0.1, np.max(y) + 0.1)

    plt.savefig("../figures/speed_stability_envelope.pdf", bbox_inches='tight', format="pdf", dpi=300)