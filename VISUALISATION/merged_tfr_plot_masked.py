import mne
import numpy as np
from scipy import stats
import statsmodels.stats.multitest as mul
import matplotlib.pyplot as plt
import os

print(mne.__version__)
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



data1 = np.zeros((len(subjects), *mne.time_frequency.read_tfrs(f'{subjects[0]}_{session[0]}_react_merged_channels-tfr.h5', condition=None)[0].crop(tmin=-1.0, tmax=1.4, fmin=2.0, fmax=40.0).data.shape))
data2 = np.zeros((len(subjects), *mne.time_frequency.read_tfrs(f'{subjects[0]}_{session[1]}_react_merged_channels-tfr.h5', condition=None)[0].crop(tmin=-1.0, tmax=1.4, fmin=2.0, fmax=40.0).data.shape))

for i, sub in enumerate(subjects):
    print(sub)
    data1[i, :, :] = mne.time_frequency.read_tfrs(f'{sub}_{session[0]}_react_merged_channels-tfr.h5', condition=None)[0].crop(tmin=-1.0, tmax=1.4, fmin=2.0, fmax=40.0).data
    data2[i, :, :] = mne.time_frequency.read_tfrs(f'{sub}_{session[1]}_react_merged_channels-tfr.h5', condition=None)[0].crop(tmin=-1.0, tmax=1.4, fmin=2.0, fmax=40.0).data
donor = mne.time_frequency.read_tfrs(f'{subjects[0]}_{session[0]}_react_merged_channels-tfr.h5', condition=None)[0].crop(tmin=-1.0, tmax=1.4, fmin=2.0, fmax=40.0)
#donor.data = data2.mean(axis=0) - data1.mean(axis=0)
donor.data = data1.mean(axis=0)
thres = 0.05
#data2 = data2.mean(axis=-1)
#data1 = data1.mean(axis=-1)

data = data2 - data1
t_stat, p_val = stats.ttest_1samp(data1, popmean=0, axis=0)
#t_stat, p_val = stats.ttest_rel(data2, data1, axis=0)
_, width, height = p_val.shape

print(p_val)


p_val_resh = p_val.reshape((width * height))
print(p_val_resh.shape)
_, p_val_fdr = mul.fdrcorrection(p_val_resh, alpha=thres)
#_, p_val_fdr = mul.fdrcorrection(p_val_fdr, alpha=thres)
#p_val_fdr = p_val_fdr.reshape((width, height))
print(p_val_fdr)
p_mul = 0.1
'''
plt.title("merged grads, spectr", fontsize = 25)
plt.ylim(-p_mul, p_mul)
plt.plot(donor.freqs, (data).mean(axis=0).reshape((width * height)), color = "r", label = "active2-end vs active1-st")
plt.plot(donor.freqs, (data1).mean(axis=0).reshape((width * height)), color = "g", label = "active1-st")
plt.plot(donor.freqs, (data2).mean(axis=0).reshape((width * height)), color = "b", label = "active2-end")
plt.legend(loc='lower right', fontsize = 12)
plt.fill_between(donor.freqs, y1 = p_mul, y2 = -p_mul, where = p_val_fdr < 0.05, facecolor = 'g', alpha = 0.46, step = 'pre')
plt.show()
print(donor.freqs[p_val_fdr < thres].min())
print(donor.freqs[p_val_fdr < thres].max())
'''
#_, p_val_fdr = mul.fdrcorrection(p_val_resh, alpha=thres)
p_val = p_val_fdr.reshape((width, height))
p_val = p_val.reshape((width, height))

fig = donor.plot(picks=donor.ch_names[0], tmin=-1.0, tmax=1.4, vmin=-0.2, vmax=0.2, show=False, mask=p_val < thres, mask_style='contour')[0]
print(fig)

fig.savefig(os.path.join("merged_channels",f"active1-st_react_fdr_contour_{thres}.png"))
plt.close()
