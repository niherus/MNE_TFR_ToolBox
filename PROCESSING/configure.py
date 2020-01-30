import os

def init():
    os.makedirs(os.path.join(os.getcwd(),"Sensor","TFR"), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),"Sensor","Evoked"), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),"Source","SourceEstimate"), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),"Source","MISC"), exist_ok=True)
    print("Start analysis")

stim = "word"

L_freq = 15
H_freq = 25
f_step = 2

period_start = -1.000
period_end = 5.750

baseline = (-0.5, -0.1)
pref = ('active2', "end")

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

