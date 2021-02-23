# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:46:42 2019

@author: Admin
"""

import mne
import numpy as np
from scipy import stats

import os
import copy
import matplotlib.pyplot as plt
import statsmodels.stats.multitest as mul
import pdfkit

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')
        

def add_pic_html(filename, pic):
    add_str_html(filename, '<IMG SRC="%s" style="width:%spx;height:%spx;"/>'%(pic,1900,162))


def get_short_legend(contrast):
    temp = contrast.split('_')
    return (temp[0], temp[2], temp[3], temp[4])

def delaete_bad_sub(contrast, del_list):
    for sub in del_list:
        if sub in contrast[1]:
            ind = contrast[1].index(sub)
            contrast[1].pop(ind)
            contrast[0] = np.delete(contrast[0], ind, axis=0)
    return contrast

def p_val_binary(p_val_n, treshold):
    p_val =  copy.deepcopy(p_val_n)
    for raw in range(p_val.shape[0]):
        for collumn in range(p_val.shape[1]):
            if p_val[raw, collumn] < treshold:
                p_val[raw, collumn] = 1
            else:
                p_val[raw, collumn] = 0
    return p_val



def space_fdr(p_val_n):
    print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    for i in range(temp.shape[1]):
        _, temp[:,i] = mul.fdrcorrection(p_val_n[:,i])
    return temp

path = os.getcwd()
list_files = os.listdir(path)

output = 'output_topo/'


topomaps = ["condition1",
            "condition2",
            "difference",
            
            "p_value_cut",
            "difference_with_fdr",
            
            "p_value_cut_with_fdr",
            "p_value",
            ]

config = pdfkit.configuration(wkhtmltopdf='D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':1.0,
    'no-outline':None,
    'quiet':''
}

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

session = ["active1-st", "active2-end"]
stim = ["react"]
        
output = 'output_topo/'

os.makedirs(os.path.join(output, "w1c_vs_w2c-end"), exist_ok=True)        


temp = mne.Evoked("donor-ave.fif")


temp.nave = 24

temp.first = -500
temp.last = 5251

temp.times = np.arange(-2.0, 2.001, 0.001)

p_mul = 1.6

times_to_plot = np.arange(-1.6, 1.6, 0.2)
legend = ["w1c", "w2c-end"]

#temp.plot_topomap(times = [-0.1,0.2], ch_type='planar1', average = 0.035, time_unit='ms', show = True, title = 'Word-Dist 1 Dif', colorbar = True,  vmax=8, vmin=-8)

rewrite = True
if rewrite:
    contr = np.zeros((len(subjects), 2, 306, 4001))
    for ind, subj in enumerate(subjects):
        temp1 = mne.Evoked(os.path.join(os.getcwd(), "{0}_{1}_{2}_beta-ave.fif".format(subj, session[0], stim[0])))
        temp1 = temp1.pick_types("grad")
        contr[ind, 0, :204, :] = temp1.data
        contr[ind, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
        temp2 = mne.Evoked(os.path.join(os.getcwd(), "{0}_{1}_{2}_beta-ave.fif".format(subj, session[1], stim[0])))
        temp2 = temp2.pick_types("grad")

        contr[ind, 1, :204, :] = temp2.data
        contr[ind, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]
    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]

    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)
    p_val_fdr = space_fdr(p_val)

    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    

        
    
    ##### CONDITION1 ######
    
    temp.data = comp1_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = legend[0], colorbar = True, vmax=p_mul, vmin=-p_mul)
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"condition1.png"), dpi = 300)
    

    plt.close()

    ##### CONDITION2 ######
    
    temp.data = comp2_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = legend[1], colorbar = True, vmax=p_mul, vmin=-p_mul)
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"condition2.png"), dpi = 300)
    plt.close()
    
    ##### CONDITION2 - CONDITION1 with marks (no FDR) ######
    
    binary = p_val_binary(p_val, treshold = 0.05)
    temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "%s - %s"%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul, vmin=-p_mul, extrapolate="local", mask = np.bool_(binary[204:,:]),
                            mask_params = dict(marker='o', markerfacecolor='yellow', markeredgecolor='k',
                                               linewidth=0, markersize=10, markeredgewidth=2))
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"difference.png"), dpi = 300)
    plt.close()
    
    ##### CONDITION2 - CONDITION1 cutted by thershold (NO FDR) ######
    
    binary = p_val_binary(p_val, treshold = 0.05)
    temp.data = (comp2_mean[204:,:] - comp1_mean[204:,:])*binary[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "%s - %s (cut)"%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul, vmin=-p_mul, extrapolate="local")
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"p_value_cut.png"), dpi = 300)
    plt.close()
    
    ##### CONDITION2 - CONDITION1 with marks (WITH FDR) ######
    
    binary = p_val_binary(p_val_fdr, treshold = 0.05)
    temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "%s - %s with_fdr"%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul, vmin=-p_mul, extrapolate="local", mask = np.bool_(binary[204:,:]),
                            mask_params = dict(marker='o', markerfacecolor='yellow', markeredgecolor='k',
                                               linewidth=0, markersize=10, markeredgewidth=2))
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"difference_with_fdr.png"), dpi = 300)
    plt.close()
    
    ##### CONDITION2 - CONDITION1 cutted by thershold (WITH FDR) ######
    
    binary = p_val_binary(p_val_fdr, treshold = 0.05)
    temp.data = (comp2_mean[204:,:] - comp1_mean[204:,:])*binary[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "%s - %s (cut) with fdr"%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul, vmin=-p_mul, extrapolate="local")
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"p_value_cut_with_fdr.png"), dpi = 300)
    plt.close()
    
    ##### LOG(20*P_VAL) ######
    
    temp.data = np.log(p_val[204:,:]*20)

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "LOG(20*p_val)", image_interp = None, colorbar = True, extrapolate="local")
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"p_value.png"), dpi = 300)
    plt.close()
    
    #import sys
   # sys.exit()



html_name = os.path.join(output, legend[0] + "_vs_" + legend[1] + ".html")
clear_html(html_name)
add_str_html(html_name, '<!DOCTYPE html>')
add_str_html(html_name, '<html>')
add_str_html(html_name, '<body>')
add_str_html(html_name, '<p style="font-size:20px;"><b> %s, average beta 15-25 from reaction </b></p>' % (legend[0] + "_vs_" + legend[1]))
add_str_html(html_name, '<p style="font-size:20px;"><b> P_val < 0.05 marked (or saved from cutting) </b></p>' )
add_str_html(html_name, '<table>')
for topo in topomaps:
    add_str_html(html_name, "<tr>")
    add_pic_html(html_name, os.path.join(legend[0] + "_vs_" + legend[1],topo+".png"))
add_str_html(html_name, "</tr>")
add_str_html(html_name, '</body>')
add_str_html(html_name, '</html>')
pdf_file = html_name.replace("html", "pdf")
pdfkit.from_file(html_name, pdf_file, configuration = config, options=options)
    
