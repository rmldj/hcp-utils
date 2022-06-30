import nibabel as nib
import numpy as np

#rsn = nib.load('../source_data/RSN.dlabel.nii')
dlab = nib.load('../source_data/Schaefer2018_100Parcels_7Networks_order.dlabel.nii')


#print(rsn.shape)
rois = dlab.get_fdata().astype(int)

# for i in range(4):
#     print(i, np.unique(rois[i]))

vertex_data = np.load('../hcp_utils/data/fMRI_vertex_info_32k.npz')
grayl = vertex_data['grayl']
grayr = vertex_data['grayr']

cortex_left_=slice(0,29696)
cortex_right_=slice(29696,59412)


 
# Yeo 7-network parcellation

sch100lv=rois[0,:32492]
sch100rv=rois[0,32492:]

sch100 = np.zeros(91282, dtype=int)
sch100l = sch100[cortex_left_]
sch100r = sch100[cortex_right_]

sch100l[:] = sch100lv[grayl]
sch100r[:] = sch100rv[grayr]

#print(np.unique(yeo7l))
#print(np.unique(yeo7r))

mapsch100=dict()
mapsch100[37]=0
mapsch100[41]=1
mapsch100[43]=2
mapsch100[38]=3
mapsch100[44]=4
mapsch100[42]=5
mapsch100[39]=6
mapsch100[40]=7

for v in mapsch100:
    sch100[sch100==v]=mapsch100[v]

#print(np.unique(yeo7))

labels = ['', 'Visual', 'Somatomotor', 'Dorsal Attention', 'Ventral Attention', 'Limbic', 'Frontoparietal', 'Default']

axis0=dlab.header.get_index_map(0)
nmap=list(axis0.named_maps)[0]

rgba = [(1.0,1.0,1.0,1.0)]

for i in [41, 43, 38, 44, 42, 39, 40]:
    lab=nmap.label_table[i]
    rgba.append((lab.red, lab.green, lab.blue, 1.0))

labels = np.array(labels)
rgba = np.array(rgba)
keys = np.arange(8)

#print(labels)
#print(rgba)

np.savez_compressed('../hcp_utils/data/sch100.npz', map_all=sch100, labels=labels, rgba=rgba, ids=keys)


"""

# Yeo 17-network parcellation

sch100lv=rois[1,:32492]
sch100rv=rois[1,32492:]

sch100 = np.zeros(91282, dtype=int)
sch100l = sch100[cortex_left_]
sch100r = sch100[cortex_right_]

sch100l[:] = sch100lv[grayl]
sch100r[:] = sch100rv[grayr]

#print(np.unique(yeo17l))
#print(np.unique(yeo17r))

mapsch100=dict()
mapsch100[37]=0
mapsch100[54]=1
mapsch100[45]=2
mapsch100[58]=3
mapsch100[55]=4
mapsch100[50]=5
mapsch100[47]=6
mapsch100[60]=7 
mapsch100[59]=8 
mapsch100[56]=9
mapsch100[49]=10
mapsch100[57]=11
mapsch100[48]=12
mapsch100[51]=13
mapsch100[61]=14
mapsch100[53]=15
mapsch100=16
mapsch100[52]=17

for v in mapsch100:
    sch100[sch100==v]=sch100[v]


#print(np.unique(yeo17))

labels = [''] + ['network_{}'.format(i) for i in range(1,18)]

axis0=rsn.header.get_index_map(0)
nmap=list(axis0.named_maps)[0]

rgba = [(1.0,1.0,1.0,1.0)]

for i in [54, 45, 58, 55, 50, 47, 60, 59, 56, 49, 57, 48, 51, 61, 53, 46, 52]:
    lab=nmap.label_table[i]
    rgba.append((lab.red, lab.green, lab.blue, 1.0))

labels = np.array(labels)
rgba = np.array(rgba)
keys = np.arange(18)

#print(labels)
#print(rgba)

np.savez_compressed('../hcp-utils/data/sch100.npz', map_all=sch100, labels=labels, rgba=rgba, ids=keys)

""";


