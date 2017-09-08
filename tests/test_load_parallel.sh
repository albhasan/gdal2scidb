echo "--------------------------------------------------------------------------------"
echo "Exporting an image series into chunks..."
echo "--------------------------------------------------------------------------------"


#40x40x512
#h12v09

export H=12
export V=09
export CHUNKSIZE=40
export IMG_SZ=4800
export OUT_FOLDER=/home/scidb/tmp
export FIRST=3
export FIRST_ID=4560
export LAST_ID=$(($IMG_SZ - $CHUNKSIZE))
export FIRST_CID=$((10#$H * $IMG_SZ))
export FIRST_RID=$((10#$V * $IMG_SZ))
export FILES=$(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h"$H"v"$V"\.006\.[0-9]\{13\}\.hdf$" | sort | head -n $FIRST)
export SDB_FORMAT=binary
#--dry-run 
parallel --jobs 0 python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --d2tid true --d2att false --tile2id false --output $SDB_FORMAT --log error {1} {2} $CHUNKSIZE $CHUNKSIZE $FIRST_CID $FIRST_RID $FILES ">" $OUT_FOLDER/mod13q1_h"$H"v"$V"_{1}_{2} ::: $(seq $FIRST_ID $CHUNKSIZE $LAST_ID) ::: $(seq $FIRST_ID $CHUNKSIZE $LAST_ID)



echo "--------------------------------------------------------------------------------"
echo "Loading 1 chunk into a 1D SciDB array..."
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
#
echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [i=0:*]"
#
echo "Loading data..."
iquery -naq "load(testG2B, '/home/scidb/tmp/mod13q1_h12v09_4680_4720', -2, '(int64,int64,int64,int16,int16,uint16,int16,int16,int16,int16,int16,int16,int16,int16,int8)', 0, shadowArray)"
#
iquery -aq "scan(testG2B)"
#
echo "--------------------------------------------------------------------------------"
echo "Loading 1 chunk into a 3D SciDB array..."
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(MOD13Q1)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
#
echo "Creating array MOD13Q1 for South America...."
# mod13q1 south america
# chunk 40x40x512
# from   h09v07
# to     h14v14
iquery -aq "CREATE ARRAY MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=43200:71999:0:40; row_id=33600:71999:0:40; time_id=0:511:0:512]" 2> /dev/null
#
iquery -naq "insert(redimension(input(<col_id:int64, row_id:int64, time_id:int64, ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [i=0:*], '/home/scidb/tmp/mod13q1_h12v09_4680_4720', -2, '(int64,int64,int64,int16,int16,uint16,int16,int16,int16,int16,int16,int16,int16,int16,int8)', 0, shadowArray), MOD13Q1), MOD13Q1)"
#
iquery -aq "scan(MOD13Q1)"
#
echo "--------------------------------------------------------------------------------"
echo "Loading 35 chunks into a 3D SciDB array..."
echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(MOD13Q1)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null
#
iquery -aq "CREATE ARRAY MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=43200:71999:0:40; row_id=33600:71999:0:40; time_id=0:511:0:512]" 2> /dev/null
# bash -x ./load_parallel.sh $(find /home/scidb/tmp/ -type f | head -n 35)
./load_parallel.sh $(find /home/scidb/tmp/ -type f | sort | head -n 35)
iquery -aq "op_count(MOD13Q1)"


