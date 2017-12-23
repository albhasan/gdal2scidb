echo "--------------------------------------------------------------------------------"
echo "GDAL2SCIDB EXAMPLE: Export data into chunks and then load it to SciDB ..."
echo "--------------------------------------------------------------------------------"

FIRST=3 # 512
H=12
V=10
CHUNKSIZE=40
IMG_SZ=4800
OUT_DIR=/home/scidb/sdb_chunks
MODIS_DIR=/home/scidb/MOD13Q1
FIRST_CID=$((10#$H * $IMG_SZ))
FIRST_RID=$((10#$V * $IMG_SZ))

echo "Exporting images' pixels..."
time python /home/scidb/ghProjects/gdal2scidb/gdal2binImg.py --d2tid True --d2att False --tile2id False --log debug $FIRST_CID $FIRST_RID $CHUNKSIZE $CHUNKSIZE $OUT_DIR $(find -L $MODIS_DIR -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | head -n $FIRST)

echo "--------------------------------------------------------------------------------"
echo "Loading 1 chunk into a 1D SciDB array..."
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
iquery -aq "CREATE ARRAY testG2B  <col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64,day_of_year:int64, reliability:int64>[i=0:*]"
iquery -naq "load(testG2B, '/home/scidb/sdb_chunks/MOD__13Q1_12_10_960_600.sdbbin', -2, '(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)', 0, shadowArray)"
iquery -aq "op_count(testG2B)"
iquery -aq "scan(testG2B)" | head
echo "--------------------------------------------------------------------------------"
echo "Loading 1 chunk into a 3D SciDB array..."
echo "--------------------------------------------------------------------------------"
SDBBIN_FORMAT="'(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)'"
SDBBIN_FLAT="<col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64,day_of_year:int64, reliability:int64> [i=0:*]"
MOD13Q1_FLAT="<col_id:int64, row_id:int64, time_id:int64, ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [i=0:*]"
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(MOD13Q1)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
iquery -aq "create array MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=0:172799:0:40; row_id=0:86399:0:40; time_id=0:511:0:512]" 2> /dev/null
iquery -naq "insert(redimension(cast(input($SDBBIN_FLAT, '/home/scidb/sdb_chunks/MOD__13Q1_12_10_960_600.sdbbin', -2, $SDBBIN_FORMAT, 0, shadowArray), $MOD13Q1_FLAT), MOD13Q1), MOD13Q1)"
iquery -aq "op_count(MOD13Q1)"
iquery -aq "scan(MOD13Q1)" | head
iquery -aq "scan(MOD13Q1)" | tail
echo "--------------------------------------------------------------------------------"
echo "Loading 35 chunks into a 3D SciDB array..."
echo "--------------------------------------------------------------------------------"
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(MOD13Q1)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
iquery -aq "create array MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=0:172799:0:40; row_id=0:86399:0:40; time_id=0:511:0:512]" 2> /dev/null
./load_parallel.sh $(find $OUT_DIR -type f | sort | head -n 35)
iquery -aq "op_count(MOD13Q1)"

exit 0
