import numpy as np
import matplotlib.pyplot as plt
from scipy import io

def data_speed(data_pass) :
    data = io.loadmat(data_pass)["exp_data"][0]
    sampling_freqHz = 201.03 # How ? 
    sampling_tstep = 1/sampling_freqHz
    airspeed = {}
    for i in range(len(data)) :
        run0 = data[i]
        pitch0 = run0[0].flatten()
        plunge0 = run0[1].flatten()
        airspeed0 = run0[2].flatten()[0]
        n_sample0 = plunge0.size
        t_sample0 = np.linspace(0, n_sample0*sampling_tstep, n_sample0)
        plunge_pitch = {"pitch": pitch0, "plunge": plunge0, "time": t_sample0}
        airspeed[airspeed0] = plunge_pitch
    return airspeed

def extract_test(data) :
    setup_test = {}
    idx_test_1_0 = np.where((data[0.0]["time"] > 8.6) & (data[0.0]["time"] < 11))
    
    time_start_0 = np.linspace(0, data[0.0]["time"][idx_test_1_0][-1] - data[0.0]["time"][idx_test_1_0][0], len(idx_test_1_0[0]))
    test_1_speed_0 = {"pitch": data[0.0]["pitch"][idx_test_1_0], "plunge": data[0.0]["plunge"][idx_test_1_0], "time": time_start_0}
    
    idx_test_2_0 = np.where((data[0.0]["time"] > 15.2) & (data[0.0]["time"] < 17))
    time_start_0 = np.linspace(0, data[0.0]["time"][idx_test_2_0][-1] - data[0.0]["time"][idx_test_2_0][0], len(idx_test_2_0[0]))
    test_2_speed_0 = {"pitch": data[0.0]["pitch"][idx_test_2_0], "plunge": data[0.0]["plunge"][idx_test_2_0], "time": time_start_0}
    idx_test_3_0 = np.where((data[0.0]["time"] > 21.3) & (data[0.0]["time"] < 23.5))
    time_start_0 = np.linspace(0, data[0.0]["time"][idx_test_3_0][-1] - data[0.0]["time"][idx_test_3_0][0], len(idx_test_3_0[0]))
    test_3_speed_0 = {"pitch": data[0.0]["pitch"][idx_test_3_0], "plunge": data[0.0]["plunge"][idx_test_3_0], "time": time_start_0}
    setup_test[0.0] = {"test_1": test_1_speed_0, "test_2": test_2_speed_0, "test_3": test_3_speed_0}
    
    
    idx_test_2_6 = np.where((data[6.4]["time"] > 17.6) & (data[6.4]["time"] < 20))
    time_start_0 = np.linspace(0, data[6.4]["time"][idx_test_2_6][-1] - data[6.4]["time"][idx_test_2_6][0], len(idx_test_2_6[0]))
    test_2_speed_6 = {"pitch": data[6.4]["pitch"][idx_test_2_6], "plunge": data[6.4]["plunge"][idx_test_2_6], "time": time_start_0}
    
    idx_test_3_6 = np.where((data[6.4]["time"] > 23.16) & (data[6.4]["time"] < 24.5))
    time_start_0 = np.linspace(0, data[6.4]["time"][idx_test_3_6][-1] - data[6.4]["time"][idx_test_3_6][0], len(idx_test_3_6[0]))
    test_3_speed_6 = {"pitch": data[6.4]["pitch"][idx_test_3_6], "plunge": data[6.4]["plunge"][idx_test_3_6], "time": time_start_0}
    
    idx_test_4_6 = np.where((data[6.4]["time"] > 28.18) & (data[6.4]["time"] < 31))
    time_start_0 = np.linspace(0, data[6.4]["time"][idx_test_4_6][-1] - data[6.4]["time"][idx_test_4_6][0], len(idx_test_4_6[0]))
    test_4_speed_6 = {"pitch": data[6.4]["pitch"][idx_test_4_6], "plunge": data[6.4]["plunge"][idx_test_4_6], "time": time_start_0}
    setup_test[6.4] = {"test_1": test_2_speed_6, "test_2": test_3_speed_6, "test_3": test_4_speed_6}

    
    # Données pour la vitesse 9.6
    idx_test_1_9 = np.where((data[9.6]["time"] > 18.8) & (data[9.6]["time"] < 21))
    time_start_0 = np.linspace(0, data[9.6]["time"][idx_test_1_9][-1] - data[9.6]["time"][idx_test_1_9][0], len(idx_test_1_9[0]))
    test_1_speed_9 = {"pitch": data[9.6]["pitch"][idx_test_1_9], "plunge": data[9.6]["plunge"][idx_test_1_9], "time": time_start_0}

    idx_test_2_9 = np.where((data[9.6]["time"] > 23.85) & (data[9.6]["time"] < 25))
    time_start_0 = np.linspace(0, data[9.6]["time"][idx_test_2_9][-1] - data[9.6]["time"][idx_test_2_9][0], len(idx_test_2_9[0]))
    test_2_speed_9 = {"pitch": data[9.6]["pitch"][idx_test_2_9], "plunge": data[9.6]["plunge"][idx_test_2_9], "time": time_start_0}

    idx_test_3_9 = np.where((data[9.6]["time"] > 27.8) & (data[9.6]["time"] < 32))
    time_start_0 = np.linspace(0, data[9.6]["time"][idx_test_3_9][-1] - data[9.6]["time"][idx_test_3_9][0], len(idx_test_3_9[0]))
    test_3_speed_9 = {"pitch": data[9.6]["pitch"][idx_test_3_9], "plunge": data[9.6]["plunge"][idx_test_3_9], "time": time_start_0}
    setup_test[9.6] = {
        "test_1": test_1_speed_9,
        "test_2": test_2_speed_9,
        "test_3": test_3_speed_9
    }

    # Données pour la vitesse 12.1
    idx_test_1_12 = np.where((data[12.1]["time"] > 23.7) & (data[12.1]["time"] < 25))
    time_start_0 = np.linspace(0, data[12.1]["time"][idx_test_1_12][-1] - data[12.1]["time"][idx_test_1_12][0], len(idx_test_1_12[0]))
    test_1_speed_12 = {"pitch": data[12.1]["pitch"][idx_test_1_12], "plunge": data[12.1]["plunge"][idx_test_1_12], "time": time_start_0}

    idx_test_2_12 = np.where((data[12.1]["time"] > 16.7) & (data[12.1]["time"] < 18))
    time_start_0 = np.linspace(0, data[12.1]["time"][idx_test_2_12][-1] - data[12.1]["time"][idx_test_2_12][0], len(idx_test_2_12[0]))
    test_2_speed_12 = {"pitch": data[12.1]["pitch"][idx_test_2_12], "plunge": data[12.1]["plunge"][idx_test_2_12], "time": time_start_0}

    idx_test_3_12 = np.where((data[12.1]["time"] > 20) & (data[12.1]["time"] < 22))
    time_start_0 = np.linspace(0, data[12.1]["time"][idx_test_3_12][-1] - data[12.1]["time"][idx_test_3_12][0], len(idx_test_3_12[0]))
    test_3_speed_12 = {"pitch": data[12.1]["pitch"][idx_test_3_12], "plunge": data[12.1]["plunge"][idx_test_3_12], "time": time_start_0}

    setup_test[12.1] = {
        "test_1": test_1_speed_12,
        "test_2": test_2_speed_12,
        "test_3": test_3_speed_12
    }

    # Données pour la vitesse 14.8
    idx_test_1_14 = np.where((data[14.8]["time"] > 22.61) & (data[14.8]["time"] < 25))
    time_start_0 = np.linspace(0, data[14.8]["time"][idx_test_1_14][-1] - data[14.8]["time"][idx_test_1_14][0], len(idx_test_1_14[0]))
    test_1_speed_14 = {"pitch": data[14.8]["pitch"][idx_test_1_14], "plunge": data[14.8]["plunge"][idx_test_1_14], "time": time_start_0}

    idx_test_2_14 = np.where((data[14.8]["time"] > 31) & (data[14.8]["time"] < 35))
    time_start_0 = np.linspace(0, data[14.8]["time"][idx_test_2_14][-1] - data[14.8]["time"][idx_test_2_14][0], len(idx_test_2_14[0]))
    test_2_speed_14 = {"pitch": data[14.8]["pitch"][idx_test_2_14], "plunge": data[14.8]["plunge"][idx_test_2_14], "time": time_start_0}

    idx_test_3_14 = np.where((data[14.8]["time"] > 41.4) & (data[14.8]["time"] < 46))
    time_start_0 = np.linspace(0, data[14.8]["time"][idx_test_3_14][-1] - data[14.8]["time"][idx_test_3_14][0], len(idx_test_3_14[0]))
    test_3_speed_14 = {"pitch": data[14.8]["pitch"][idx_test_3_14], "plunge": data[14.8]["plunge"][idx_test_3_14], "time": time_start_0}

    setup_test[14.8] = {
        "test_1": test_1_speed_14,
        "test_2": test_2_speed_14,
        "test_3": test_3_speed_14
    }

    # Données pour la vitesse 16.4
    idx_test_1_16 = np.where((data[16.4]["time"] > 56.64) & (data[16.4]["time"] < 61))
    time_start_0 = np.linspace(0, data[16.4]["time"][idx_test_1_16][-1] - data[16.4]["time"][idx_test_1_16][0], len(idx_test_1_16[0]))
    test_1_speed_16 = {"pitch": data[16.4]["pitch"][idx_test_1_16], "plunge": data[16.4]["plunge"][idx_test_1_16], "time": time_start_0}

    idx_test_2_16 = np.where((data[16.4]["time"] > 68.2) & (data[16.4]["time"] < 70))
    time_start_0 = np.linspace(0, data[16.4]["time"][idx_test_2_16][-1] - data[16.4]["time"][idx_test_2_16][0], len(idx_test_2_16[0]))
    test_2_speed_16 = {"pitch": data[16.4]["pitch"][idx_test_2_16], "plunge": data[16.4]["plunge"][idx_test_2_16], "time": time_start_0}

    idx_test_3_16 = np.where((data[16.4]["time"] > 72.39) & (data[16.4]["time"] < 78))
    time_start_0 = np.linspace(0, data[16.4]["time"][idx_test_3_16][-1] - data[16.4]["time"][idx_test_3_16][0], len(idx_test_3_16[0]))
    test_3_speed_16 = {"pitch": data[16.4]["pitch"][idx_test_3_16], "plunge": data[16.4]["plunge"][idx_test_3_16], "time": time_start_0}

    setup_test[16.4] = {
        "test_1": test_1_speed_16,
        "test_2": test_2_speed_16,
        "test_3": test_3_speed_16
    }

    # Données pour la vitesse 17.6
    idx_test_1_17 = np.where((data[17.6]["time"] > 15.12) & (data[17.6]["time"] < 23.51))
    time_start_0 = np.linspace(0, data[17.6]["time"][idx_test_1_17][-1] - data[17.6]["time"][idx_test_1_17][0], len(idx_test_1_17[0]))
    test_1_speed_17 = {"pitch": data[17.6]["pitch"][idx_test_1_17], "plunge": data[17.6]["plunge"][idx_test_1_17], "time": time_start_0}

    idx_test_2_17 = np.where((data[17.6]["time"] > 29.98) & (data[17.6]["time"] < 37))
    time_start_0 = np.linspace(0, data[17.6]["time"][idx_test_2_17][-1] - data[17.6]["time"][idx_test_2_17][0], len(idx_test_2_17[0]))
    test_2_speed_17 = {"pitch": data[17.6]["pitch"][idx_test_2_17], "plunge": data[17.6]["plunge"][idx_test_2_17], "time": time_start_0}

    idx_test_3_17 = np.where((data[17.6]["time"] > 39.8) & (data[17.6]["time"] < 50))
    time_start_0 = np.linspace(0, data[17.6]["time"][idx_test_3_17][-1] - data[17.6]["time"][idx_test_3_17][0], len(idx_test_3_17[0]))
    test_3_speed_17 = {"pitch": data[17.6]["pitch"][idx_test_3_17], "plunge": data[17.6]["plunge"][idx_test_3_17], "time": time_start_0}

    setup_test[17.6] = {
        "test_1": test_1_speed_17,
        "test_2": test_2_speed_17,
        "test_3": test_3_speed_17
    }
    
    # Données pour la vitesse 18.8
    idx_test_1_18 = np.where((data[18.8]["time"] > 20) & (data[18.8]["time"] < 50))
    time_start_0 = np.linspace(0, data[18.8]["time"][idx_test_1_18][-1] - data[18.8]["time"][idx_test_1_18][0], len(idx_test_1_18[0]))
    test_1_speed_18 = {"pitch": data[18.8]["pitch"][idx_test_1_18], "plunge": data[18.8]["plunge"][idx_test_1_18], "time": time_start_0}

    setup_test[18.8] = {
        "test_1": test_1_speed_18
    }




    return setup_test