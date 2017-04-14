import collections
import os
import re
import sys
import numpy
# import struct
from gdalconst import *
from osgeo import gdal # from osgeo import ogr, osr, gdal



# regular expressions used to identify the type of image from its file name
reOldLandsatExt = re.compile('^L.[0-9]{14}.[A-Z]{2}[0-9]{2}_B[A-Z0-9][A-Z0-9]?\.TIF$')
reNewLandsatExt = re.compile('^L[A-Z][0-9]{2}_[A-Z][0-9][A-Z]{2}_[0-9]{6}_[0-9]{8}_[0-9]{8}_[0-9]{2}_[A-Z][0-9]_B[A-Z0-9][A-Z0-9]?\.TIF$')



## Get the pixels at the same positions from several images
#
# @param filepaths		A string of vector. The paths of the files
# @param x				A number. The position of the first pixel in x
# @param y				A number. The position of the first pixel in y
# @param xchunk			A number. The size of the window in x
# @param ychunk			A number. The size of the window in y
# @param dimpos			A numner. Position of the new dimension in the array: 0 at the biginning, -1 at the end
# @return				A numpy array
def getPixelImages(filepaths, x, y, xchunk, ychunk, dimpos = 0):
	res = []
	try:
		pixlist = []
		for filepath in filepaths:
			pixlist.append(getPixels(filepath, x, y, xchunk, ychunk))
		res = numpy.stack(pixlist, axis = dimpos)
	except:
		raise
	return(res)



## Get pixels from an image
#
# @param filepath		A string. The path of the file
# @param x				A number. The position of the first pixel in x
# @param y				A number. The position of the first pixel in y
# @param xchunk			A number. The size of the window in x
# @param ychunk			A number. The size of the window in y
# @param dimpos			A numner. Position of the new dimension in the array: 0 at the biginning, -1 at the end
# @return				A numpy array
def getPixels(filepath, x, y, xchunk, ychunk, dimpos = 0):
	res = []
	try:
		ds = gdal.Open(filepath, GA_ReadOnly)
		pixlist = []
		for bandid in range(1, ds.RasterCount + 1):
			band = ds.GetRasterBand(bandid)
			pixs = band.ReadAsArray(x, y, xchunk, ychunk)
			pixlist.append(pixs)
		if len(pixlist) == 1:
			res = pixlist[0]
		elif len(pixlist) > 1:
			res = numpy.stack(pixlist, axis = dimpos)
	except:
		raise
	finally:
		band = None
		ds = None
	return(res)



## Get some pixels from an image
#
# @param filepath		A string. The path of the file
# @param idband			A number. The id of the band to retrieve data from
# @param x				A number. The position of the first pixel in x
# @param y				A number. The position of the first pixel in y
# @param xchunk			A number. The size of the window in x
# @param ychunk			A number. The size of the window in y
# @return				A numpy array
def getBandPixels(filepath, idband, x, y, xchunk, ychunk):
	try:
		raster = filepath
		ds = gdal.Open(raster)
		band = ds.GetRasterBand(idband)
		array = band.ReadAsArray(x, y, xchunk, ychunk)
	except:
		raise()
	finally:
		band = None
		ds = None
	return(array)



## Get GDAL metadata from the image
#
# @param filepath A string.
# @return A dict
def getImageMetadata(filepath):
	res = {}
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
	except:
		raise RuntimeError("Could not get image metadata")
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
		raise()
	return res



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



## Fix the band number in the file's name (padding zeros)
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
# @param filepath A string. The path to the file
# @return A dict
def getFileNameMetadata(filepath):
	filename = os.path.basename(filepath)
	landsatSensor = {'C':'OLI/TIRS Combined', 'O':'OLI-only', 'T':'TIRS-only', 'E':'ETM+', 'T':'TM', 'M':'MSS'}
	landsatSatellite = {'7':'Landsat7', '8':'Landsat8'}
	landsatProcessingLevel = {'L1TP':'Precision Terrain', 'L1GP':'Systematic Terrain', 'L1GS':'Systematic'}
	landsatCollectionCategory = {'RT':'Real Time', 'T1':'Tier 1', 'T2':'Tier 2'}
	res = {'type': 'Unknown'}
	fband = ''
	if reOldLandsatExt.search(filename):
		# example LC80090452014008LGN00_B1.TIF
		ftype		= "Landsat untiered"
		fimage		= filename[0:21]
		fsensor		= landsatSensor[filename[1]]
		fsatellite	= landsatSatellite[str(int(filename[2]))]
		fpath		= filename[3:6]
		frow		= filename[6:9]
		fyear		= filename[9:13]
		fdoy		= filename[13:16]											# day of the year
		fstationId	= filename[16:19]
		farchive	= filename[19:21]
		if len(filename) > 25:
			fband = filename.split("_")[1].split('.')[0][1:]
		res = {
		'filepath': 	filepath, 
		'image': 		fimage, 
		'type': 		ftype, 
		'sensor': 		fsensor, 
		'satellite': 	fsatellite, 
		'path': 		fpath, 
		'row': 			frow, 
		'year': 		fyear, 
		'doy': 			fdoy, 
		'stationId': 	fstationId, 
		'archive':		farchive, 
		'band':			fband
		}
	elif reNewLandsatExt.search(filename):
		# example LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF
		ftype = "Landsat tiered"
		fimage		= filename[0:40]
		fsensor		= landsatSensor[filename[1]]
		fsatellite	= landsatSatellite[str(int(filename[2:4]))]
		fproclev	= landsatProcessingLevel[filename[5:9]]						# processing correction level
		fpath		= filename[10:13]
		frow		= filename[13:16]
		facqdate	= filename[17:25]											# acquisition date
		fprodate	= filename[26:34]											# processing date
		fcolnum		= filename[35:37]											# collection number
		fcolcat		= landsatCollectionCategory[filename[38:40]]				# collection category
		if len(filename) > 43:
			fband = filename.split("_")[7].split('.')[0][1:]
		res = {
		'filepath': filepath, 
		'image': fimage, 
		'type': ftype, 
		'sensor': fsensor, 
		'satellite': fsatellite, 
		'level': fproclev, 
		'path': fpath, 
		'row': frow, 
		'acquisition':facqdate, 
		'processing': fprodate, 
		'collection': fcolnum, 
		'category': fcolcat, 
		'band':fband
		}
	return res
	


## Get the number of consequtive repetitions in a vector
#
# @param vec A list of values that could repeat themselvec along the list
# @return Two lists. One made of elements found and the other with their respective last positions
def findrep(vec):
	el = []
	pos = []
	if len(vec) > 0:
		el.append(vec[0])
		for i in range(len(vec)):
			if(vec[i] != el[len(el) - 1]):
				pos.append(i - 1)
				el.append(vec[i])
		pos.append(i)
	return el, pos

