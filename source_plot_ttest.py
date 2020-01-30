import os
import mne
import numpy as np
from scipy import stats

mimi = 1
def signed_p_val(t, p_val):

   if t >= 0:
      return 1 - p_val
   else:
      return -(1 - p_val)


vect_signed_p_val = np.vectorize(signed_p_val)

data_dir = os.getcwd()

session = ["active1", "active2-end"]
stim = ["word", "dist"]
ttest_result_file = '{0}_{1}_sub23_integ50'
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

stc_test = mne.read_source_estimate(os.path.join(data_dir, "394_tiev_active2_word_int_50ms-rh.stc"))
stc_test.resample(20)

comp1_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
comp2_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))

for ind, subj in enumerate(subjects):
    print(ind + 1, subj)
    temp1 = mne.read_source_estimate(os.path.join(os.getcwd(), "{0}_{1}_{2}_int_50ms-lh.stc".format(subj, session[0], stim[0])))
    temp1.resample(20)
    comp1_per_sub[ind, :, :] = temp1.data
    temp2 = mne.read_source_estimate(os.path.join(os.getcwd(), "{0}_{1}_{2}_int_50ms-lh.stc".format(subj, session[1], stim[0])))
    temp2.resample(20)
    comp2_per_sub[ind, :, :] = temp2.data
    

print("calculation ttest")
    
t_stat, p_val = stats.ttest_rel(comp2_per_sub, comp1_per_sub, axis=0)
print(p_val.min(), p_val.mean(), p_val.max())
print(t_stat.min(), t_stat.mean(), t_stat.max())
p_val = vect_signed_p_val(t_stat, p_val)
print("Hello mother fucker", mimi)
print("calculation complited")
p_val_stc = mne.SourceEstimate(data = p_val, vertices = stc_test.vertices  ,  tmin = stc_test.tmin, tstep = stc_test.tstep)
print(p_val_stc.data.min(), p_val_stc.data.mean(), p_val_stc.data.max())
print("Brain's rendering")
#os.environ["SUBJECTS_DIR"] = 'D:\\beta_data\\stc_beta\\freesurfer\\'
p_val_stc.subject = 'avg_platon_27sub'
p_val_stc.save(ttest_result_file.format("p-val","w1_w2-end"))
'''
brain = p_val_stc.plot(hemi = 'both', time_viewer = True, cortex = 'bone', clim={"kind":"value", "pos_lims":(0.9, 0.95,1)} )

for ind, subj in enumerate(subjects):
    

views = ['med','lat']
stc = mne.read_source_estimate(data_dir + cur_stc)

os.environ["SUBJECTS_DIR"] = 'D:\\beta_data\\stc_beta\\freesurfer\\'
stc.subject = 'avg_platon_27sub'



brain = stc.plot(hemi = 'both', time_viewer = True, cortex = 'bone')
'''
