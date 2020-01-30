import mne, os
import numpy as np
from mne import set_config
from joblib import Parallel, delayed
from configure import *
import pickle


set_config("MNE_MEMMAP_MIN_SIZE", "1M")
set_config("MNE_CACHE_DIR", ".tmp")

mne.set_log_level("ERROR")
os.makedirs("baseline", exist_ok=True)
init()

def read_events(filename):
    with open(filename, "r") as f:
        b = f.read().replace("[","").replace("]", "")
        b = b.split("\n")
        b = list(map(str.split, b))
        b = list(map(lambda x: list(map(int, x)), b))
        return np.array(b)

data_path = '/net/synology/volume1/data/programs/ANYA/SPEECH_LEARN/RAW_trans/'
out_path = f'beta_{stim + "NEW"}_{L_freq}_{H_freq}/'
os.makedirs(os.path.join(os.getcwd(), "Sensor", "TFR", out_path), exist_ok = True)

with open("configure.py", "r") as f_in:
    settings = f_in.readlines()
    with open(os.path.join(os.getcwd(), "Sensor", "TFR", out_path, "confige.log"), "w") as f_out:
        f_out.writelines(settings)
         

def calculate_beta(subj ):
    print(subj)
    mne.set_log_level("ERROR")
    freqs = np.arange(L_freq, H_freq, f_step)
    raw_file = os.path.join(data_path, subj,"{0}_{1}_raw_tsss_bads_trans.fif".format(subj,pref[0]))
    try:
        raw_data = mne.io.Raw(raw_file, preload=True)
    except:
        print("\t", "File wasn't found. Please, check the filename format")
        return 0
    

    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
    
    
    if stim == "react":
        events = read_events(os.path.join(os.getcwd(), "EVENTS", "{0}_{1}_{2}_{3}.txt".format(subj, pref[0], "w", pref[1])))
        events_react = read_events(os.path.join(os.getcwd(), "EVENTS", "{0}_{1}_{2}_{3}.txt".format(subj, pref[0], stim[0], pref[1])))
        epochs = mne.Epochs(raw_data, events_react, event_id = None, tmin = period_start, tmax = period_end, picks = picks, preload = True)
        freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = 8, use_fft = False, return_itc = False)
        with open(f"{os.getcwd()}/baseline/{subj}_{pref[0]}_{pref[1]}_baseline.txt", "rb") as f:
            b_line = pickle.load(f)
        freq_show.data = np.log10(freq_show.data/b_line[:, :, np.newaxis])
    else:
        events = read_events(os.path.join(os.getcwd(), "EVENTS", "{0}_{1}_{2}_{3}.txt".format(subj, pref[0], stim[0], pref[1])))
        epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start, tmax = period_end, baseline = baseline, picks = picks, preload = True)
        #epochs.resample(300)

        freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = 8, use_fft = False, return_itc = False)
        '''
        with open(f"{os.getcwd()}/baseline/{subj}_{pref[0]}_{pref[1]}_baseline.txt", "wb") as f:
            pickle.dump(freq_show.data[:, :, 500:900].mean(axis=-1), f)
        '''

    #if stim == "react":
        #freq_show.apply_baseline(baseline=(-0.5,-0.1), mode="ratio")
        #for freq_num in range(freq_show.data.shape[0]):
        #    freq_show.data[freq_num, :, :, :4000] = freq_show.data[freq_num, :, :, -int(period_start*1000) + move_time[freq_num] - 2000: -int(period_start*1000) + move_time[freq_num] + 2000 ]
        #req_show.data = freq_show.data[:, :, :, :4000]
        #freq_show.times = np.arange(-2.0, 2.0, 0.001)
        #freq_show = freq_show.average()
        
    freq_show.save(os.path.join(os.getcwd(), "Sensor", "TFR", out_path, "{0}_{1}-{2}_{3}_int_50ms-tfr.h5".format(subj, pref[0], pref[1], stim)), overwrite=True)
    print(subj, pref, " ended!")

p_func = delayed(calculate_beta)
parallel = Parallel(10, max_nbytes = None)

answ = input(f"Are you sure? Your beta data in {out_path} will be rewrited.\n")
if  answ == "" or answ != "yes":
    print("Analisys canceled")
else:
    parallel(p_func(subject) for subject in subjects)

