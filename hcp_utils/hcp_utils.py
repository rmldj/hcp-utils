import nibabel as nib
from nilearn import surface
from nilearn import plotting
from sklearn.utils import Bunch
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from scipy.sparse import load_npz
from scipy.sparse.csgraph import connected_components
import os
import re
from pathlib import Path

# define standard structures (for 3T HCP-like data)

struct = Bunch()

struct.cortex_left = slice(0,29696)
struct.cortex_right = slice(29696,59412)
struct.cortex = slice(0,59412)
struct.subcortical = slice(59412,None)

struct.accumbens_left = slice(59412,59547)
struct.accumbens_right = slice(59547,59687)
struct.amygdala_left = slice(59687,60002)
struct.amygdala_right = slice(60002,60334)
struct.brainStem = slice(60334,63806)
struct.caudate_left = slice(63806,64534)
struct.caudate_right = slice(64534,65289)
struct.cerebellum_left = slice(65289,73998)
struct.cerebellum_right = slice(73998,83142)
struct.diencephalon_left = slice(83142,83848)
struct.diencephalon_right = slice(83848,84560)
struct.hippocampus_left = slice(84560,85324)
struct.hippocampus_right = slice(85324,86119)
struct.pallidum_left = slice(86119,86416)
struct.pallidum_right = slice(86416,86676)
struct.putamen_left = slice(86676,87736)
struct.putamen_right = slice(87736,88746)
struct.thalamus_left = slice(88746,90034)
struct.thalamus_right = slice(90034,None)

# The fMRI data are not defined on all 32492 vertices of the 32k surface meshes
# Hence we need to record what is the mapping between the cortex grayordinates from fMRI
# and the vertices of the 32k surface meshes.
# This information is kept in vertex_info
#
# for a standard 3T HCP style fMRI image get_HCP_vertex_info(img) should coincide with vertex_info


def _make_vertex_info(grayl, grayr, num_meshl, num_meshr):
    vertex_info = Bunch()
    vertex_info.grayl = grayl
    vertex_info.grayr = grayr
    vertex_info.num_meshl = num_meshl
    vertex_info.num_meshr = num_meshr
    return vertex_info

PKGDATA = Path(__file__).parent / 'data'

vertex_data = np.load(PKGDATA / 'fMRI_vertex_info_32k.npz')
vertex_info = _make_vertex_info(vertex_data['grayl'], vertex_data['grayr'], int(vertex_data['num_meshl']), int(vertex_data['num_meshr']))

def get_HCP_vertex_info(img):
    """
    Extracts information about the relation of indices in the fMRI data to the surface meshes and the left/right cortex.
    Use only for meshes different from the 32k standard one which is loaded by default.
    """
    assert isinstance(img, nib.cifti2.cifti2.Cifti2Image)
    
    map1 = img.header.get_index_map(1)
    bms = list(map1.brain_models)

    grayl = np.array(bms[0].vertex_indices)
    grayr = np.array(bms[1].vertex_indices)
    num_meshl = bms[0].surface_number_of_vertices
    num_meshr = bms[1].surface_number_of_vertices
    return _make_vertex_info(grayl, grayr, num_meshl, num_meshr)


# The following three functions take a 1D array of fMRI grayordinates
# and return the array on the left- right- or both surface meshes

def left_cortex_data(arr, fill=0, vertex_info=vertex_info):
    """
    Takes a 1D array of fMRI grayordinates and returns the values on the vertices of the left cortex mesh which is neccessary for surface visualization. 
    The unused vertices are filled with a constant (zero by default). 
    """
    out = np.zeros(vertex_info.num_meshl)
    out[:] = fill
    out[vertex_info.grayl] = arr[:len(vertex_info.grayl)]
    return out

def right_cortex_data(arr, fill=0, vertex_info=vertex_info):
    """
    Takes a 1D array of fMRI grayordinates and returns the values on the vertices of the right cortex mesh which is neccessary for surface visualization. 
    The unused vertices are filled with a constant (zero by default). 
    """
    out = np.zeros(vertex_info.num_meshr)
    out[:] = fill
    if len(arr) == len(vertex_info.grayr):
        # means arr is already just the right cortex
        out[vertex_info.grayr] = arr
    else:
        out[vertex_info.grayr] = arr[len(vertex_info.grayl):len(vertex_info.grayl) + len(vertex_info.grayr)]
    return out

