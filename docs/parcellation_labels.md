# Parcellation labels

Here we summarize the labels and the corresponding numerical ids of regions of the parcellations included in `hcp_utils`. We start with the smaller parcellations ending with the largest ones.

[Return to the main documentation](index.html)


### Standard CIFTI subcortical structures

```
hcp.parcellation_labels(hcp.standard)
```

![standard parcellation labels](images/standard.png)


### Yeo 7-region networks

```
hcp.parcellation_labels(hcp.yeo7)
```

![yeo-7 parcellation labels](images/yeo7.png)


### Yeo 17-region networks

```
hcp.parcellation_labels(hcp.yeo17)
```

![yeo-17 parcellation labels](images/yeo17.png)

### Cole-Anticevic brain-wide functional networks

These functional networks differ from the previous ones
* always contain whole cortical parcels from the MMP parcellation
* extend to the subcortical structures 

```
hcp.parcellation_labels(hcp.ca_network)
```

![ca_network parcellation labels](images/ca_network.png)


### Multi Modal Parcellation MMP

To the 360 cortical regions we added the standard subcortical structures (ids 361-379).
We exchanged the internal numerical ids between the left and right hemispheres for consistency with the Cole-Anticevic Brain-wide Network Partition. 

```
hcp.parcellation_labels(hcp.mmp)
```

![mmp parcellation labels](images/mmp.png)

### Cole-Anticevic extension of MMP to a parcellation of the subcortical regions

```
hcp.parcellation_labels(hcp.ca_parcels)
```

![ca_parcels parcellation labels](images/ca_parcels.png)


[Return to the main documentation](index.html)

