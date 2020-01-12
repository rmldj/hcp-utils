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













