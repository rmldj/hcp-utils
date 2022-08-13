import nibabel as nib
import numpy as np

#rsn = nib.load('../source_data/RSN.dlabel.nii')
dlab = nib.load('../source_data/Schaefer2018_100Parcels_7Networks_order.dlabel.nii')

#print(rsn.shape)
rois = dlab.get_fdata().astype(int)

vertex_data = np.load('../hcp_utils/data/fMRI_vertex_info_32k.npz')
grayl = vertex_data['grayl']
grayr = vertex_data['grayr']

cortex_left_=slice(0,29696)
cortex_right_=slice(29696,59412)


# Schaefer parcellation

sch100lv=rois[0,:32492]
sch100rv=rois[0,32492:]

sch100 = np.zeros(91282, dtype=int)
sch100l = sch100[cortex_left_]
sch100r = sch100[cortex_right_]

sch100l[:] = sch100lv[grayl]
sch100r[:] = sch100rv[grayr]


ax0 = dlab.header.get_axis(0)
keys = list(ax0.label[0].keys())
vals = list(ax0.label[0].values())
labels = np.array([v[0] for v in vals])
rgba = [v[1][1:] for v in vals]
#rgba = [v[1][1:] for v in vals


np.savez_compressed('../hcp_utils/data/sch100.npz', map_all=sch100, labels=labels, rgba=rgba, ids=keys)
