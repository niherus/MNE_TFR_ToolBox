import sys
import os
import numpy as np
import mne
import time

data_dir = 'G:\\MEG_data\\ttest_res\\words_distr_pas1_vs_pas2\\p-val\\'
views = ['med','lat']
hemies = ["lh", "rh"]
os.environ["SUBJECTS_DIR"] = 'D:\\beta_data\\stc_look\\freesurfer\\'


folders = ["p-val_w1_w2", "p-val_w1_w2-end", "p-val_d1_d2", "p-val_d1_d2-end"]
for folder in folders:
    print(folder)
    os.makedirs(os.path.join(os.getcwd(),folder), exist_ok = True)

    stc = mne.read_source_estimate(os.path.join(os.getcwd(), "%s_sub23_integ50-lh.stc" % (folder)))

    stc.subject = 'avg_platon_27sub'
    st = np.where(np.isclose(stc.times, 0))[0][0]
    end = np.where(np.isclose(stc.times, 5))[0][0]
    stc.data *= 100
    times = np.arange(st,end,2)

    for view in views:
        for hemi in hemies:

            brain = stc.plot(hemi = hemi, background = "white", title=f"{hemi} {view}",foreground = "black", time_viewer = False, cortex = 'bone', clim = {"kind": "value", "pos_lims": (95.0,99.9,100.6)})
            brain.save_image_sequence(fname_pattern = "{0}\\{1}_{2}_%0.4d.png".format(folder, hemi, view), time_idx = times, montage=view)

            brain.close()
            del brain

