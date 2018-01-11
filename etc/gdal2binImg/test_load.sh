#!/bin/bash
echo "################################################################################"
echo "GDAL2SCIDB EXAMPLE: Export data into CSV and binary and load then load it"
echo "################################################################################"

FIRST=3 # 512

H=12
V=10
CHUNKSIZE=40
IMG_SZ=4800
OUT_DIR=/home/scidb/sdb_chunks/tmp
MODIS_DIR=/home/scidb/MOD13Q1
FIRST_CID=$((10#$H * $IMG_SZ))
FIRST_RID=$((10#$V * $IMG_SZ))


# TODO: This fails! 20180911
# Query was executed successfully
# UserException in file: src/query/ops/input/InputArray.cpp function: moveNext line: 373
# Error id: scidb::SCIDB_SE_IMPORT_ERROR::SCIDB_LE_FILE_IMPORT_FAILED
# Error description: Import error. Import from file '/home/scidb/sdb_chunks/tmp/MOD__13Q1_12_10_960_600.sdbbin' (instance 0) to array 'testG2B' failed at line 8214, column 5, off
# set 985600, value='(unreadable)': Failed to read file: 0.
# /home/scidb/MOD13Q1/2004/MOD13Q1.A2004097.h12v10.006.2015154124916.hdf
# /home/scidb/MOD13Q1/2004/MOD13Q1.A2004353.h12v10.006.2015154142052.hdf
# /home/scidb/MOD13Q1/2004/MOD13Q1.A2004017.h12v10.006.2015154121146.hdf
echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS"
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm $OUT_DIR/*.sdbbin
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
echo "Exporting images' pixels..."
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att False --tile2id False --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $(find -L $MODIS_DIR -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | head -n $FIRST)
iquery -aq "CREATE ARRAY testG2B  <col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64,day_of_year:int64, reliability:int64>[i=0:*]"
iquery -naq "load(testG2B, '$OUT_DIR/MOD__13Q1_12_10_960_600.sdbbin', -2, '(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)', 0, shadowArray)"
iquery -aq "op_count(testG2B)"
iquery -aq "scan(testG2B)" | head





echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS (img date as an extra attribute)"
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm $OUT_DIR/*.sdbbin
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
echo "Exporting images' pixels..."
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att True --tile2id False --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $(find -L $MODIS_DIR -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | head -n $FIRST)
iquery -aq "CREATE ARRAY testG2B  <col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64,day_of_year:int64, reliability:int64, d2att:int64>[i=0:*]"
iquery -naq "load(testG2B, '$OUT_DIR/MOD__13Q1_12_10_960_600.sdbbin', -2, '(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)', 0, shadowArray)"
iquery -aq "op_count(testG2B)"
iquery -aq "scan(testG2B)" | head
echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS (img date, path, row as an extra attributes)"
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm $OUT_DIR/*.sdbbin
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
echo "Exporting images' pixels..."
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att True --tile2id True --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $(find -L $MODIS_DIR -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | head -n $FIRST)
iquery -aq "CREATE ARRAY testG2B  <h:int64, v:int64, col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64,day_of_year:int64, reliability:int64, d2att:int64>[i=0:*]"
iquery -naq "load(testG2B, '$OUT_DIR/MOD__13Q1_12_10_960_600.sdbbin', -2, '(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)', 0, shadowArray)"
iquery -aq "op_count(testG2B)"
iquery -aq "scan(testG2B)" | head
echo "--------------------------------------------------------------------------------"
echo "Last cleaning..."
echo "--------------------------------------------------------------------------------"
rm $OUT_DIR/*.sdbbin
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
