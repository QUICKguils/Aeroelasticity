import PullData as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import enveloppe_fct as ef
import VizData as vd


data = pd.data_speed(r"..\res\DATAG2_v7")
data = pd.extract_test(data)
speed_stab = ef.get_speed_stab(data)

vd.viz_speed_stabWithenvelope(speed_stab)