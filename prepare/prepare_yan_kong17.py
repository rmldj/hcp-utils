import numpy as np
import scipy.io
import nibabel as nib

# define the resolution of the parcellation
# parcellation files are taken from https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Yan2023_homotopic
parcels = 1000
yan_kong17 = nib.load(f'../source_data/{parcels}Parcels_Kong2022_17Networks.dlabel.nii')

# rois of grayordinates in the cortex
rois = yan_kong17.dataobj[0].astype(int)

# define a medial wall mask for fsLR
# the mask file is taken from https://github.com/ThomasYeoLab/CBIG/blob/master/stable_projects/brain_parcellation/Kong2019_MSHBM/lib/fs_LR_32k_medial_mask.mat
mat = scipy.io.loadmat('../source_data/fs_LR_32k_medial_mask.mat')
mask = mat['medial_mask']
rois = rois[np.where(mask!=0)[0]]

# extract parcel names and colors
axis0=yan_kong17.header.get_index_map(0)
nmap=list(axis0.named_maps)[0]

keys = [0]
labels = ['']
rgba = [(0.0, 0.0, 0.0, 0.0)]

for i in range(1, parcels+1):
    roi = nmap.label_table[i]
    labels.append(roi.label[11:])
    rgba.append((roi.red, roi.green, roi.blue, roi.alpha))
    keys.append(i)

# extend the cortical parcellation by the standard subcortical structures from CIFTI-2
map_all = np.zeros(91282, dtype=int)
map_all[:59412] = rois

accumbens_left_=slice(59412,59547)
accumbens_right_=slice(59547,59687)
amygdala_left_=slice(59687,60002)
amygdala_right_=slice(60002,60334)
brainStem_=slice(60334,63806)
caudate_left_=slice(63806,64534)
caudate_right_=slice(64534,65289)
cerebellum_left_=slice(65289,73998)
cerebellum_right_=slice(73998,83142)
diencephalon_left_=slice(83142,83848)
diencephalon_right_=slice(83848,84560)
hippocampus_left_=slice(84560,85324)
hippocampus_right_=slice(85324,86119)
pallidum_left_=slice(86119,86416)
pallidum_right_=slice(86416,86676)
putamen_left_=slice(86676,87736)
putamen_right_=slice(87736,88746)
thalamus_left_=slice(88746,90034)
thalamus_right_=slice(90034,None)

structures_subcortical=[accumbens_left_, accumbens_right_, amygdala_left_, amygdala_right_,
                        caudate_left_, caudate_right_, cerebellum_left_, cerebellum_right_, diencephalon_left_, diencephalon_right_,
                        hippocampus_left_, hippocampus_right_, pallidum_left_, pallidum_right_, putamen_left_, putamen_right_,
                        thalamus_left_, thalamus_right_, brainStem_]

names_subcortical=['accumbens_left', 'accumbens_right', 'amygdala_left', 'amygdala_right',
                   'caudate_left', 'caudate_right', 'cerebellum_left', 'cerebellum_right', 'diencephalon_left', 'diencephalon_right',
                   'hippocampus_left', 'hippocampus_right', 'pallidum_left', 'pallidum_right', 'putamen_left', 'putamen_right',
                   'thalamus_left', 'thalamus_right', 'brainStem']

num_subcortical = len(structures_subcortical)

for i in range(num_subcortical):
    struct = structures_subcortical[i]
    name = names_subcortical[i]
    map_all[struct] = int(parcels+1) + i
    keys.append(int(parcels+1) + i)

labels.extend(names_subcortical)

# assign black color for subcortical parts
rgba_sc = np.zeros((num_subcortical, 4))

labels = np.array(labels)
rgba = np.vstack((np.array(rgba), rgba_sc))
keys = np.array(keys)

# save parcellation
np.savez_compressed(f'../hcp-utils/data/yan_kong17_{parcels}parcels.npz', map_all=map_all, labels=labels, rgba=rgba, ids=keys)