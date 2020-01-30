import sys
import mne
import numpy as np
import os

def  event_correction(event):
    if event > 8320:
        event -= 8320
    elif event > 4160 and event != 8320:
        event -= 4160
    return event

vec_event_correction = np.vectorize(event_correction)

subjects = [ 
    '030_koal',
    '050_gail',
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

eventCodes = {
    "hicha": 2,
    "hichu": 18,
    "hisha": 20,
    "hishu": 6,
    "hisa": 16,
    "hisu": 22,
    "hiva": 32,
    "hivu": 4
    }
sessions = ["active1", "active2"]
data_path = '/net/synology/volume1/data/programs/ANYA/SPEECH_LEARN/RAW_trans/'

reject = dict(grad = 5e-10, mag = 9e-11, eog = 1e-2)
period_start = -1.000
period_end = 5.750

words = [2, 6, 16, 4]

dists = [18, 20, 22, 32]

for ind, subj in enumerate(subjects):
    print("\t",subj)
    for pref in sessions:
        print("\t"*2,pref)
        raw_file = os.path.join(data_path, subj,"{0}_{1}_raw_tsss_bads_trans.fif".format(subj,pref))
        try:
            raw_data = mne.io.Raw(raw_file)
        except:
            print("\t" * 3,raw_file, "is not found\nCheck name format")
            
        picks = mne.pick_types(raw_data.info, meg = True, eog = True)
            
        events = mne.find_events(raw_data, stim_channel = "STI101", shortest_event = 1)
        events[:,2] = vec_event_correction(events[:,2])
        epochs = mne.Epochs(raw_data, events,
                    	event_id = words, tmin = period_start, tmax = period_end,
                    	baseline = (None, 0), picks = picks, preload = True, reject = reject)

        cov = mne.compute_covariance(epochs, tmax = 0)
        mne.write_cov("covariance/" + subj + "_" + pref + "_word-cov.fif", cov)
        print(subj + "_" + pref + "_word-cov.fif", "successfully saved")
            
        epochs = mne.Epochs(raw_data, events,
                    	event_id = dists, tmin = period_start, tmax = period_end,
                    	baseline = (None, 0), picks = picks, preload = True, reject = reject)

        cov = mne.compute_covariance(epochs, tmax = 0)
        mne.write_cov("covariance/" + subj + "_" + pref + "_dist-cov.fif", cov)
        print(subj + "_" + pref + "_dist-cov.fif", "successfully saved")

