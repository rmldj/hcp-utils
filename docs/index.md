# Introduction

Utilities to use  [Human Connectome Project](https://www.humanconnectome.org/) (HCP) and HCP-like data with [nilearn](https://nilearn.github.io/). 


![brain image](images/image.png)


The utilities mainly deal with plotting surface data, accessing the predefined subcortical structures as well as using various parcellations. Various helper functions aid e.g. in mapping the HCP fMRI cortical data to surface vertices for visualization etc. The functions work directly with numpy arrays of shape `Tx91282` or `91282` for fMRI data, with `T` being the number of time frames, while `91282` is the standard HCP dimensionality for the 3T cortical surface and subcortical data.


# Installation

Make sure that you have the following packages installed
```
nibabel, nilearn, numpy, scikit-learn, matplotlib, pandas
```
Then install with 
```
pip install hcp_utils   # TO BE IMPLEMENTED
```
upgrade with
```
pip install --upgrade hcp_utils
```


# Usage

Here we assume that the commands will be run in a Jupyter notebook as this allows for rotating and scaling the 3D plots with your mouse.

### Getting started

First import prerequisities.
```
import nibabel as nib
import nilearn.plotting as plotting
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```
Then import `hcp_utils`:
```
import hcp_utils as hcp
```

We use `nibabel` to load a CIFTI file with the fMRI time series. We also extract the fMRI time series to a `numpy` array.
```
img = nib.load('PATH/TO/fMRI_data_file.dtseries.nii')
X = img.get_fdata()
X.shape     # e.g. (1200, 91282)
```
which corresponds to 600 time-steps and 91282 grayordinates.

The CIFTI file format partitions the 91282 grayordinates into the left- and right- cortex as well as 19 subcortical regions. We can easily extract say the signal in the left hippocampus using `hcp.struct`

```
X_hipL = X[:, hcp.struct.hippocampus_left]
X_hipL.shape    # (1200, 764)
```

The other available regions are
```
hcp.struct.keys()
```

> dict_keys(['cortex_left', 'cortex_right', 'cortex', 'subcortical', 'accumbens_left', 'accumbens_right', 'amygdala_left', 'amygdala_right', 'brainStem', 'caudate_left', 'caudate_right', 'cerebellum_left', 'cerebellum_right', 'diencephalon_left', 'diencephalon_right', 'hippocampus_left', 'hippocampus_right', 'pallidum_left', 'pallidum_right', 'putamen_left', 'putamen_right', 'thalamus_left', 'thalamus_right'])

For convenience we add a function which normalized the data so that each grayordinate has zero (temporal) mean and unit standard deviation:
```
Xn = hcp.normalize(X)
```

### Plotting

In order to plot the cortical surface data for the whole bran, one has to have the surface meshes appropriate for HCP data and combine the ones corresponding to the left and right hemispheres into a single mesh. 
In addition, the HCP fMRI data are defined on a *subset* of the surface vertices (29696 out of 32492 for the left cortex and 29716 out of 32492 for the right cortex). Hence we have to construct an auxilliary array of size 32492 or 64984 with the fMRI data points inserted in appropriate places and a constant (zero by default) elsewhere. This is achieved by the `cortex_data(arr, fill=0)`, `left_cortex_data(arr, fill=0)` and `right_cortex_data(arr, fill=0)` functions.

`hcp_utils` comes with preloaded surface meshes from the HCP S1200 group average data as well as the whole brain meshes composed of both the left and right meshes. In addition sulcal depth data is included for shading. These data are packaged in the following way:

```
hcp.mesh.keys()
```

> dict_keys(['white_left', 'white_right', 'white', 'midthickness_left', 'midthickness_right', 'midthickness', 'pial_left', 'pial_right', 'pial', 'inflated_left', 'inflated_right', 'inflated', 'very_inflated_left', 'very_inflated_right', 'very_inflated', 'flat_left', 'flat_right', 'flat', 'sphere_left', 'sphere_right', 'sphere', 'sulc', 'sulc_left', 'sulc_right'])

Here `white` is the top of white matter, `pial` is the surface of the brain, `midthickness` is halfway between them, while `inflated` and `very_inflated` may be better for visualization. `flat` is a 2D flat representation.

In order to make an interactive 3D surface plot using `nilearn` of the normalized fMRI data (thresholded at 1.5) at t=29 on the inflated group average mesh, we write

```
plotting.view_surf(hcp.mesh.inflated, hcp.cortex_data(Xn[29]), 
    threshold=1.5, bg_map=hcp.mesh.sulc)
```

![brain image](images/out1.png)

The group average surfaces are much smoother than the ones for individual subjects. If we have those at our disposal we can load them and use them for visualization.

```
mesh_sub = hcp.load_surfaces(example_filename='path/to/fsaverage_LR32k/
    sub-XX.R.pial.32k_fs_LR.surf.gii')
```

Here as an argument we give just one example filename and `hcp_utils` will try to load all other versions for both hemispheres and the sulcal depth file assuming HCP like naming conventions (the `.R.pial` part here).
Let's look at the same data but now on the inflated single subject surface:

```
plotting.view_surf(mesh_sub.inflated, hcp.cortex_data(Xn[29]), 
    threshold=1.5, bg_map=mesh_sub.sulc)
```

![brain image](images/out2.png)

### Parcellations

`hcp_utils` comes with a couple of parcellations preloaded. In particular we have the following ones (with the name of the variable with the parcellation data)

* the *Glasser et.al.* Multi-Modal Parcellation (MMP 1.0) which partitions each hemisphere of the cortex into 180 regions - `hcp.mmp`
* the Cole-Anticevic Brain-wide Network Partition (version 1.1) which 
    * extends the Multi-Modal Parcellation of the cortex by a parcellation of the subcortical regions - `hcp.ca_parcels`
    * groups the cortical (MMP) and subcortical regions into functional networks - `hcp.ca_network`
* the *Yeo et.al.* 7- and 17- (cortical) functional networks - `hcp.yeo7` and `hcp.yeo17`
* the standard CIFTI partition into the main subcortical regions - `hcp.standard`

For references see the [github page](https://github.com/rmldj/hcp-utils). Please cite the relevant papers if you make use of these parcellations. These parcellations were extracted from the relevant `.dlabel.nii` files by the scripts in the `prepare/` folder of the package repository.

All the labels and the corresponding numerical ids for these parcellations are shown on the [parcellation labels](./parcellation_labels.html) page.
















