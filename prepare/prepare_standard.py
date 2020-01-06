import nibabel as nib
import numpy as np


map_all = np.zeros(91282, dtype=int)

cortex_left_=slice(0,29696)
cortex_right_=slice(29696,59412)

keys = [0, 1, 2]
labels = ['', 'cortex_left', 'cortex_right']
rgba = [(1.0, 1.0, 1.0, 1.0), (0.87, 0.09, 0.16, 1.0), (0.92, 0.12, 0.18, 1.0)]

map_all[cortex_left_] = 1
map_all[cortex_right_] = 2

# extend the cortical parcellation by the standard subcortical structures from CIFTI-2


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
    map_all[struct] = 361 + i
    keys.append(361 + i)

labels.extend(names_subcortical)

# random colors for subcortical parts
np.random.seed(555)
colors2 = np.random.uniform(size=((num_subcortical-1)//2, 4))
colors1 = 0.8 * colors2

rgba_sc = np.zeros((num_subcortical, 4))
rgba_sc[:-1][::2] = colors1
rgba_sc[1::2] = colors2
rgba_sc[:,3] = 1.0 


labels = np.array(labels)
rgba = np.vstack((np.array(rgba), rgba_sc))
keys = np.array(keys)


np.savez_compressed('../hcp-utils/data/standard.npz', map_all=map_all, labels=labels, rgba=rgba, ids=keys)

