#!/bin/bash
################################################################################
# GET THE TIME ID OF A MODIS IMAGE
# Shell wrapper for date2index.py
#-------------------------------------------------------------------------------
# Usage:
# ./test.sh /home/scidb/MODIS/2015/MOD13Q1.A2015177.h14v11.006.2015301214542.hdf
################################################################################

# $0 script
# $1 path to HDF file

HDF_PATH=$1

HDF_FNAME=$(basename $HDF_PATH)
HDF_DATE=$(echo $HDF_FNAME | cut -c 10-16)
HDF_TID=$(/home/scidb/ghProjects/gdal2scidb/./date2index.py $HDF_DATE 20000101 16)

echo $HDF_TID
