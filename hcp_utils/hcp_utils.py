import nibabel as nib
from nilearn import surface
from nilearn import plotting
from sklearn.utils import Bunch
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
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


def make_vertex_info(grayl, grayr, num_meshl, num_meshr):
    vertex_info = Bunch()
    vertex_info.grayl = grayl
    vertex_info.grayr = grayr
    vertex_info.num_meshl = num_meshl
    vertex_info.num_meshr = num_meshr
    return vertex_info

PKGDATA = Path(__file__).parent / 'data'

vertex_data = np.load(PKGDATA / 'fMRI_vertex_info_32k.npz')
vertex_info = make_vertex_info(vertex_data['grayl'], vertex_data['grayr'], int(vertex_data['num_meshl']), int(vertex_data['num_meshr']))

def get_HCP_vertex_info(img):
    assert isinstance(img, nib.cifti2.cifti2.Cifti2Image)
    
    map1 = img.header.get_index_map(1)
    bms = list(map1.brain_models)

    grayl = np.array(bms[0].vertex_indices)
    grayr = np.array(bms[1].vertex_indices)
    num_meshl = bms[0].surface_number_of_vertices
    num_meshr = bms[1].surface_number_of_vertices
    return make_vertex_info(grayl, grayr, num_meshl, num_meshr)


# The following three functions take a 1D array of fMRI grayordinates
# and return the array on the left- right- or both surface meshes

def left_cortex_data(arr, vertex_info=vertex_info):
    out = np.zeros(vertex_info.num_meshl)
    out[vertex_info.grayl] = arr[:len(vertex_info.grayl)]
    return out

def right_cortex_data(arr, vertex_info=vertex_info):
    out = np.zeros(vertex_info.num_meshr)
    if len(arr) == len(vertex_info.grayr):
        # means arr is already just the right cortex
        out[vertex_info.grayr] = arr
    else:
        out[vertex_info.grayr] = arr[len(vertex_info.grayl):len(vertex_info.grayl) + len(vertex_info.grayr)]
    return out

def cortex_data(arr):
    dataL = left_cortex_data(arr)
    dataR = right_cortex_data(arr)
    return np.hstack((dataL, dataR))

# utility function for making a mesh for both hemispheres
# used internally by load_surfaces

def combine_meshes(meshL, meshR):
    coordL, facesL = meshL
    coordR, facesR = meshR
    coord = np.vstack((coordL, coordR))
    faces = np.vstack((facesL, facesR+len(coordL)))
    return coord, faces

# loads all available surface meshes

def load_surfaces(filename_pattern=None, filename_sulc=None):
    if filename_pattern is None:
        filename_pattern = str(PKGDATA / 'S1200.{}.{}_MSMAll.32k_fs_LR.surf.gii')

    meshes = Bunch()
    for variant in ['white', 'midthickness', 'pial', 'inflated', 'flat']:
        count = 0
        for hemisphere, hemisphere_name in [('L', 'left'), ('R', 'right')]:
            filename = filename_pattern.format(hemisphere, variant)
            if os.path.exists(filename):
                meshes[variant+'_'+hemisphere_name] = surface.load_surf_mesh(filename)
                count += 1
            else:
                print('Cannot find', filename)
        if count==2:
            meshes[variant] = combine_meshes(meshes[variant+'_left'], meshes[variant+'_right'])

    if filename_sulc is None:
        filename_sulc = filename_pattern.format('XX','XX').replace('XX.XX', 'sulc').replace('surf.gii','dscalar.nii')
    if os.path.exists(filename_sulc):
        sulc_image = nib.load(filename_sulc)
        meshes['sulc'] = - sulc_image.get_fdata()[0]
        num = len(meshes.sulc)
        meshes['sulc_left'] = meshes.sulc[:num//2]
        meshes['sulc_right'] = meshes.sulc[num//2:]
    else:
        print('Cannot load file {} with sulcal depth data'.format(filename_sulc))

    return meshes

mesh = load_surfaces()

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
    parcellation.labels = parcnpz['labels']
    parcellation.ids = parcnpz['ids']
    parcellation.map_all = parcnpz['map_all']
    parcellation.rgba = parcnpz['rgba']

    return parcellation

mmp = _load_hcp_parcellation('mmp')
ca_network = _load_hcp_parcellation('ca_network')
ca_parcels = _load_hcp_parcellation('ca_parcels')
yeo7 = _load_hcp_parcellation('yeo7')
yeo17 = _load_hcp_parcellation('yeo17')
standard = _load_hcp_parcellation('standard')

def view_parcellation(meshLR, parcellation):
    cmap = matplotlib.colors.ListedColormap(parcellation.rgba)
    return plotting.view_surf(meshLR, cortex_data(parcellation.map_all), symmetric_cmap=False, cmap=cmap)

def parcellation_labels(parcellation):
    n = len(parcellation.labels)
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
        label = parcellation.labels[i]
        if label == '':
            label = 'None'
        
        name = '{} ({})'.format(label, parcellation.ids[i])

        col = i // nrows
        row = i % nrows
        y = Y - (row * H) - H

        xi = w * (col + 0.05)
        xf = w * (col + 0.25)
        xt = w * (col + 0.3)

        ax.text(xt, y + h/2 , name, fontsize=h, horizontalalignment='left', verticalalignment='center')

        ax.add_patch(mpatches.Rectangle((xi, y), xf-xi, h ,linewidth=1,edgecolor='k',facecolor=parcellation.rgba[i]))
    
    ax.set_xlim(0, X)
    ax.set_ylim(0, Y)
    ax.set_axis_off()

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
    




def normalize(X):
    return (X - np.mean(X,axis=0))/np.std(X,axis=0)

def parcellate(X, parcellation, method=np.mean):
    n = len(parcellation.ids)
    Xp = np.zeros((len(X), np), dtype=X.dtype)
    for i, k in enumerate(parcellation.ids):
        if k!=0:
            Xp[:, i] = method(X[:, parcellation.map_all==k], axis=1)
    return Xp

