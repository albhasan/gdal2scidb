Load MOD13Q1 to SciDB
==========

Python scripts for exporting a raster (supported by GDAL) to SciDB binary format and CSV


### Pre-requisites:

### Procedure:
1. Export MOD13Q1 HDF images to SciDB binary. To achiueve this, you need to modify the script *sample_exportMODIS.sh*. This script relies on the Linux's *find* command to make a list of MOD13Q1 HDF files. At least, you need to custom the variables *H*, *V* *OUT_DIR*, *SCRIPT_DIR*, and *MODIS_DIR*. *H* and *V* constraint the search to s single MODIS tile. *OUT_DIR* is where the resulting binaries files are going to be stored. 
*SCRIPT_DIR* should point to the directory of the *gdal2binImg.py* script. *MODIS_DIR* should point to the the directory where the HDf files are stored (it could be the toip folder, since the *find* command is recursive). 

```
```

1. Load the SciDB binaries to SciDB



