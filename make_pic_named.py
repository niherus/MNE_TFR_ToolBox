import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import pdfkit

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

def contr_num(filename):
    for ind, c in enumerate(contrast):
        if c in filename:
            return ind+1
    return None

def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

def get_short_legend(contrast):
    temp = contrast.split('_')
    return (temp[0], temp[2], temp[3], temp[4])

def get_full_legend(contrast):
    temp = contrast.split('_')
    return (diction[temp[0]], diction[temp[2]], diction[temp[3]], temp[4])

def delaete_bad_sub(contrast, del_list):
    for sub in del_list:
        if sub in contrast[1]:
            ind = contrast[1].index(sub)
            contrast[1].pop(ind)
            contrast[0] = np.delete(contrast[0], ind, axis=0)
    return contrast


def add_pic_html(filename, pic, pic_folder, pos_n, size):
    x = size[0]
    y = size[1]
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC=" ../output/%s" />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+pic))

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
    #plt.axvline(0, color = 'k', linewidth = 3, linestyle = '--', zorder = 1)
    #plt.axhline(0, color = 'k', linewidth = 1.5, zorder = 1)
    #plt.axvline(2.5, color = 'k', linewidth = 3, linestyle = '--', zorder = 1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label)
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = (p_val < 0.01), facecolor = 'm', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = ((p_val >= 0.01) * (p_val < 0.05)), facecolor = 'g', alpha = 0.46, step = 'pre')
    plt.tick_params(labelsize = 16)
    plt.legend(loc='upper right', fontsize = 16)
    plt.title(title, fontsize = 40)
    path = output + folder + '/'
    os.makedirs(path, exist_ok = True)
    plt.savefig(path+title + '.svg', transparent=True)
    plt.close()

config = pdfkit.configuration(wkhtmltopdf='D:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}

diction = {"w1c": "W1 (correct) (move)",
           "w2c": "W2 (correct) (move)",
           "w1em": "W1 (error) (move)",
           "w1eo": "W1 (error) (no move)",
           "d1cr": "D1 (correct) (no move)",
           "d2cr": "D2 (correct) (no move)",
           "d1fa": "D1 (error) (move)",
           "s1em": "S1 (error) (move)",
           "s1c": "S1 (correct) (move/nomove)",
           "s2c": "S2 (correct) (move/nomove)",
           'wlh2c': "active2 hicha correct move",
           'wrh2c': "active2 hivu correct move",
           'wlh1c': "active1 hicha correct move",
           'wrh1c': "active1 hivu correct move",
           "stim": "from stimulus",
           "react": "from reaction",
           "fb": "from feedback",
           "all": "from stimulus (all)"
           }

contrast = [
    'w1c_vs_d1fa',
    'w2c_vs_d2cr',
    'w1c_vs_w2c',
    'd1cr_vs_d2cr',
    'w1c_vs_d1cr',
    'w1em_vs_w1eo',
    'd1fa_vs_d1cr',
    'w1c_vs_w1em',
    # 'w1c_vs_s1c',
    'w1c_vs_s1em',
    'wlh2c_vs_wrh2c',
    'wlh1c_vs_wrh2c_stim'
    ]

planars = ['planar1', 'planar2', 'combine_planar']

output = 'output/'
rewrite = True
os.makedirs(output, exist_ok=True)

pos = io.loadmat('pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat('channel_labels.mat')['chanlabels'])
session = ["active1-st", "active2-end"]
stim = ["react"]

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

path = os.getcwd()
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

comp1 = contr[:, 0, :, 200:-200]
comp2 = contr[:, 1, :, 200:-200]

t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)

comp1_mean = comp1.mean(axis=0)
comp2_mean = comp2.mean(axis=0)

p_mul = 0.3

if False:
    time = np.arange(-0.5, 0.05*(comp1_mean.shape[1])-0.5, 0.05)
    print(time.shape)
    print(comp1_mean.shape)
else:
    time = temp1.times[200:-200] - 2
    print(time.shape)
    print(comp1_mean.shape)
if rewrite:
    for indx in range(comp1_mean.shape[0]):
        if indx < 204:
            p_mul = 0.3
        else:
            p_mul = 1.6
        plot_stat_comparison(comp1_mean[indx], comp2_mean[indx], p_val[indx], p_mul, time, title = chan_labels[indx],
                             folder = "w1_vs_w2_end", comp1_label = "w1c", comp2_label = "w2c_end")

    print('\tPictures generated')
else:
    print('\tPictures uploaded')

for ind, planar in enumerate(planars):
    html_name = 'html_plots/pic_compose_n2_%s_%s_vs_%s_%s_%s.html' % (planar, "w1", "w2_end", "all", "soft-balanced")
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:32px;"><b> %s, active,average beta 15-25 <span style="color:green;"> 0.01 < p <= 0.05 </span> <span style="color:Magenta;">p <= 0.01 </span> </b></p>' % (planar))
    title = ["W1 (correct) (move)", "W2 (correct) (move) _end"]
    add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (title[0], title[1]))
    title = ["from reaction ", "soft-balanced"]
    add_str_html(html_name, '<p style="font-size:32px;color:Maroon;"><b> %s %s </b></p>' % (title[0], title[1]))
    add_str_html(html_name, '<h1 style="font-size:32px;"><b> %s participants </b></h1>' % (contr.shape[0]))
    add_str_html(html_name, '<h1 style="font-size:48px;"><b> (%s) </b></h1>' % 3)
    if ind == 2:
        for ch_num in range(204, len(chan_labels)):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_html(html_name, pic, "w1_vs_w2_end", pos[ch_num], [200,150])
    else:
        for ch_num in range(ind, 204, 2):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_html(html_name, pic,  "w1_vs_w2_end", pos[ch_num], [200,150])

    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdf_file = html_name.split("/")[1].split('.')[0]
    print(os.getcwd() + '/%s' % html_name)
    pdfkit.from_file(os.getcwd() + '/%s' % html_name, 'all_pdf/%s.pdf' % pdf_file, configuration = config, options=options)
print('\tAll printed')

