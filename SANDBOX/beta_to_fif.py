# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 20:46:42 2019

@author: Admin
"""

import mne
import numpy as np
from scipy import stats
from mne import set_config
import os
import copy
import matplotlib.pyplot as plt
import statsmodels.stats.multitest as mul
from fpdf import FPDF
from configure import *

set_config("MNE_MEMMAP_MIN_SIZE", "1M")
set_config("MNE_CACHE_DIR", ".tmp")

mne.set_log_level("ERROR")       

def add_pic_html(filename, pic):
    add_str_html(filename, '<IMG SRC="%s" style="width:%spx;height:%spx;"/>'%(pic,1900,162))


def get_short_legend(contrast):
    temp = contrast.split('_')
    return (temp[0], temp[2], temp[3], temp[4])

def generate_legend(comp_name):
    params = comparisons[comp_name]
    
    if params[0][0] != params[0][1]:
        return params[0]
    else:
        return params[1]

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
    temp = copy.deepcopy(p_val_n)
    for i in range(temp.shape[1]):
        _, temp[:,i] = mul.fdrcorrection(p_val_n[:,i])
    return temp

def full_fdr(p_val_n):
    w, h = p_val_n.shape
    p_val_resh = p_val_n.reshape((w*h))
    _, p_val_resh_fdr = mul.fdrcorrection(p_val_resh)
    return p_val_resh_fdr.reshape((w, h))

def generate_array(comp_name, tmin = None, tmax = None):
    params = comparisons[comp_name]
    
    test = mne.Evoked(os.path.join(data_path, 
                            file_format.format(subjects[0],
                                               params[0][0], 
                                               params[1][0])))
    test.shift_time(-2.0)
    test = test.crop(tmin, tmax)
    return np.zeros((len(subjects), 2, *test.data.shape))
    

pdf = FPDF(orientation="L", unit="pt", format="A3")
pdf.set_font("Times", size = 18)
output = 'output_topo/'


topomaps = ["cmp1_fdr",
            "cmp2_fdr",
            "dif_nofdr",
            "dif_fdr",
            

            ]

       
for folder in comparisons.keys():

    os.makedirs(os.path.join(output, folder), exist_ok=True)        

times_to_plot = np.arange(tmin, tmax, tstep)

rewrite = True
if rewrite:
    for comp_name in comparisons.keys():
        print(comp_name, "started")
        pdf.add_page()
        contr = generate_array(comp_name, tmin, tmax)
        legend = generate_legend(comp_name)
        params = comparisons[comp_name]
        
        for ind, subj in enumerate(subjects):
            
            for i in range(2):
                temp = mne.Evoked(os.path.join(data_path,
                            file_format.format(subjects[ind],
                                               params[0][i], 
                                               params[1][i])))
                temp.shift_time(-2.0)
                temp = temp.pick_types("grad").crop(tmin, tmax)
                contr[ind, i, :204, :] = temp.data
                contr[ind, i, 204:, :] = temp.data[::2] + temp.data[1::2]
            print(subj, "added to analysis")
        comp1 = contr[:, 0, :, :]
        comp2 = contr[:, 1, :, :]
        
        t_stat_dif, p_val_dif = stats.ttest_rel(comp1, comp2, axis=0)
        t_stat_cmp1, p_val_cmp1 = stats.ttest_1samp(comp1, popmean=0, axis=0)
        t_stat_cmp2, p_val_cmp2 = stats.ttest_1samp(comp2, popmean=0, axis=0)
        
        
        comp1_mean = comp1.mean(axis=0)
        comp2_mean = comp2.mean(axis=0)
        
        temp.pick_types(meg="planar1")
        donor = mne.EvokedArray(data=temp.data, info=temp.info)
        
        
        if "cmp1_nofdr" in topomaps:
            ##### CONDITION1 (no FDR) ###### 
            temp.data = comp1_mean[204:,:]
            binary = p_val_binary(p_val_cmp1, treshold = 0.05)
            fig = temp.plot_topomap(times = times_to_plot, average = average,
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = legend[0] + " nofdr", colorbar = True, 
                                vmax=p_mul, vmin=-p_mul, extrapolate="local",
                                mask = np.bool_(binary[204:,:]), units=units,
                                mask_params = dict(marker='o',
                                                   markerfacecolor='w', 
                                                   markeredgecolor='k',
                                                   linewidth=0,
                                                   markersize=7,
                                                   markeredgewidth=2))
            fig.savefig(os.path.join(output,
                                     comp_name,
                                     "cmp1_nofdr.png"),
                        dpi = 300)
        
    
            plt.close()
        
        if "cmp1_fdr" in topomaps:
            ##### CONDITION1 (FDR) ###### 
            temp.data = comp1_mean[204:,:]
            binary = p_val_binary(full_fdr(p_val_cmp1), treshold = 0.05)
            fig = temp.plot_topomap(times = times_to_plot, average = average,
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = legend[0] + " fdr", colorbar = True,
                                vmax=p_mul, vmin=-p_mul, extrapolate="local",
                                mask = np.bool_(binary[204:,:]), units=units,
                                mask_params = dict(marker='o',
                                                   markerfacecolor='w', 
                                                   markeredgecolor='k',
                                                   linewidth=0,
                                                   markersize=7,
                                                   markeredgewidth=2))
            fig.savefig(os.path.join(output,
                                     comp_name,
                                     "cmp1_fdr.png"),
                        dpi = 300)
        
    
            plt.close()
        
        if "cmp2_nofdr" in topomaps:
            ##### CONDITION2 (no FDR) ######
            temp.data = comp2_mean[204:,:]
            binary = p_val_binary(p_val_cmp2, treshold = 0.05)
            fig = temp.plot_topomap(times = times_to_plot, average = average,
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = legend[1] + " nofdr", colorbar = True,
                                vmax=p_mul, vmin=-p_mul, extrapolate="local",
                                mask = np.bool_(binary[204:,:]), units=units,
                                mask_params = dict(marker='o',
                                                   markerfacecolor='w', 
                                                   markeredgecolor='k',
                                                   linewidth=0,
                                                   markersize=7,
                                                   markeredgewidth=2))
            fig.savefig(os.path.join(output,
                                     comp_name,
                                     "cmp2_nofdr.png"),
                        dpi = 300)
            plt.close()
        
        if "cmp2_fdr" in topomaps:
            ##### CONDITION2 (FDR) ######
            temp.data = comp2_mean[204:,:]
            binary = p_val_binary(full_fdr(p_val_cmp2), treshold = 0.05)
            fig = temp.plot_topomap(times = times_to_plot, average = average,
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = legend[1] + " fdr", colorbar = True, 
                                vmax=p_mul, vmin=-p_mul, extrapolate="local",
                                mask = np.bool_(binary[204:,:]), units =units,
                                mask_params = dict(marker='o',
                                                   markerfacecolor='w', 
                                                   markeredgecolor='k',
                                                   linewidth=0,
                                                   markersize=7,
                                                   markeredgewidth=2))
            fig.savefig(os.path.join(output,
                                     comp_name,
                                     "cmp2_fdr.png"),
                        dpi = 300)
        
            plt.close()
            
        if "dif_nofdr" in topomaps:
            ##### CONDITION2 - CONDITION1 with marks (no FDR) ######
            dif_title = legend[1] + " vs " + legend[0] + " nofdr"
            temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]
            binary = p_val_binary(p_val_dif, treshold = 0.05)
            fig = temp.plot_topomap(times = times_to_plot, average = average,
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = dif_title, colorbar = True, 
                                vmax=p_mul, vmin=-p_mul, extrapolate="local",
                                mask = np.bool_(binary[204:,:]), units=units,
                                mask_params = dict(marker='o',
                                                   markerfacecolor='w', 
                                                   markeredgecolor='k',
                                                   linewidth=0,
                                                   markersize=7,
                                                   markeredgewidth=2))
            fig.savefig(os.path.join(output,
                                     comp_name,
                                     "dif_nofdr.png"),
                        dpi = 300)
        
        
            plt.close()
           
        if "dif_fdr" in topomaps:
            ##### CONDITION2 - CONDITION1 with marks (FDR) ######
            dif_title = legend[1] + " vs " + legend[0] + " fdr"
            temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]
            binary = p_val_binary(full_fdr(p_val_dif), treshold = 0.05)
            fig = temp.plot_topomap(times = times_to_plot, average = average,
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = dif_title, colorbar = True, 
                                vmax=p_mul, vmin=-p_mul, extrapolate="local",
                                mask = np.bool_(binary[204:,:]), units=units,
                                mask_params = dict(marker='o',
                                                   markerfacecolor='w', 
                                                   markeredgecolor='k',
                                                   linewidth=0,
                                                   markersize=7,
                                                   markeredgewidth=2))
            fig.savefig(os.path.join(output,
                                     comp_name,
                                     "dif_fdr.png"),
                        dpi = 300)
            
            plt.close()
    
        if params[1][0][0] == "r":
            end = "reaction"
        else:
            end = "stimulus"
            
        
        pdf.multi_cell(w=0.0,
                       h=20,
                       txt = '''
{0} vs {1} p < 0.05 from {2}
tmin = {3}, tmax = {4}, tstep = {5}
fmin = {6}, fmax = {7}, fstep = {8}
Num of subj - {9}
                       '''.format(legend[1],
                       legend[0], end, tmin, tmax, tstep,
                       fmin, fmax, fstep, len(subjects)
                       ), border=1, align='L')
    
        y = 200
        for topo in topomaps:
            pic_file = os.path.join(output, comp_name, topo + ".png")
            pdf.image(pic_file, x=0, y=y, w=1200, h=0)
            y += 150
        
        pdf.output(os.path.join("all_pdf", comp_name + "pdf"))
        
 
