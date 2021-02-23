#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:30:43 2021

@author: niherus
"""
#Paths of fif files for generate images
data_path = "/net/nas1/srv/data/server/data/home/niherus/Desktop/Python/Make_source_for_beta/MAIN_SCRIPT/Sensor/Evoked/beta_reactclean_15_26"

#List of subjects
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

#File formats
file_format = "{0}_{1}_{2}_beta-ave.fif"

#List of Comparisons
comparisons = {
    "active1 vs sctive2":
        [
            ["active1-st", "active2-end"],
            ["react", "react"]
        ]
    }

    
#Output folder
output = 'output_topo/'

#Plot/Topomap params
p_mul = 1.6
tmin = -1.0
tmax = 1.4
tstep = 0.2
average = 0.05
fmin = 15
fmax = 25
fstep = 2
units = "dB"
#