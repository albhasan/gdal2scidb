#!/bin/bash
################################################################################
# EXPORT LANDSAT IMAGE SERIES TO SCIDB BINARY FILES
################################################################################
# Configuration
export PPP=225                              # LANDSAT PATH
export RRR=065                              # LANDSAT ROW
export CHUNKSIZE=40                         # Chunk's spatial side (in pixels). i.e. 40 means 40x40 pixels


###########################
export FIRST=36 # 36                        # Chunk's time side. Limit to this number of images
export IMG_SZ_PIX=7581                      # Image size. Number of pixels (columns?)
export IMG_SZ_LIN=7721                      # Image size. Number of lines (in pixels)
#export FIRST_ID_PIX=0                      # first pixel from where start extracting chunks
#export FIRST_ID_LIN=0                      # first pixel from where start extracting chunks
export FIRST_ID_PIX=7520                    # first pixel from where start extracting chunks
export FIRST_ID_LIN=7680                    # first pixel from where start extracting chunks
###########################


export OUT_FOLDER=/disks/d7/sdb_chunksL8                # Where to store the chunk binaries
export SCRIPT_FOLDER=/home/scidb/ghProjects/gdal2scidb  # Path to script folder

export SDB_FORMAT=csv # binary              # chunk file format
export COL_NUM=01                           # LANDSAT collection number
export COL_CAT=T1                           # LANDSAT collection category
# Pre-processing
export LAST_ID_PIX=$((($IMG_SZ_PIX / $CHUNKSIZE) * $CHUNKSIZE))
export LAST_ID_LIN=$((($IMG_SZ_LIN / $CHUNKSIZE) * $CHUNKSIZE))
export FIRST_CID=0                          # compute the col_id of the first pixel of the tile
export FIRST_RID=0                          # compute the row_id of the first pixel of the tile

# Get the the files to process
export FILES=$(find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1 -type f | grep "LC08_L1TP_"$PPP$RRR"_[0-9]\{8\}_[0-9]\{8\}_"$COL_NUM"_"$COL_CAT"_sr_.*\.tif" | sort | head -n $FIRST)

# Build chunks from the images
# --eta
parallel --dry-run --jobs 0 python $SCRIPT_FOLDER/gdal2bin_chunk.py --d2tid false --d2att true --tile2id true --output $SDB_FORMAT --log error {1} {2} $CHUNKSIZE $CHUNKSIZE $FIRST_CID $FIRST_RID $FILES ">" $OUT_FOLDER/LC08_L1TP_"$PPP"v"$RRR"_{1}_{2} ::: $(seq $FIRST_ID_PIX $CHUNKSIZE $LAST_ID_PIX) ::: $(seq $FIRST_ID_LIN $CHUNKSIZE $LAST_ID_LIN)

