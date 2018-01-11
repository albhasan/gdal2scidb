Load MOD13Q1 to SciDB
==========

Python scripts for exporting a raster (supported by GDAL) to SciDB binary format and CSV


### Files
- *load_distributed.sh*         Sample script for loading MOD13Q1 h12v08 binary files to SciDB (see examples below). It depends on GNU Parallel and *load_parallel.sh*.
- *load_parallel.sh*            Script for parallel loading  up to 35 binary files to SciDB.
- *README.md*                   This file.
- *sample_exportLC8.sh*         TODO
- *sample_exportMOD13Q1.sh*     Sample script for exporting MOD13Q1 h12v08 from HDF to binary (see examples below).
- *test_load_parallel.sh*       Script for testing parallel load to SciDB.
- *test_load.sh*                Script for testing data loading to SciDB.






### Example: Export, transform and load MODIS MOD13Q1


#### Server setup

##### Specifications

This sample was run on 5 servers with the following characteristics

- Linux 4.4.0-31-generic #50~14.04.1-Ubuntu SMP Wed Jul 13 01:07:32 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
- Description:    Ubuntu 14.04.5 LTS (trusty)

##### Code

```
cd ~
mkdir ghProjects
cd ghProjects
git clone https://github.com/albhasan/gdal2scidb.git
```



#### SciDB setup

SciDB 16.9 configuration file

```
[esensing2]
server-0=esensing-006,6
server-1=esensing-007,6
server-2=esensing-008,6
server-3=esensing-009,6
server-4=esensing-010,6
security=trust
db_user=scidb
install_root=/opt/scidb/16.9
pluginsdir=/opt/scidb/16.9/lib/scidb/plugins
logconf=/opt/scidb/16.9/share/scidb/log4cxx.properties
requests=1000
base-path=/home/scidb/data
base-port=1239
mem-array-threshold=512
smgr-cache-size=512
max-memory-limit=8000
merge-sort-buffer=64
small-memalloc-size=256
replication-receive-queue-size=40
replication-send-queue-size=8
sg-receive-queue-size=35
sg-send-queue-size=35
execution-threads=6
operator-threads=4
result-prefetch-threads=8
result-prefetch-queue-size=2
```

The cluster's coordinator machine *mounts* each instance's directory as detailed below. This eases SciDB's data upload in parallel
```
/home/scidb/instances/0/0
/home/scidb/instances/0/1
...
/home/scidb/instances/0/6
/home/scidb/instances/1/0
...
/home/scidb/instances/4/5
/home/scidb/instances/4/6
```


#### Data setup

The cluster's coordinator machine access a repository of MOD13Q1 using *automount* through a symbolic link */home/scidb/MOD13Q1*.

From the cluster's coordinator perspective, the MODIS files appear as:

```
ls -l /home/scidb/MOD13Q1/2000 | head -3
-rw-rw-r-- 1 1029    5049 123759483 May 26  2017 MOD13Q1.A2000049.h09v07.006.2015136104539.hdf
-rw-rw-r-- 1 1029    5049  15858843 May 26  2017 MOD13Q1.A2000049.h09v08.006.2015136104511.hdf
-rw-rw-r-- 1 1029    5049  15041283 May 26  2017 MOD13Q1.A2000049.h09v09.006.2015136104508.hdf
```


#### Array setup

The array's schema to store the data is:

```
MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=0:172799:0:40; row_id=0:86399:0:40; time_id=0:511:0:512]
```

### Export data from HDF to binary files

SciDB is able to load binary data as long as it follows a certain schema.

The script *sample_exportMOD13Q1.sh* relies on the Linux's *find* command to make a list of MOD13Q1 HDF files. To do its work, the script relies on the variables *H*, *V* *OUT_DIR*, *SCRIPT_DIR*, and *MODIS_DIR*. *H* and *V* constraint the search to a single MODIS tile. *OUT_DIR* is where the resulting binaries files are going to be stored. *SCRIPT_DIR* points to the directory hosting the *gdal2binImg.py* script. *MODIS_DIR* should point to the the directory with the HDf files.

Use the script *sample_exportMOD13Q1.sh* export the MOD13Q1 Tile h10v08 to binary:

```
mkdir -p /home/scidb/sdb_chunks/mod13q1_h10v08 # Directory for storing MOD13Q1 binary files
bash /home/scidb/ghProjects/gdal2scidb/etc/gdal2binImg/sample_exportMOD13Q1.sh
```


### Load binary data to SciDB

The script *load_distributed.sh* uses GNU parallel to coordinate calls to *load_parallel.sh* in order to load MOD13Q1 h12v08 binary files to SciDB. *load_distributed.sh* uses the variables *H* and *V* to filter the binaries files of a single MODIS tile and the variable *SDB_INSTANCES* to know the maximum number of binary files that *load_parallel.sh* can handle.

*load_parallel.sh* uses the varibles *SDB_INSTANCES_MACHINE* and *SDB_INSTANCES* to build a directory structure. This script expects to find such directory structure under the parent directory specified in *SDB_INSTANCES_PATH*.

```
bash /home/scidb/ghProjects/gdal2scidb/etc/gdal2binImg/load_distributed.sh
```
