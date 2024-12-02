import numpy as np
import matplotlib.pyplot as plt
from scipy import io

# plt.rcParams['text.usetex'] = True
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['STIX Two Text'] + plt.rcParams['font.serif']
# plt.rcParams['figure.figsize'] = (6.34, 3.34)
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 200

data = io.loadmat(r"..\res\DATAG2_v7")["exp_data"][0]
# print(data)

sampling_freqHz = 201.03 # How ? 
sampling_tstep = 1/sampling_freqHz

run0 = data[0]
pitch0 = run0[0].flatten()
plunge0 = run0[1].flatten()
airspeed0 = run0[2].flatten()[0]
print(airspeed0)
n_sample0 = plunge0.size
t_sample0 = np.linspace(0, n_sample0*sampling_tstep, n_sample0)

fig = plt.figure()
fig.suptitle(f"Response to an external impulsion ($U_\\infty$ = {airspeed0} m/s)")
fig.supxlabel("Time (s)")
fig.supylabel("Acceleration (m/s²)")

gs = fig.add_gridspec(2, 1, hspace=0.5)
(ax_pitch, ax_plunge) = gs.subplots()

ax_pitch.plot(t_sample0, pitch0)
ax_pitch.set_title("Pitch")
ax_plunge.plot(t_sample0, plunge0)
ax_plunge.set_title("Plunge")

fig.savefig("../figures/impulsion_response.png")
