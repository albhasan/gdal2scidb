#!/bin/bash
################################################################################
# SCIDB PARRALEL LOAD
#-------------------------------------------------------------------------------
# Call load_parallel.sh with lots of SciDB binary files
#-------------------------------------------------------------------------------
# NOTE:
# - Writes files to a file in order to avoid ERROR: Argument list too long
################################################################################
# build a lists of binary chunk files
H=12                                 # MODIS TILE H
V=08                                 # MODIS TILE V
SDB_INSTANCES=35                     # SciDB instances in the whole cluster
IMG_PREFIX=MOD                       # Prefix of the image name. i.e. MOD, MYD, LC8

# create a list of files to process and feed them to GNU PARALLEL to avoid
find -L /home/scidb/sdb_chunks -type f | grep $IMG_PREFIX"__13Q1_"$H"_"$V"_" | sort > fileslist_h"$H"v"$V".txt
parallel --eta --jobs 1 -n $SDB_INSTANCES --arg-file fileslist_h"$H"v"$V".txt bash load_parallel.sh

exit 0
