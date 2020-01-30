import mne, os, sys, numpy as np
from configure import *

mne.set_log_level("ERROR")

folder = f"beta_{stim + 'NEW'}_{L_freq}_{H_freq}"
data_path = os.path.join(os.getcwd(), 'Sensor', 'TFR', folder)
out_path = os.path.join(os.getcwd(), 'Sensor', 'Evoked', folder)
os.makedirs(out_path, exist_ok = True)
init()

sessions = [ ('active1', "st"), ('active2', "end")]


subjects = [ 
    '030_koal',

    '051_vlro',
    '128_godz',
    '136_spar',
    '176_nama',
    '202_skol',
    '211_gnlu',
    '277_trev',
    '307_firo',
    '308_lodm',
    '317_arel',
    '355_slya',
    '372_skju',
    '389_revi',
    '390_shko',
    '394_tiev',
    '402_maev',
    '406_bial',
    '409_kodm',
    '415_yael',
    '436_buni',
    '383_laan']

temp1 = mne.Evoked("383_laan_active2_word-ave.fif")

with open("configure.py", "r") as f_in:
    settings = f_in.readlines()
    with open(os.path.join(out_path, "confige.log"), "w") as f_out:
        f_out.writelines(settings)

for subj in subjects:
    print(subj)
    for pref in sessions:
	
        freq_file = os.path.join(os.getcwd(), data_path, "{0}_{1}-{2}_{3}_int_50ms-tfr.h5".format(subj,pref[0], pref[1], stim))   
        freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
        temp = freq_data.data.sum(axis=1)
        temp= temp.reshape(temp.shape[0],1,temp.shape[1])
        freq_data.data = temp
        #freq_data.apply_baseline(baseline=(-0.5,-0.1), mode="logratio")
        new_evoked = temp1.copy()
        new_evoked.info = freq_data.info
        new_evoked.nave = freq_data.nave
        new_evoked.kind = "average"
        new_evoked.times = freq_data.times
        new_evoked.first = 0
        new_evoked.last = new_evoked.times.shape[0] - 1
        new_evoked.comment = freq_data.comment
        new_evoked.data = freq_data.data.mean(axis=1)
        new_evoked.save(os.path.join(out_path, "{0}_{1}-{2}_{3}_beta-ave.fif".format(subj,pref[0], pref[1], stim)))


