import sys
import mne
import numpy as np
import os

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
    #'403_skju',
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


sessions = ["active1", "active2"]
data_path = '/net/synology/volume1/data/programs/ANYA/SPEECH_LEARN/RAW_trans/'
cov_path = "covariance/"
fwd_path = '/net/synology/volume1/data/programs/ANYA/SPEECH_LEARN/PYTHON/MNE/FWD/'
inv_path = 'inverse_data/'
reject = dict(grad = 5e-10, mag = 9e-11, eog = 1e-2)
period_start = -1.000
period_end = 5.750

subj = subjects[0]
pref = sessions[0]
words = ["word", "dist"]

for ind, subj in enumerate(subjects):
    print("\t",subj)
    for pref in sessions:
        print("\t"*2,pref)
        for stim in words:
            print("\t"*3,stim)

            raw_file = os.path.join(data_path, subj,"{0}_{1}_raw_tsss_bads_trans.fif".format(subj,pref))
            raw_data = mne.io.Raw(raw_file)
            fwd_file = os.path.join(fwd_path,'{0}_active1_raw_tsss_bads_trans-ico-4-fwd.fif'.format(subj))
            fwd_data = mne.read_forward_solution(fwd_file)
            cov_file = os.path.join(os.getcwd(), cov_path, subj + "_" + pref + "_" + stim + "-cov.fif")
            cov_data = mne.read_cov(cov_file)

            inverse_operator = mne.minimum_norm.make_inverse_operator(raw_data.info, fwd_data, cov_data, loose = 0.4)
            mne.minimum_norm.write_inverse_operator(os.path.join(os.getcwd(), inv_path, "{0}_{1}_{2}_raw_tsss_bads_trans-ico-4-inv.fif".format(subj,pref, stim)), inverse_operator)


