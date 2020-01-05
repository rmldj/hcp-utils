import nibabel as nib
import numpy as np

rsn = nib.load('../source_data/RSN.dlabel.nii')

#print(rsn.shape)

rois = rsn.get_fdata().astype(int)

# for i in range(4):
#     print(i, np.unique(rois[i]))

vertex_data = np.load('../data/fMRI_vertex_info_32k.npz')
grayl = vertex_data['grayl']
grayr = vertex_data['grayr']

cortex_left_=slice(0,29696)
cortex_right_=slice(29696,59412)


 
# Yeo 7-network parcellation

yeo7lv=rois[0,:32492]
yeo7rv=rois[0,32492:]

yeo7 = np.zeros(91282, dtype=int)
yeo7l = yeo7[cortex_left_]
yeo7r = yeo7[cortex_right_]

yeo7l[:] = yeo7lv[grayl]
yeo7r[:] = yeo7rv[grayr]

#print(np.unique(yeo7l))
#print(np.unique(yeo7r))

mapyeo7=dict()
mapyeo7[37]=0
mapyeo7[41]=1
mapyeo7[43]=2
mapyeo7[38]=3
mapyeo7[44]=4
mapyeo7[42]=5
mapyeo7[39]=6
mapyeo7[40]=7

for v in mapyeo7:
    yeo7[yeo7==v]=mapyeo7[v]

#print(np.unique(yeo7))

labels = ['', 'Visual', 'Somatomotor', 'Dorsal Attention', 'Ventral Attention', 'Limbic', 'Frontoparietal', 'Default']

axis0=rsn.header.get_index_map(0)
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

np.savez_compressed('../data/yeo7.npz', map_all=yeo7, labels=labels, rgba=rgba, ids=keys)


# Yeo 17-network parcellation

yeo17lv=rois[1,:32492]
yeo17rv=rois[1,32492:]

yeo17 = np.zeros(91282, dtype=int)
yeo17l = yeo17[cortex_left_]
yeo17r = yeo17[cortex_right_]

yeo17l[:] = yeo17lv[grayl]
yeo17r[:] = yeo17rv[grayr]

#print(np.unique(yeo17l))
#print(np.unique(yeo17r))

mapyeo17=dict()
mapyeo17[37]=0
mapyeo17[54]=1
mapyeo17[45]=2
mapyeo17[58]=3
mapyeo17[55]=4
mapyeo17[50]=5
mapyeo17[47]=6
mapyeo17[60]=7
mapyeo17[59]=8
mapyeo17[56]=9
mapyeo17[49]=10
mapyeo17[57]=11
mapyeo17[48]=12
mapyeo17[51]=13
mapyeo17[61]=14
mapyeo17[53]=15
mapyeo17[46]=16
mapyeo17[52]=17

for v in mapyeo17:
    yeo17[yeo17==v]=mapyeo17[v]

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

np.savez_compressed('../data/yeo17.npz', map_all=yeo17, labels=labels, rgba=rgba, ids=keys)
