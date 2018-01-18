#!/bin/bash
echo "################################################################################"
echo "GDAL2SCIDB EXAMPLE: Export data into CSV and binary and load then load it"
echo "################################################################################"


OUT_DIR=/home/scidb/sdb_chunks/tmp
CHUNKSIZE=40
#
FIRST=1 # 512
MODIS_DIR=/home/scidb/MOD13Q1
IMG_SZ=4800
H=12
V=10
FIRST_CID=$((10#$H * $IMG_SZ))
FIRST_RID=$((10#$V * $IMG_SZ))
FILES_MODIS=$(find -L $MODIS_DIR -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | head -n $FIRST)
#
FIRST=33
LANDSAT_DIR=/home/scidb/LANDSAT8/SurfaceReflectanceC1
P="226"
R="064"
FILES_LANDSAT=$(find -L $LANDSAT_DIR -type f | grep -E "LC08_L1(TP|GT)_"$P""$R"_[[:digit:]]{8}_[[:digit:]]{8}_01_(T1|T2)_sr_([[:alnum:]]+|[[:alnum:]]+_[[:alnum:]]+)\.(tif|TIF)$" | sort | head -n $FIRST)



echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS"
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm $OUT_DIR/*.sdbbin
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
echo "Exporting images' pixels..."
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att False --tile2id False --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $FILES_MODIS
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
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att True --tile2id False --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $FILES_MODIS
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
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att True --tile2id True --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $FILES_MODIS
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


# TODO: add LANDSAT exports
echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS"
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm $OUT_DIR/*.sdbbin
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
echo "Exporting images' pixels..."
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --tile2id True --d2tid False --d2att True --l2att False --c2att True --ignoreLevel True --log debug 0 0 $CHUNKSIZE $CHUNKSIZE $OUT_DIR $FILES_LANDSAT
