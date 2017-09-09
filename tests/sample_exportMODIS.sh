#!/bin/bash
################################################################################
# EXPORT MOD13Q1 IMAGE SERIES TO SCIDB BINARY FILES
################################################################################
export H=12
export V=09
export CHUNKSIZE=40
export IMG_SZ=4800
export OUT_FOLDER=/home/scidb/tmp
export SCRIPT_FOLDER=/home/scidb/ghProjects/gdal2scidb
export FIRST=512
export FIRST_ID=0
export LAST_ID=$(($IMG_SZ - $CHUNKSIZE))
export FIRST_CID=$((10#$H * $IMG_SZ))
export FIRST_RID=$((10#$V * $IMG_SZ))
export SDB_FORMAT=binary
#
export FILES=$(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | sort | head -n $FIRST)
parallel --eta --jobs 0 python $SCRIPT_FOLDER/gdal2bin_chunk.py --d2tid true --d2att false --tile2id false --output $SDB_FORMAT --log error {1} {2} $CHUNKSIZE $CHUNKSIZE $FIRST_CID $FIRST_RID $FILES ">" $OUT_FOLDER/mod13q1_h"$H"v"$V"_{1}_{2} ::: $(seq $FIRST_ID $CHUNKSIZE $LAST_ID) ::: $(seq $FIRST_ID $CHUNKSIZE $LAST_ID)

