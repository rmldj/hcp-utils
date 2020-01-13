from nilearn import surface
import numpy as np
from scipy.sparse import csr_matrix, save_npz
from scipy.sparse.csgraph import connected_components

coordl, facesl = surface.load_surf_mesh('../hcp_utils/data/S1200.L.pial_MSMAll.32k_fs_LR.surf.gii')
coordr, facesr = surface.load_surf_mesh('../hcp_utils/data/S1200.R.pial_MSMAll.32k_fs_LR.surf.gii')

faces = np.vstack((facesl, facesr+len(coordl)))

vertex_data = np.load('../hcp_utils/data/fMRI_vertex_info_32k.npz')

grayl = vertex_data['grayl']
grayr = vertex_data['grayr']

gray = np.hstack((grayl, grayr + len(coordl)))

print(len(gray), np.amax(gray))

gray_vertex = dict()

for i, g in enumerate(gray):
    gray_vertex[g] = i


print()
print(gray_vertex[180], gray_vertex[235], gray_vertex[12])

nv = len(grayl) + len(grayr)

def adjacency1(triangles, nv=nv):
    # standard adjacency matrix containing all edges between cortical grayordinates
	
    adj_rows = []
    adj_cols = []
    dist = []

    used=set()
    for i1,i2,i3 in triangles:
        for p in [(i1,i2), (i2,i1), (i1,i3), (i3,i1), (i2,i3), (i3,i2)]:
            if p in used:
                continue
            i,j=p

            if i in gray_vertex and j in gray_vertex:
                adj_rows.append(gray_vertex[i])
                adj_cols.append(gray_vertex[j])
                dist.append(1)
            used.add(p)
        
    adj=csr_matrix((dist, (adj_rows, adj_cols)), shape=(nv,nv), dtype=int)
    return adj	


adj1 = adjacency1(faces)


print(94, adj1.getrow(94)) # 11, 12, 20, 21, 95, 102
print(21, adj1.getrow(21)) # should contain 20, 94, 102 but not 11 and 95

#print(21, adj2.getrow(21)) # should contain 20, 94, 102 and 11 and 95

n_components, labels = connected_components(adj1, directed=False)
print(len(grayl), len(grayr))
print(n_components, np.unique(labels, return_counts=True)) # one should get 2 components: left and right cortex

save_npz('../hcp_utils/data/cortical_adjacency.npz', adj1)
