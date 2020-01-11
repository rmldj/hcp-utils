# hcp-utils (WORK IN PROGRESS)

Utilities to use  [Human Connectome Project](https://www.humanconnectome.org/) (HCP) and HCP-like data with [nilearn](https://nilearn.github.io/). 


![brain image](https://github.com/rmldj/hcp-utils/raw/master/images/image.png)


The utilities mainly deal with plotting surface data, accessing the predefined subcortical structures as well as using various parcellations. Various helper functions aid e.g. in mapping the HCP fMRI cortical data to surface vertices for visualization etc. The functions work directly with numpy arrays of shape `Tx91282` or `91282` for fMRI data, with `T` being the number of time frames, while `91282` is the standard HCP dimensionality for the 3T cortical surface and subcortical data.

## Documentation

Find the documentation at ...

## Installation

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


## External data

### Surface meshes

The default surface meshes for 3D visualization come from the group average of the Human Connectome Project (HCP) 1200 Subjects (S1200) data release (March 2017) processed using HCP pipelines. They can be obtained on BALSA: https://balsa.wustl.edu/reference/show/pkXDZ 


These group average files are redistributed under the HCP Open Access Data Use Terms https://www.humanconnectome.org/study/hcp-young-adult/document/wu-minn-hcp-consortium-open-access-data-use-terms with the acknowledgment: 

*"Data were provided [in part] by the Human Connectome Project, WU-Minn Consortium (Principal Investigators: David Van Essen and Kamil Ugurbil; 1U54MH091657) funded by the 16 NIH Institutes and Centers that support the NIH Blueprint for Neuroscience Research; and by the McDonnell Center for Systems Neuroscience at Washington University."*


### Parcellations

When using the included parcellations, please cite the relevant papers.

**The Glasser MMP1.0 Parcellation:** Glasser, Matthew F., Timothy S. Coalson, Emma C. Robinson, Carl D. Hacker, John Harwell, Essa Yacoub, Kamil Ugurbil, et al. 2016. “A Multi-Modal Parcellation of Human Cerebral Cortex.” Nature 536 (7615): 171–78.  http://doi.org/10.1038/nature18933 (see in particular the details in *Supplementary	Neuroanatomical	Results*).

**Yeo 7 or (17) Network Parcellation:** Yeo, B. T. Thomas, Fenna M. Krienen, Jorge Sepulcre, Mert R. Sabuncu, Danial Lashkari, Marisa Hollinshead, Joshua L. Roffman, et al. 2011. “The Organization of the Human Cerebral Cortex Estimated by Intrinsic Functional Connectivity.” Journal of Neurophysiology 106 (3): 1125–65. https://doi.org/10.1152/jn.00338.2011.

**The Cole-Anticevic Brain-wide Network Partition:** Ji JL*, Spronk M*, Kulkarni K, Repovs G, Anticevic A**, Cole MW** (2019). "Mapping the human brain's cortical-subcortical functional network organization". NeuroImage. 185:35–57. doi:10.1016/j.neuroimage.2018.10.006 [* = equal contribution; ** = senior authors] https://doi.org/10.1016/j.neuroimage.2018.10.006 (also available as an open access bioRxiv preprint: http://doi.org/10.1101/206292) and https://github.com/ColeLab/ColeAnticevicNetPartition/


