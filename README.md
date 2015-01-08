gdal2scidb
==========

Python scripts for exporting a raster (supported by GDAL) to SciDB binary format

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
<li><code>LICENSE</code> - License file.</li>
<li><code>README.md</code> - This file.</li>
<li><code>gdalAdd2bin.py</code> - Script that export/adds an GDAL-supported raster file to SciDB's binary format.</li>
<li><code>gdalCheckFolder.py</code> - Script that checks a folder for SciDB's binary files.</li>
<li><code>gdalLoad2scidb.py</code> - Script that loads a binary file to a SciDB database.</li>
<li><code>installGdalHdf.sh</code> - Script that compiles GDAL with HDF and NetCDF support.</li>
</ul>

<h3>Instructions:</h3>
<ol>
<li>Download the scripts to the <i>script-folder</i></li>
<li>Create a destination array in SciDB. This is the <i>dest-array</i>
	<ul>
	<li>
	<code>CREATE ARRAY MOD13Q1_TEST009_20140605 &lt;ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, viewza:int16, sunza:int16, relaza:int16, cdoy:int16, reli:int16&gt; [col_id=48000:72000,502,5,row_id=38400:62400,502,5,time_id=0:9200,1,0];</code>
	</li>
	</ul>
</li>
<li>Create a folder accesible by SciDB. This is the <i>check-folder</i> from where data is loaded to SciDB.</li>
<li>Run <code>gdalCheckFolder.py</code> pointing to the <i>check-folder</i>, the script checks the folder for binary files. this script must be able to find and run <code>gdalLoad2scidb.py</code> in the <i>script-folder</i>.</li>
<li>Run <code>gdalAdd2bin.py</code> to export MODIS HDFs to binary files. The resulting files can be stored in the <i>check-folder</i>.</li>
</ol>

<h3>Notes</h3>
<ul>
<li>The GDALDataType and the array's attribite data type must match. For example, when uploading a 3 band-TIF image, note below the array's uint8 attributes and the parameter gdalDatatype GDT_Byte:</li>
	<ul>
	<li><code>CREATE ARRAY ANDRE_ROT &lt;band01:uint8,band02:uint8,band03:uint8&gt; [col_id=0:14840,502,5,row_id=0:10915,502,5,time_id=0:20000,1,0]</code></li>
	<li><code>python /home/scidb/andre/gdal2scidb/gdalAdd2bin.py --log INFO --gdalDatatype GDT_Byte /home/scidb/andre/data/Aerial_Image/rot.tif /home/scidb/andre/data/Aerial_Image/rot.sdbbin</code></li>
	<li><code>python /home/scidb/andre/gdal2scidb/gdalLoad2scidb.py /home/scidb/andre/data/Aerial_Image/rot.sdbbin ANDRE_RO<T/code></li>
	</ul>
</ul>
