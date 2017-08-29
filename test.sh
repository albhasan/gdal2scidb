#!/bin/bash
echo "################################################################################"
echo "GDAL2SCIDB: LOAD DATA USING CSV AND BINARY"
echo "################################################################################"



echo "--------------------------------------------------------------------------------"
echo "Load data using CSV data exported from MODIS"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null


echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output csv --tile2id false 0 0 3 3 10 10 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int16> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"

echo "Showing array's contents..."
iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using CSV data exported from MODIS (image date as an extra attribute)"
echo "--------------------------------------------------------------------------------"

rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output csv --d2att True --tile2id false 0 0 3 3 10 10 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int16, imgdate:int32> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"

echo "Showing array's contents..."
iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using CSV data exported from MODIS (include images's path and row)"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output csv --tile2id true 0 0 3 3 10 10 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <ipath_id:int64, irow_id:int64, col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int16> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"

echo "Showing array's contents..."
iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output binary --tile2id false 0 0 40 40 0 0 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 1) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, '(int64,int64,int64,int16,int16,uint16,int16,int16,int16,int16,int16,int16,int16,int16,int8)', 0, shadowArray)"

iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using binary data exported from MODIS (img date as an extra attribute)"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output binary --d2att True --tile2id false 0 0 40 40 0 0 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 1) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8, imgdate:int32> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, '(int64,int64,int64,int16,int16,uint16,int16,int16,int16,int16,int16,int16,int16,int16,int8,int32)', 0, shadowArray)"

iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using csv data exported from LANDSAT"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --d2tid False --output csv --tile2id false 0 0 1 1 0 0 $(find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1 -type f | grep "LC08_L1GT_226064_[0-9]\{8\}_[0-9]\{8\}_01_T2_sr_[+a-z|+A-Z].*\.tif$" | sort | head -n 33) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64, aerosol:uint8, band1:int16, band2:int16, band3:int16, band4:int16, band5:int16, band6:int16, band7:int16, evi:int16, ndvi:int16, savi:int16> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"

iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using csv data exported from LANDSAT (include images's path and row)"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

echo "Exporting images' pixels..."
python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --d2tid False --output csv --tile2id true 0 0 1 1 0 0 $(find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1 -type f | grep "LC08_L1GT_226064_[0-9]\{8\}_[0-9]\{8\}_01_T2_sr_[+a-z|+A-Z].*\.tif$" | sort | head -n 33) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <ipath_id:int64, irow_id:int64, col_id:int64, row_id:int64, time_id:int64, aerosol:uint8, band1:int16, band2:int16, band3:int16, band4:int16, band5:int16, band6:int16, band7:int16, evi:int16, ndvi:int16, savi:int16> [i=0:*]"

echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"

iquery -aq "scan(testG2B)"



echo "--------------------------------------------------------------------------------"
echo "Load data using csv data exported from LANDSAT"
echo "--------------------------------------------------------------------------------"

echo "Cleaning..."
rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --d2tid False --output binary --tile2id false 0 0 1 1 0 0 $(find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1 -type f | grep "LC08_L1GT_226064_[0-9]\{8\}_[0-9]\{8\}_01_T2_sr_[+a-z|+A-Z].*\.tif$" | sort | head -n 33) > /tmp/gdal2scidb_data

echo "Creating an array..."
iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64, aerosol:uint8, band1:int16, band2:int16, band3:int16, band4:int16, band5:int16, band6:int16, band7:int16, evi:int16, ndvi:int16, savi:int16> [i=0:*]"


echo "Loading data..."
iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, '(int64,int64,int64,uint8,int16,int16,int16,int16,int16,int16,int16,int16,int16,int16)', 0, shadowArray)"

iquery -aq "scan(testG2B)"



# TODO: Test --d2tid True



echo "--------------------------------------------------------------------------------"
echo "Cleaning..."
echo "--------------------------------------------------------------------------------"

rm /tmp/gdal2scidb_data 2> /dev/null
iquery -aq "remove(testG2B)" 2> /dev/null
iquery -aq "remove(shadowArray)" 2> /dev/null

exit 0
