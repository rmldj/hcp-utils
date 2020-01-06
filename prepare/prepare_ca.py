import nibabel as nib
import numpy as np

ca_net = nib.load('../source_data/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_netassignments_LR.dlabel.nii')

# rois of grayordinates in the cortex

rois = ca_net.dataobj[0].astype(int)

axis0 = ca_net.header.get_index_map(0)
nmap = list(axis0.named_maps)[0]

labels = []
rgba = []
keys = []

# left hemisphere
for i in nmap.label_table:
    roi = nmap.label_table[i]
    labels.append(roi.label[:-4])
    keys.append(roi.key)
    rgba.append((roi.red, roi.green, roi.blue, roi.alpha))

# replace shorthand labels by full names from ColeAnticevicNetPartition/network_labelfile.txt
labels = ['', 'Visual1', 'Visual2', 'Somatomotor', 'Cingulo-Opercular', 'Dorsal-attention', 'Language', 'Frontoparietal', 'Auditory', 'Default', 'Posterior-Multimodal', 'Ventral-Multimodal', 'Orbito-Affective']

labels = np.array(labels)
rgba = np.array(rgba)
keys = np.array(keys)

np.savez_compressed('../hcp-utils/data/ca_network_1.1.npz', map_all=rois, labels=labels, rgba=rgba, ids=keys)

#print(np.unique(rois))

ca_parcels = nib.load('../source_data/CortexSubcortex_ColeAnticevic_NetPartition_wSubcorGSR_parcels_LR.dlabel.nii')

# rois of grayordinates in the cortex

rois = ca_parcels.dataobj[0].astype(int)

axis0 = ca_parcels.header.get_index_map(0)
nmap = list(axis0.named_maps)[0]

labels = []
rgba = []
keys = []

# left hemisphere
for i in nmap.label_table:
    roi = nmap.label_table[i]
    labels.append(roi.label)
    keys.append(roi.key)
    rgba.append((roi.red, roi.green, roi.blue, roi.alpha))

#print(labels)
#print()
#print(rgba)
#print()

#print(np.unique(rois))
#print(len(rois))

labels = np.array(labels)
rgba = np.array(rgba)
keys = np.array(keys)

np.savez_compressed('../hcp-utils/data/ca_parcels_1.1.npz', map_all=rois, labels=labels, rgba=rgba, ids=keys)
