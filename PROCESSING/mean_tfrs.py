import mne, os, sys, numpy as np
from configure import *
mne.set_log_level("ERROR")

out_path = f'beta_{stim}_{L_freq}_{H_freq}/'
data_path = os.path.join(os.getcwd(), "Sensor", "TFR", out_path)
out_path = os.path.join(os.getcwd(), "Sensor", "TFR_mean", out_path)
os.makedirs(out_path, exist_ok = True)
sessions = [ ('active1', "st"), ('active2', "end")]


for pref in sessions:
    data = []
    for subj in subjects:
        print(subj)
        freq_file = os.path.join(os.getcwd(), data_path, "{0}_{1}-{2}_{3}_int_50ms-tfr.h5".format(subj,pref[0], pref[1], stim))   
        data.append(mne.time_frequency.read_tfrs(freq_file)[0])
    freq_data = mne.grand_average(data)
    freq_data.apply_baseline(baseline=(-0.5,-0.1), mode="logratio")

    freq_data.save(os.path.join(os.getcwd(), out_path, "ave_{0}-{1}_{2}_int_50ms-tfr.h5".format(pref[0], pref[1], stim)), overwrite=True)


