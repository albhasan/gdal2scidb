#!/bin/bash

# create array
# iquery -aq "CREATE ARRAY MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=0:172799:0:40; row_id=0:86399:0:40; time_id=0:511:0:512]"

# export h13v09



H=13                                 # MODIS TILE H
V=09                                 # MODIS TILE V
FIRST=2                              # Chunk's time side. Limit to this number of images
CHUNKSIZE=40                         # Chunk's spatial side (in pixels). i.e. 40 means 40x40 pixels
IMG_SZ=4800                          # Side of a whole image (in pixels)
OUT_DIR=/home/scidb/sdb_chunks/tmp   # Where to store the chunk binaries
SCRIPT_FOLDER=/home/scidb/ghProjects/gdal2scidb  # Path to script folder
SDB_INSTANCES=35                     # SciDB instances in the whole cluster


# Pre-processing
FIRST_CID=$((10#$H * $IMG_SZ))       # compute the col_id of the first pixel of the tile
FIRST_RID=$((10#$V * $IMG_SZ))       # compute the row_id of the first pixel of the tile

# Get the path of the files to process
FILES=$(find -L /home/scidb/MOD13Q1 -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | sort | head -n $FIRST)

# Build chunks from the images
python $SCRIPT_FOLDER/gdal2binImg.py --d2tid true --d2att false --tile2id false --log error $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $FILES





# create a list of files to process and feed them to GNU PARALLEL to avoid
find /home/scidb/sdb_chunks -type f | grep "MOD__13Q1_"$H"_"$V"_" | sort > fileslist_h"$H"v"$V".txt
parallel --eta --jobs 1 -n $SDB_INSTANCES --arg-file fileslist_h"$H"v"$V".txt bash load_parallel.sh







#find /home/scidb/sdb_chunks -type f | grep "MOD__13Q1_"$H"_"$V"_" | sort > fileslist_h"$H"v"$V".txt
parallel --eta --jobs 1 -n $SDB_INSTANCES --arg-file fileslist_h"$H"v"$V".txt bash load_parallel.sh