def cortex_data(arr, fill=0, vertex_info=vertex_info):
    """
    Takes a 1D array of fMRI grayordinates and returns the values on the vertices of the full cortex mesh which is neccessary for surface visualization. 
    The unused vertices are filled with a constant (zero by default). 
    """
    dataL = left_cortex_data(arr, fill=fill, vertex_info=vertex_info)
    dataR = right_cortex_data(arr, fill=fill, vertex_info=vertex_info)
    return np.hstack((dataL, dataR))

# utility function for making a mesh for both hemispheres
# used internally by load_surfaces

def combine_meshes(meshL, meshR):
    """
    Combines left and right meshes into a single mesh for both hemispheres.
    """
    coordL, facesL = meshL
    coordR, facesR = meshR
    coord = np.vstack((coordL, coordR))
    faces = np.vstack((facesL, facesR+len(coordL)))
    return coord, faces

# loads all available surface meshes

def load_surfaces(example_filename=None, filename_sulc=None):
    """
    Loads all available surface meshes and sulcal depth file.
    Combines the left and right hemispheres into joint meshes for the whole brain.
    With no arguments loads the HCP S1200 group average meshes.
    If loading subject specific meshes it is enough to specify a single `example_filename` being one of
    `white|midthickness|pial|inflated|very_inflated` type e.g.

    ```
    mesh = load_surfaces(example_filename='PATH/sub-44.L.pial.32k_fs_LR.surf.gii')
    ```
    The function will load all available surfaces from that location.

    """
    if example_filename is None:
        filename_pattern = str(PKGDATA / 'S1200.{}.{}_MSMAll.32k_fs_LR.surf.gii')
    else:
        filename_pattern = re.sub('\.(L|R)\.', '.{}.', example_filename)
        filename_pattern = re.sub('white|midthickness|pial|inflated|very_inflated', '{}', filename_pattern)

    flatsphere_pattern = str(PKGDATA / 'S1200.{}.{}.32k_fs_LR.surf.gii')

    meshes = Bunch()
    for variant in ['white', 'midthickness', 'pial', 'inflated', 'very_inflated', 'flat' , 'sphere']:
        count = 0
        for hemisphere, hemisphere_name in [('L', 'left'), ('R', 'right')]:
            if variant in ['flat' , 'sphere']:
                filename = flatsphere_pattern.format(hemisphere, variant)
            else:
                filename = filename_pattern.format(hemisphere, variant)
            if os.path.exists(filename):
                coord, faces = surface.load_surf_mesh(filename)
                if variant=='flat':
                    coordnew = np.zeros_like(coord)
                    coordnew[:, 1] = coord[:, 0]
                    coordnew[:, 2] = coord[:, 1]
                    coordnew[:, 0] = 0
                    coord = coordnew
                meshes[variant+'_'+hemisphere_name] = coord, faces
                count += 1
            else:
                print('Cannot find', filename)
        if count==2:
            if variant == 'flat':
                coordl, facesl = meshes['flat_left']
                coordr, facesr = meshes['flat_right']
                coordlnew = coordl.copy()
                coordlnew[:, 1] = coordl[:, 1] - 250.0
                coordrnew = coordr.copy()
                coordrnew[:, 1] = coordr[:, 1] + 250.0
                meshes['flat'] = combine_meshes( (coordlnew, facesl), (coordrnew, facesr) )
            else:
                meshes[variant] = combine_meshes(meshes[variant+'_left'], meshes[variant+'_right'])

    if filename_sulc is None:
        filename_sulc = filename_pattern.format('XX','XX').replace('XX.XX', 'sulc').replace('surf.gii','dscalar.nii')
    if os.path.exists(filename_sulc):
        sulc_data = - nib.load(filename_sulc).get_fdata()[0]
        if len(sulc_data)==59412:
            # this happens for HCP S1200 group average data
            sulc_data = cortex_data(sulc_data)
        meshes['sulc'] = sulc_data
        num = len(meshes.sulc)
        meshes['sulc_left'] = meshes.sulc[:num//2]
        meshes['sulc_right'] = meshes.sulc[num//2:]
    else:
        print('Cannot load file {} with sulcal depth data'.format(filename_sulc))

    return meshes

mesh = load_surfaces()

# parcellations

def _load_hcp_parcellation(variant=None):
    allowed = ['mmp', 'ca_network', 'ca_parcels', 'yeo7', 'yeo17', 'standard']
    if variant not in allowed:
        print('argument should be one of ' + ','.join(allowed))
        return
    
    if variant=='standard':
        parcnpz = np.load(PKGDATA / 'standard.npz')
    if variant=='mmp':
        parcnpz = np.load(PKGDATA / 'mmp_1.0.npz')
    if variant=='ca_network':
        parcnpz = np.load(PKGDATA / 'ca_network_1.1.npz')
    if variant=='ca_parcels':
        parcnpz = np.load(PKGDATA / 'ca_parcels_1.1.npz')
    if variant=='yeo7':
        parcnpz = np.load(PKGDATA / 'yeo7.npz')
    if variant=='yeo17':
        parcnpz = np.load(PKGDATA / 'yeo17.npz')
    
    parcellation = Bunch()
    parcellation.ids = parcnpz['ids']
    parcellation.map_all = parcnpz['map_all']

    labels = parcnpz['labels']
    labelsdict = dict()
    rgba = parcnpz['rgba']
    rgbadict = dict()
    for i, k in enumerate(parcellation.ids):
        labelsdict[k] = labels[i]
        rgbadict[k] = rgba[i]

    parcellation.labels = labelsdict
    parcellation.rgba = rgbadict

    i = 0
    nontrivial_ids = []
    for k in parcellation.ids:
        if k!=0:
            nontrivial_ids.append(k)
            i += 1
    parcellation.nontrivial_ids = np.array(nontrivial_ids)

    return parcellation

# predefined parcellations

mmp = _load_hcp_parcellation('mmp')
ca_network = _load_hcp_parcellation('ca_network')
ca_parcels = _load_hcp_parcellation('ca_parcels')
yeo7 = _load_hcp_parcellation('yeo7')
yeo17 = _load_hcp_parcellation('yeo17')
standard = _load_hcp_parcellation('standard')

def view_parcellation(meshLR, parcellation):
    """
    View the given parcellation on an a whole brain surface mesh.
    """
    # for some parcellations the numerical ids need not be consecutive
    cortex_map = cortex_data(parcellation.map_all)
    ids = np.unique(cortex_map)
    normalized_cortex_map = np.zeros_like(cortex_map)
    rgba = np.zeros((len(ids), 4))
    for i in range(len(ids)):
        ind = cortex_map==ids[i]
        normalized_cortex_map[ind] = i
        rgba[i,:] = parcellation.rgba[ids[i]]

    cmap = matplotlib.colors.ListedColormap(rgba)
    return plotting.view_surf(meshLR, normalized_cortex_map, symmetric_cmap=False, cmap=cmap)

def parcellation_labels(parcellation):
    """
    Displays names of ROI's in a parcellation together with color coding and the corresponding numeric ids.
    """
    n = len(parcellation.ids)
    ncols = 4
    nrows = n // ncols + 1

    dpi = 72
    h = 12
    dh = 6
    H = h + dh

    Y = (nrows + 1) * H
    fig_height = Y / dpi

    fig, ax = plt.subplots(figsize=(18, fig_height))
    X, _ = fig.get_dpi() * fig.get_size_inches()
    w = X/ncols

    for i in range(n):
        k = parcellation.ids[i]
        label = parcellation.labels[k]
        if label == '':
            label = 'None'
        
        name = '{} ({})'.format(label, k)

        col = i // nrows
        row = i % nrows
        y = Y - (row * H) - H

        xi = w * (col + 0.05)
        xf = w * (col + 0.25)
        xt = w * (col + 0.3)

        ax.text(xt, y + h/2 , name, fontsize=h, horizontalalignment='left', verticalalignment='center')

        ax.add_patch(mpatches.Rectangle((xi, y), xf-xi, h ,linewidth=1,edgecolor='k',facecolor=parcellation.rgba[k]))
    
    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_axis_off()

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
    

def parcellate(X, parcellation, method=np.mean):
    """
    Parcellates the data into ROI's using `method` (mean by default). Ignores the unassigned grayordinates with id=0.
    Works both for time-series 2D data and snapshot 1D data.
    """
    n = np.sum(parcellation.ids!=0)
    if X.ndim==2:
        Xp = np.zeros((len(X), n), dtype=X.dtype)
    else:
        Xp = np.zeros(np, dtype=X.dtype)
    i = 0
    for k in parcellation.ids:
        if k!=0:
            if X.ndim==2:
                Xp[:, i] = method(X[:, parcellation.map_all==k], axis=1)
            else:
                Xp[i] = method(X[parcellation.map_all==k])
            i += 1
    return Xp

def unparcellate(Xp, parcellation):
    """
    Takes as input time-series (2D) or snapshot (1D) parcellated data.
    Creates full grayordinate data with grayordinates set to the value of the parcellated data.
    Can be useful for visualization.
    """
    n = len(parcellation.map_all)
    if Xp.ndim==2:
        X = np.zeros((len(Xp), n), dtype=Xp.dtype)
    else:
        X = np.zeros(n, dtype=Xp.dtype)
    i = 0
    for k in parcellation.ids:
        if k!=0:
            if Xp.ndim==2:
                X[:, parcellation.map_all==k] = Xp[:,i][:,np.newaxis]
            else:
                X[parcellation.map_all==k] = Xp[i]
            i += 1
    return X

def mask(X, mask, fill=0):
    """
    Takes 1D data `X` and a mask `mask`. Sets the exterior of mask to a constant (by default zero).
    Can be useful for visualization.
    """
    X_masked = np.zeros_like(X)
    X_masked[:] = fill
    X_masked[mask] = X[mask]
    return X_masked


def ranking(Xp, parcellation, descending=True):
    """
    Returns a dataframe with sorted values in the 1D parcellated array with appropriate labels
    """
    ind = np.argsort(Xp)
    if descending:
        ind = ind[::-1]
    labels = []
    ids = []
    for i in range(len(Xp)):
        j = ind[i]
        k = parcellation.nontrivial_ids[j]
        labels.append(parcellation.labels[k])
        ids.append(k)
    return pd.DataFrame({'region':labels, 'id':ids, 'data':Xp[ind]})


def make_lr_parcellation(parcellation):
    """
    Takes the given parcellation and produces a new one where parcels in the left and right hemisphere are made to be distinct.
    Subcortical voxels are set to 0 (unassigned).
    """
    map_all = np.zeros_like(parcellation.map_all)
    left = parcellation.map_all[struct.cortex_left]
    right = parcellation.map_all[struct.cortex_right]
    left_ids = np.unique(left)
    right_ids = np.unique(right)
    if left_ids[0]==0:
        left_ids = left_ids[1:]
    if right_ids[0]==0:
        right_ids = right_ids[1:]

    n_left_ids = len(left_ids)
    n_right_ids = len(right_ids)
    new_left_ids = np.arange(n_left_ids) + 1
    new_right_ids = np.arange(n_right_ids) + new_left_ids[-1] + 1

    labels = dict()
    labels[0] = ''
    ids = [0]
    nontrivial_ids = []
    rgba = dict()
    rgba[0] = np.array([1.0,1.0,1.0,1.0])

    for i in range(n_left_ids):
        old_id = left_ids[i]
        new_id = new_left_ids[i]
        map_all[struct.cortex_left][left==old_id] = new_id
        labels[new_id] = parcellation.labels[old_id] + ' L'
        ids.append(new_id)
        nontrivial_ids.append(new_id)
        color = parcellation.rgba[old_id].copy()
        color[:3] = color[:3] * 0.7
        rgba[new_id] = color

    for i in range(n_right_ids):
        old_id = right_ids[i]
        new_id = new_right_ids[i]
        map_all[struct.cortex_right][right==old_id] = new_id
        labels[new_id] = parcellation.labels[old_id] + ' R'
        ids.append(new_id)
        nontrivial_ids.append(new_id)
        rgba[new_id] = parcellation.rgba[old_id]

    new_parcellation = Bunch()
    new_parcellation.map_all = map_all
    new_parcellation.labels = labels
    new_parcellation.ids = ids
    new_parcellation.nontrivial_ids = nontrivial_ids
    new_parcellation.rgba = rgba

    return new_parcellation

# Other utilities

def normalize(X):
    """
    Normalizes data so that each grayordinate has zero (temporal) mean and unit standard deviation.
    """
    return (X - np.mean(X,axis=0))/np.std(X,axis=0)


# cortical adjacency matrix

cortical_adjacency = load_npz(PKGDATA / 'cortical_adjacency.npz')

def cortical_components(condition, cutoff=0):
    """
    Decomposes boolean array condition into connected components on the cortex.
    Returns `n_components`, `sizes` and an integer array `rois` with corresponding labels.
    0 means unassigned.
    """

    condition_cortex = condition[struct.cortex]
    rois = np.zeros(len(condition), dtype=int)
    G = cortical_adjacency[condition_cortex, :][:, condition_cortex]
    n_components, labels = connected_components(G)
    _, counts = np.unique(labels, return_counts=True)

    perm = np.argsort(counts)[::-1]
    invperm = np.argsort(perm)
    labels = invperm[labels] + 1
    rois[struct.cortex][condition_cortex] = labels
    sizes = counts[perm]

    if cutoff>0:
        maxc_arr = np.where(sizes<cutoff)[0]
        if len(maxc_arr)>0:
            maxc = maxc_arr[0]
            n_components = maxc
            sizes = sizes[:maxc]
            rois[rois>maxc] = 0

    return n_components, sizes, rois



