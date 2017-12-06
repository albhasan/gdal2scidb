gdal2scidb
==========

Python scripts for exporting a raster (supported by GDAL) to SciDB binary format and CSV


### Pre-requisites:
- Python
- Python GDAL
- GDAL
- SciDB
- These scripts must be installed on the SciDB's coordinator instance and they must be ran using an user enabled to execute IQUERY


### Files:
- `date2index.py`           Python application that transform a date into a time_id.
- `gdal2bin_chunkImg.py`    Python application that export GDAL images' segments to the stdout using SciDB's binary format.
- `gdal2bin_util.py`        Python module with utilitary functions.
- `LICENSE`                 License file.
- `README.md`               This file.
- `test_gdal2bin_util.py`   Unit test of utilitary functions.
- `test.sh`                 Case test script. It requires a running SciDB cluster, MOD13Q1 and LANDSAT surface reflectance images.


### Definitions:
- An *image* is made of one or more *bands* of the same path/row and date.
- An *image series* is made of one or more *images* of the same satellite, sensor, path and row but different acquisition time..
- A *band* is contained in one *image file*.
- A *image file* contains one or more *bands*.
- A *chunk* is a contiguos segment of one *image series*. That is, a chunk is made of pixels on the same positions but different time.


### Sample image series MODIS:
The MODIS files are retrieved using this bash command: 

```
find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3
```

This command retrives just three files. To retrieve the whole image series, remove the last part, starting at the pipe `|`. This sample is composed of the following files:

- `/home/scidb/MODIS/2006/MOD13Q1.A2006001.h09v08.005.2008063192116.hdf`
- `/home/scidb/MODIS/2006/MOD13Q1.A2006177.h09v08.005.2008131182157.hdf`
- `/home/scidb/MODIS/2006/MOD13Q1.A2006273.h09v08.005.2008272191539.hdf`

### Image series LANDSAT:

The LANDSAT files are retrieved using this bash command:

```
find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1 -type f | grep "LC08_L1GT_226064_[0-9]\{8\}_[0-9]\{8\}_01_T2_sr_[+a-z|+A-Z].*\.tif$" | sort | head -n 33
```

### Cases

#### Export a single chunk to CSV from the image series MODIS:
```
echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output csv --tile2id false 0 0 3 3 10 10 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3) > /tmp/gdal2scidb_data
echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int16> [i=0:*]"
echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"
echo "Showing array's contents..."
iquery -aq "scan(testG2B)"
```

#### Case test:
The `test.sh` bash script:
- The script searches MOD13Q1 images at `/home/scidb/MODIS`
- The script searches 11 band LANDSAT images at `/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1`

### Notes:

### TODO:
- These scripts build a chunk at a time. This is inefficient. Re-write 
- Test sentinel images

