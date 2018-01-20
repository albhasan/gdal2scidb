#!/bin/bash
################################################################################
# EXPORT MOD13Q1 IMAGE SERIES TO SCIDB BINARY FILES
################################################################################
# Configuration
H=10                                 # MODIS TILE H
V=08                                 # MODIS TILE V
CHUNKSIZE=40                         # Chunk's spatial side (in pixels). i.e. 40 means 40x40 pixels
FIRST=512                            # Chunk's time side. Limit to this number of images
IMG_SZ=4800                          # Side of a whole image (in pixels)
OUT_DIR=/home/scidb/sdb_chunks/mod13q1_h"$H"v"$V"    # Where to store the chunk binaries
SCRIPT_FOLDER=/home/scidb/ghProjects/gdal2scidb      # Path to script folder

# Pre-processing
FIRST_CID=$((10#$H * $IMG_SZ))       # compute the col_id of the first pixel of the tile
FIRST_RID=$((10#$V * $IMG_SZ))       # compute the row_id of the first pixel of the tile

# Get the path of the files to process
FILES=$(find -L /home/scidb/MOD13Q1 -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | sort | head -n $FIRST)

# Build chunks from the images
python $SCRIPT_FOLDER/gdal2binImg.py --d2tid true --d2att false --tile2id false --log error $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $FILES

exit 0
