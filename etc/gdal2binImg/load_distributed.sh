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
export H=12                                 # MODIS TILE H
export V=09                                 # MODIS TILE V
export FIRST=40                             # Maximum number of files to list
export SDB_INSTANCES=35                     # SciDB instances in the whole cluster

# create a list of files to process and feed them to GNU PARALLEL to avoid 
find /home/scidb/sdb_chunks -type f | grep "MOD__13Q1_"$H"_"$V"_" | sort | head -n $FIRST > fileslist_h"$H"v"$V".txt
parallel --eta --jobs 1 -n $SDB_INSTANCES --arg-file fileslist_h"$H"v"$V".txt bash load_parallel.sh 


exit 0
