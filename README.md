gdal2scidb
==========

Python scripts for exporting a raster (supported by GDAL) to SciDB binary format and CSV

<h3>Pre-requisites:</h3>
<ul>
<li>Python.</li>
<li>Python GDAL.</li>
<li>GDAL.</li>
<li>SciDB.</li>
<li>These scripts must be installed on the SciDB coordinator instance and they must be ran using an user enabled to execute IQUERY.</li>
</ul>

<h3>Files:</h3>
<ul>
<li><code>date2index.py</code> - Python application that transform a date into a time_id.</li>
<li><code>gdal2bin_chunkImg.py</code> - Python application that export GDAL images' segments to the stdout using SciDB's binary format.</li>
<li><code>gdal2bin_util.py</code> - Python module with utilitary functions.</li>
<li><code>LICENSE</code> - License file.</li>
<li><code>README.md</code> - This file.</li>
<li><code>test_gdal2bin_util.py</code> - Unit test of utilitary functions.</li>
<li><code>test.sh</code> - Case test script. It requires a running SciDB cluster, MOD13Q1 and LANDSAT surface reflectance images.</li>
</ul>


<h3>Definitions:</h3>
<ul>
<li>An <b>image</b> is made of one or more <b>bands</b> of the same path/row and date.</li>
<li>An <b>image series</b> is made of one or more <b>images</b> of the same satellite, sensor, path and row but different acquisition time.</li>
<li>A <b>band</b> is contained in one <b>file</b></li>
<li>A <b>file</b> contains one or more <b>bands</b></li>
<li>A <b>chunk</b> is a contiguos segment of one <b>image series</b>. That is, a chunk is made of pixels on the same positions but different time.</li>
</ul>


<h3>Sample image series MODIS:</h3>
The <b>image series</b> MODIS are retrieved using this bash command: 

<code>find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3</code>

This command retrives just three files. To retrieve the whole image series, remove the last part, starting at the pipe <code>|</code>. This sample is composed of the following files:

<ul>
<li><code>/home/scidb/MODIS/2006/MOD13Q1.A2006001.h09v08.005.2008063192116.hdf</code></li>
<li><code>/home/scidb/MODIS/2006/MOD13Q1.A2006177.h09v08.005.2008131182157.hdf</code></li>
<li><code>/home/scidb/MODIS/2006/MOD13Q1.A2006273.h09v08.005.2008272191539.hdf</code></li>
</ul>


<h3>Image series LANDSAT:</h3>
The <b>image series</b> LANDSAT are retrieved using this bash command <code>find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1 -type f | grep "LC08_L1GT_226064_[0-9]\{8\}_[0-9]\{8\}_01_T2_sr_[+a-z|+A-Z].*\.tif$" | sort | head -n 33</code>. It is composed of the following files:
<ul>
<li><code>TODO</code></li>
</ul>





<h3>Cases:</h3>

<h3>Export a single chunk to CSV from the image series MODIS:</h3>
<code>echo "Cleaning..."</code>
<code>rm /tmp/gdal2scidb_data 2> /dev/null</code>
<code>iquery -aq "remove(testG2B)" 2> /dev/null</code>
<code>iquery -aq "remove(shadowArray)" 2> /dev/null</code>
<code>echo "Exporting images' pixels..."</code>
<code>python /home/scidb/ghProjects/gdal2scidb/gdal2bin_chunk.py --log info --output csv --tile2id false 0 0 3 3 10 10 $(find /home/scidb/MODIS -type f | grep "MOD13Q1\.A[0-9]\{7\}\.h09v08\.005\.[0-9]\{13\}\.hdf$" | head -n 3) > /tmp/gdal2scidb_data</code>
<code>echo "Creating an array..."</code>
<code>iquery -aq "CREATE ARRAY testG2B <col_id:int64, row_id:int64, time_id:int64,ndvi:int16, evi:int16, quality:uint16, red:int16,nir:int16, blue:int16,mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int16> [i=0:*]"</code>
<code>echo "Loading data..."</code>
<code>iquery -naq "load(testG2B, '/tmp/gdal2scidb_data', -2, 'CSV')"</code>
<code>echo "Showing array's contents..."</code>
<code>iquery -aq "scan(testG2B)"</code>


<ol>
<li>TODO</li>
</ol>



<h3>Case test:</h3>
The <code>test.sh</code> bash script:
<ol>
<li>The script searches MOD13Q1 images at <code>/home/scidb/MODIS</code> </li>
<li>The script searches 11 band LANDSAT images at <code>/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1</code> </li>
</ol>




<h3>Notes</h3>
<ul>
<li>TODO</li>
</ul>

