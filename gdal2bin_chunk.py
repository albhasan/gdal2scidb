import argparse
import collections
import os
import re
import sys
import logging



from gdalconst import *
from osgeo import gdal # from osgeo import ogr, osr, gdal
from os.path import basename






# python gdal2bin_chunk.py "/home/alber/landsat/downloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF" "/home/alber/Desktop"

# python gdal2bin_chunk.py "/home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B1.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B2.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B3.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B4.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF" "/home/alber/Desktop"



# regular expressions used to identify the type of image from its file name
reOldLandsatExt = re.compile('^L.[0-9]{14}.[A-Z]{2}[0-9]{2}_B[0-9][0-9]?\.TIF$')
reNewLandsatExt = re.compile('^L[A-Z][0-9]{2}_[A-Z][0-9][A-Z]{2}_[0-9]{6}_[0-9]{8}_[0-9]{8}_[0-9]{2}_[A-Z][0-9]_B[0-9][0-9]?\.TIF$')





## Get GDAL metadata from the image
#
# @param filepath A string.
# @return A dict
def getImageMetadata(filepath):
	try:
		path, filename = os.path.split(filepath)
		dataset = gdal.Open(filepath, GA_ReadOnly)								# open dataset
		driver = dataset.GetDriver().LongName
		ncol = dataset.RasterXSize
		nrow = dataset.RasterYSize
		geotransform = dataset.GetGeoTransform() 
		#GeoTransform[0] /* top left x */
		#GeoTransform[1] /* w-e pixel resolution */
		#GeoTransform[2] /* rotation, 0 if image is "north up" */
		#GeoTransform[3] /* top left y */
		#GeoTransform[4] /* rotation, 0 if image is "north up" */
		#GeoTransform[5] /* n-s pixel resolution */ 
		bandtype = []
		for bandid in range(1, dataset.RasterCount + 1):
			band = dataset.GetRasterBand(bandid)
			bandtype.append(gdal.GetDataTypeName(band.DataType))
		res = {'file':filepath, 'driver':driver, 'ncol':ncol, 'nrow':nrow, 'bandtype':bandtype, 'geotransform':geotransform}	
	except IOError as e:
		logging.exception("IOError:\n" + str(e.message) + " " + filepath)
	except:
		e = sys.exc_info()[0]
		logging.exception("Unknown exception:\n" + str(e.message) + " " + filepath)
	finally:
		dataset = None															# close dataset
	return res



## Match the GDAL to python datatypes
#
# @param gdalType	A string. The name of the GDAL datatype
# @return			A string. The type code
def mapGdal2python(gdalType):
	# http://www.gdal.org/gdal_8h.html
	# http://docs.python.org/2/library/array.html
	#
	#GDT_Unknown 	Unknown or unspecified type
	#GDT_Byte 		Eight bit unsigned integer
	#GDT_UInt16 	Sixteen bit unsigned integer
	#GDT_Int16 		Sixteen bit signed integer
	#GDT_UInt32 	Thirty two bit unsigned integer
	#GDT_Int32 		Thirty two bit signed integer
	#GDT_Float32 	Thirty two bit floating point
	#GDT_Float64 	Sixty four bit floating point
	#GDT_CInt16 	Complex Int16
	#GDT_CInt32 	Complex Int32
	#GDT_CFloat32 	Complex Float32
	#GDT_CFloat64 	Complex Float64 	
	#
	# Type code		C Type 			Python Type			Minimum size in bytes
	# 'c'			char			character			1
	# 'b'			signed char		int					1
	# 'B'			unsigned char	int					1
	# 'u'			Py_UNICODE		Unicode character	2
	# 'h'			signed short	int					2
	# 'H'			unsigned short	int					2
	# 'i'			signed int		int					2
	# 'I'			unsigned int	long				2
	# 'l'			signed long		int					4
	# 'L'			unsigned long	long				4
	# 'f'			float			float				4
	# 'd'			double			float				8	
	try:
		res = {
			'GDT_Byte':		'f',
			'GDT_Int16':	'h', 
			'GDT_UInt16':	'H', 
			'GDT_Int32':	'i', 
			'GDT_UInt32':	'I', 
			'GDT_Float32':	'f',
			'GDT_Float64':	'd',
			'GDT_CInt16':	'h', 
			'GDT_CInt32':	'i', 
			'GDT_CFloat32':	'f',
			'GDT_CFloat64':	'd'
		}[gdalType]
	except KeyError:
		res = 'f'
	return res


