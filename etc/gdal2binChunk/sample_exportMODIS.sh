#!/bin/bash
################################################################################
# EXPORT MOD13Q1 IMAGE SERIES TO SCIDB BINARY FILES
################################################################################
# Configuration
export H=12                                 # MODIS TILE H
export V=09                                 # MODIS TILE V
export CHUNKSIZE=40                         # Chunk's spatial side (in pixels). i.e. 40 means 40x40 pixels
export FIRST=512                            # Chunk's time side. Limit to this number of images
export IMG_SZ=4800                          # Side of a whole image (in pixels)
export OUT_FOLDER=/home/scidb/tmp           # Where to store the chunk binaries
export SCRIPT_FOLDER=/home/scidb/ghProjects/gdal2scidb # Path to script folder
export FIRST_ID=0                           # col & row of the first pixel from where start extracting chunks
export SDB_FORMAT=binary                    # chunk file format
# Pre-processing
export LAST_ID=$(($IMG_SZ - $CHUNKSIZE))
export FIRST_CID=$((10#$H * $IMG_SZ))       # compute the col_id of the first pixel of the tile
export FIRST_RID=$((10#$V * $IMG_SZ))       # compute the row_id of the first pixel of the tile
# Get the path of the files to process
export FILES=$(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | sort | head -n $FIRST)
# Build chunks from the images
parallel --eta --jobs 0 python $SCRIPT_FOLDER/gdal2bin_chunk.py --d2tid true --d2att false --tile2id false --output $SDB_FORMAT --log error {1} {2} $CHUNKSIZE $CHUNKSIZE $FIRST_CID $FIRST_RID $FILES ">" $OUT_FOLDER/mod13q1_h"$H"v"$V"_{1}_{2} ::: $(seq $FIRST_ID $CHUNKSIZE $LAST_ID) ::: $(seq $FIRST_ID $CHUNKSIZE $LAST_ID)

