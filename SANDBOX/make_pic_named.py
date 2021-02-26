# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 20:46:42 2021

@author: Admin
"""


import mne
from mne import set_config
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
from fpdf import FPDF
from configure import comparisons,\
    data_path, file_format, subjects,\
        tmin, tmax, tstep,\
            fmin, fmax, fstep,\
                average, p_mul, units
                
set_config("MNE_MEMMAP_MIN_SIZE", "1M")
set_config("MNE_CACHE_DIR", ".tmp")

mne.set_log_level("ERROR")  

def generate_legend(comp_name):
    params = comparisons[comp_name]
    
    if params[0][0] != params[0][1]:
        return params[0]
    else:
        return params[1]

def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

def generate_array(comp_name, tmin = None, tmax = None):
    params = comparisons[comp_name]
    
    test = mne.Evoked(os.path.join(data_path, 
                            file_format.format(subjects[0],
                                               params[0][0], 
                                               params[1][0])))
    test.shift_time(-2.0)
    test = test.crop(tmin, tmax)
    return np.zeros((len(subjects), 2, *test.data.shape))



def plot_stat_comparison(comp1, comp2, p_val, p_mul, time, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2'):
    assert(len(comp1) == len(comp2) == len(time))
    plt.figure()
    plt.rcParams['axes.facecolor'] = 'none'
    plt.xlim(time[0], time[-1])
    plt.ylim(-p_mul, p_mul)
    plt.plot([0, 0.001], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([-6, 6], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([2.6, 2.601], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label)
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = (p_val < 0.01), facecolor = 'm', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = ((p_val >= 0.01) * (p_val < 0.05)), facecolor = 'g', alpha = 0.46, step = 'pre')
    plt.xticks(ticks=np.arange(int(time[0]), time[-1], 0.5))
    plt.tick_params(labelsize = 25)
    plt.legend(loc='upper right', fontsize = 16)
    plt.title(title, fontsize = 30)
    path = output + folder + '/'
    os.makedirs(path, exist_ok = True)
    plt.savefig(path+title + '.png', dpi=50, transparent=True)
    plt.close()

planars = ['planar1', 'planar2', 'combine_planar']

output = 'output/'
rewrite = True
os.makedirs(output, exist_ok=True)

pos = io.loadmat('pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat('channel_labels.mat')['chanlabels'])

for folder in comparisons.keys():

    os.makedirs(os.path.join(output, folder), exist_ok=True)    



for comp_name in comparisons.keys():
    print(comp_name, "started")
    pdf = FPDF(orientation="L", unit="pt", format="A3")
    pdf.set_font("Times", size = 14)
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

    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)

    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)

    
    for indx in range(comp1_mean.shape[0]):
        if indx < 204:
            p_mul_in_data = 2.4/2
        else:
            p_mul_in_data = 2.5
        plot_stat_comparison(comp1_mean[indx], comp2_mean[indx], p_val[indx], 
                        p_mul_in_data, temp.times, title = chan_labels[indx],
                        folder = comp_name, comp1_label = legend[0], 
                        comp2_label = legend[1])

    if params[1][0][0] == "r":
        end = "reaction"
    else:
        end = "stimulus"

    for ind, planar in enumerate(planars):
        print(planar, "printed")
        pdf.add_page()
        pdf.multi_cell(w=0.0,
                       h=15,
                       txt = '''
    Planar: {0}
    {1} vs {2} from {3}
    tmin = {4}, tmax = {5}, tstep = {6}
    fmin = {7}, fmax = {8}, fstep = {9}
    0.01 < p_val <= 0.05 - green
    p_val <= 0.01 - magenta
    Num of subj - {10}
                       '''.format(planar, legend[1],
                       legend[0], end, tmin, tmax, tstep,
                       fmin, fmax, fstep, len(subjects)
                       ), border=0, align='L')
    

        if ind == 2:
            for ch_num in range(204, len(chan_labels)):
                ww = 70
                hh = ww * 3 // 4
                x = round(pos[ch_num][0] * ww * 15, 3)
                y = 10 + round((1 - pos[ch_num][1]) * hh * 15, 3)
                
                pic_file = os.path.join(output, comp_name, chan_labels[ch_num] + '.png')
                pdf.image(pic_file, x=x, y=y, w=ww, h=0)

        else:
            for ch_num in range(ind, 204, 2):
                ww = 70
                hh = ww * 3 // 4
                x = round(pos[ch_num][0] * ww * 15, 3)
                y = 10 + round((1 - pos[ch_num][1]) * hh * 15, 3)
                
                pic_file = os.path.join(output, comp_name, chan_labels[ch_num] + '.png')
                pdf.image(pic_file, x=x, y=y, w=ww, h=0)

    pdf.output(os.path.join("all_pdf", "timecourse_" + comp_name + ".pdf"))
    pdf.close()

print('\tAll printed')