## Match the GDAL to a datatype
#
# @param gdalType	A string. The name of the GDAL datatype
# @return			A number
def mapGdaldatatype2(gdalType):
	try:
		res = {
			'GDT_Unknown':	0, 
			'GDT_Byte':		1, 
			'GDT_UInt16':	2, 
			'GDT_Int16':	3,
			'GDT_UInt32':	4, 
			'GDT_Int32':	5, 
			'GDT_Float32':	6, 
			'GDT_Float64':	7,
			'GDT_CInt16':	8, 
			'GDT_CInt32':	9, 
			'GDT_CFloat32':	10, 
			'GDT_CFloat64':	11,
			'GDT_TypeCount':	12
		}[gdalType]
	except KeyError:
		res = 0
	return res



## Get some pixels from an image
#
# @param filepath		A string. The path of the file
# @param lineMin		A number. The minumim line to read (including)
# @param lineMax		A number. The maximum line to read (including)
# @param sampMin		A number. The minimum column to read (including)
# @param sampMax		A number. The maximum column to read (including)
# @param deltaCol_id	A number. The colum id of the first pixel in the image
# @param deltaRow_id	A number. The row id of the first pixel in the image
# @return
def getPixels(filepath, block):
	try:
		path, filename = os.path.split(filepath)
		dataset = gdal.Open(filepath, GA_ReadOnly)								# open dataset
		for i in range(dataset.RasterCount):
			band = dataset.GetRasterBand(band)
			# stats = band.GetStatistics( True, True )
			block_sizes = band.GetBlockSize()
			x_block_size = block_sizes[0]
			y_block_size = block_sizes[1]
			print(band.GetStatistics( True, True ))
			
			use bytearray to write 
			
			
	except RuntimeError, e:
		print(e)
		raise()
	finally:
		src_ds = None															# close dataset

	



## From a file name, returns the image name
#
# @param filename A string. The name of the file (no path!)
# @return A string
def getImageName(filename):
	res = ""
	if reOldLandsatExt.match(filename):
		# example LC80090452014008LGN00_B1.TIF
		res = filename[:21]
	elif reNewLandsatExt.match(filename):	
		# example LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF
		res = filename[:40]
	return res





## Fixes the band number in the file's name (padding zeros)
#
# @param filename A string. The name of the file (no path!)
# @return A dict
def completeBandNumber(filename):
	res = filename
	if reOldLandsatExt.match(filename):
		if(len(filename) == 28):
			res = filename[:23] + '0' + filename[23:]
	elif reNewLandsatExt.match(filename):
		if(len(filename) == 47):
			res = filename[:42] + '0' + filename[42:]
	return res





