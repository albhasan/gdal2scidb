#!/bin/bash
################################################################################
# SCIDB LOADER HELPER
#-------------------------------------------------------------------------------
# Load in parallel a SDB_INSTANCES number of SciDB binary files
#-------------------------------------------------------------------------------
# NOTE:
# - Do not use pipes because not all partition formats support them
# - All instances' folders must be accessible from the coordinator instance
# - MOD13Q1 schema <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=0:172799:0:40; row_id=0:86399:0:40; time_id=0:511:0:512]
#-------------------------------------------------------------------------------
# PARAMETERS
# $1    path to SciDB binary file
# $2    path to SciDB binary file
# ...
# ...
# ...
# $35    path to SciDB binary file
################################################################################
# number of SciDB instances in each machine
SDB_INSTANCES_MACHINE=7
# number of SciDB instances in the whole cluster
SDB_INSTANCES=35
# Path containing the SciDB instance folders (e.g. 0, 1, 2, 3, 4)
SDB_INSTANCES_PATH=/home/scidb/instances
SDB_1D_SCHEMA="<col_id:int64, row_id:int64, time_id:int64, ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [i=0:*]"
SDB_FORMAT="'(int64,int64,int64,int16,int16,uint16,int16,int16,int16,int16,int16,int16,int16,int16,int8)'"
SDB_3D_ARRAY=MOD13Q1
#-------------------------------------------------------------------------------
echo "Validating..."
#-------------------------------------------------------------------------------
if [ "$#" -lt 1 ] || [ "$#" -gt $SDB_INSTANCES ]; then
    echo "ERROR: You must provide between 1 and $SDB_INSTANCES binary files"
    exit 1
fi
if [ "$#" -eq $SDB_INSTANCES ]; then
    #-------------------------------------------------------------------------------
    echo "Loading files using all SciDB instances..."
    #-------------------------------------------------------------------------------
    echo "Copying files..."
    count=0
    for f in "$@"; do
        min=$(( $count % $SDB_INSTANCES_MACHINE ))
        mip=`echo $(( $count / $SDB_INSTANCES_MACHINE )) | cut -f1 -d "."`
        cp "$f" $SDB_INSTANCES_PATH/$mip/$min/p &
        # the last one does NOT run in the background
        if [ $count -eq $SDB_INSTANCES ]; then
            cp "$f" $SDB_INSTANCES_PATH/$mip/$min/p
        fi
        count=`expr $count + 1`
    done
    echo "Running SciDB query..."
    iquery -naq "insert(redimension(input($SDB_1D_SCHEMA, 'p', -1, $SDB_FORMAT, 0, shadowArray), $SDB_3D_ARRAY), $SDB_3D_ARRAY)"
    echo "Deleting files..."
    countdel=0
    for f in "$@"; do
        min=$(( $countdel % $SDB_INSTANCES_MACHINE ))
        mip=`echo $(( $countdel / $SDB_INSTANCES_MACHINE )) | cut -f1 -d "."`
        rm $SDB_INSTANCES_PATH/$mip/$min/p
        countdel=`expr $countdel + 1`
    done
else
    #-------------------------------------------------------------------------------
    echo "Loading files using one SciDB instance..."
    #-------------------------------------------------------------------------------
    for f in "$@"; do
        echo "Copying file..."
        cp "$f" $SDB_INSTANCES_PATH/0/0/p
        echo "Running SciDB query..."
        iquery -naq "insert(redimension(input($SDB_1D_SCHEMA, '/home/scidb/data/0/0/p', -2, $SDB_FORMAT, 0, shadowArray), $SDB_3D_ARRAY), $SDB_3D_ARRAY)"
        echo "Deleting file..."
        rm $SDB_INSTANCES_PATH/0/0/p
    done
fi

exit 0