## Get the metadata from a file's name
#
# @param filename A string. The name of the file (no path!)
# @return A dict
def getFileNameMetadata(filename):
	landsatSensor = {'C':'OLI/TIRS Combined', 'O':'OLI-only', 'T':'TIRS-only', 'E':'ETM+', 'T':'TM', 'M':'MSS'}
	landsatSatellite = {'7':'Landsat7', '8':'Landsat8'}
	landsatProcessingLevel = {'L1TP':'Precision Terrain', 'L1GP':'Systematic Terrain', 'L1GS':'Systematic'}
	landsatCollectionCategory = {'RT':'Real Time', 'T1':'Tier 1', 'T2':'Tier 2'}
	res = {'type': 'Unknown'}
	if reOldLandsatExt.match(filename):
		# example LC80090452014008LGN00_B1.TIF
		ftype		= "Landsat untiered"
		fsensor		= landsatSensor[filename[1]]
		fsatellite	= landsatSatellite[str(int(filename[2]))]
		fpath		= filename[3:6]
		frow		= filename[6:9]
		fyear		= filename[9:13]
		fdoy		= filename[13:16]											# day of the year
		fstationId	= filename[16:19]
		farchive	= filename[19:21]
		if len(filename) > 24:
			fband = filename[23:25] if filename[24].isdigit() else filename[23]
		res = {'type': ftype, 'sensor': fsensor, 'satellite': fsatellite, 'path': fpath, 'row': frow, 'year': fyear, 'doy': fdoy, 'stationId': fstationId, 'archive':farchive}
	elif reNewLandsatExt.match(filename):
		# example LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF
		ftype = "Landsat tiered"
		fsensor		= landsatSensor[filename[1]]
		fsatellite	= landsatSatellite[str(int(filename[2:4]))]
		fproclev	= landsatProcessingLevel[filename[5:9]]						# processing correction level
		fpath		= filename[10:13]
		frow		= filename[13:16]
		facqdate	= filename[17:25]											# acquisition date
		fprodate	= filename[26:34]											# processing date
		fcolnum		= filename[35:37]											# collection number
		fcolcat		= landsatCollectionCategory[filename[38:40]]				# collection category
		res = {'type': ftype, 'sensor': fsensor, 'satellite': fsatellite, 'level': fproclev, 'path': fpath, 'row': frow, 'acquisition':facqdate, 'processing': fprodate, 'collection': fcolnum, 'category': fcolcat}		
	return res




#********************************************************
# MAIN
#********************************************************
def main(argv):
	parser = argparse.ArgumentParser(description = "Exports GDAL images to SciDB binary.")
	parser.add_argument("inputFiles", help = "List of images separated by spaces.")
	parser.add_argument("outputFolder", help = "Path to the folder where the binary files are created.")
	parser.add_argument("--log", help = "Log level. Default = WARNING", default = 'WARNING')
	#Get paramters
	args = parser.parse_args()
	inputFiles = args.inputFiles
	outputFolder = args.outputFolder
	log = args.log
	####################################################
	# CONFIG
	####################################################
	gdal.UseExceptions()														# use GDAL's error messages #gdal.DontUseExceptions()
	if os.path.isdir(outputFolder) == False:
		raise Exception("Invalid output folder!")
	# log
	numeric_loglevel = getattr(logging, log.upper(), None)
	if not isinstance(numeric_loglevel, int):
		raise ValueError('Invalid log level: %s' % log)
	logging.basicConfig(filename = 'log_gdal2bin_chunk.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
	logging.info("gdal2bin_chunk: " + str(args))
	####################################################
	# SCRIPT
	####################################################
	flist = inputFiles.split()													# get the list of files
	# sort by image-band
	imgfiles = {}
	for i in range(0, len(flist)) :
		imgfiles[completeBandNumber(os.path.basename(flist[i]))] = flist[i]
	imgfiles = collections.OrderedDict(sorted(imgfiles.items()))
	# group bands into images
	lastimg = ""
	for key in imgfiles:
		# same image, different band (file)
		print(getImageMetadata(imgfiles[key]))
		print("--------------------------------")
		
		if lastimg == getImageName(os.path.basename(imgfiles[key])):
			pixels = getPixels(imgfiles[key], 1)
		else:
			lastimg = getImageName(os.path.basename(imgfiles[key]))




	# --------------------------------------------------------------------------	
	# open dataset
	#
	# take nxn pixels and upload thenm to a multidimensional array
	
	#
	
	
	
	
if __name__ == "__main__":
   main(sys.argv[1:])

