import os
import sys
import argparse
from array import array
import struct
import gdal
from gdalconst import *
import datetime
import logging


def mapGdaldatatype2(gdalType):
	try:
		res = {
			'GDT_Unknown': 0, 
			'GDT_Byte': 1, 
			'GDT_UInt16': 2, 
			'GDT_Int16': 3,
			'GDT_UInt32': 4, 
			'GDT_Int32': 5, 
			'GDT_Float32': 6, 
			'GDT_Float64': 7,
			'GDT_CInt16': 8, 
			'GDT_CInt32': 9, 
			'GDT_CFloat32': 10, 
			'GDT_CFloat64': 11,
			'GDT_TypeCount': 12
		}[gdalType]
	except KeyError:
		res = 0
	return res


def mapGdal2python(gdalType):
	#http://www.gdal.org/gdal_8h.html
	#http://docs.python.org/2/library/array.html
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
	try:
		res = {
			'GDT_Byte': 'f',
			'GDT_Int16': 'h', 
			'GDT_UInt16': 'H', 
			'GDT_Int32': 'i', 
			'GDT_UInt32': 'I', 
			'GDT_Float32': 'f',
			'GDT_Float64': 'd',
			'GDT_CInt16': 'h', 
			'GDT_CInt32': 'i', 
			'GDT_CFloat32': 'f',
			'GDT_CFloat64': 'd'
		}[gdalType]
	except KeyError:
		res = 'f'
	return res


def getImageMetadata(filepath):
	'''Resturns general information about the image'''
	try:
		path, filename = os.path.split(filepath)
		dataset = gdal.Open(filepath, GA_ReadOnly)
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
	return res
	

def addFile2bin(filepath, bfpath, lineMin, lineMax, sampMin, sampMax, deltaCol_id, deltaRow_id, timid, gdalDatatype):
	try:
		path, filename = os.path.split(filepath)
		dataset = gdal.Open(filepath, GA_ReadOnly)
		bfile = open(bfpath, "ab")
		xSize = sampMax - sampMin + 1
		ySize = lineMax - lineMin + 1
		fxSize = 'f' * xSize
		arraydt = mapGdal2python(gdalDatatype)
		gdaldt = mapGdaldatatype2(gdalDatatype)
		for imageLine in range(lineMin, lineMax + 1):
			idy = deltaRow_id + imageLine
			bandlines = []
			#Get the row of all the bands 
			for bandid in range(1, dataset.RasterCount + 1):
				band = dataset.GetRasterBand(bandid)
				scanline = band.ReadRaster( sampMin, imageLine, xSize, 1, xSize, 1, gdaldt)
				tuple_of_floats = struct.unpack(fxSize, scanline)
				bandlines.append(tuple_of_floats)
			# Retrieves a value of a column for all the bands
			for imageColumn in range(sampMin, sampMax + 1):
				idx = deltaCol_id + imageColumn
				vals = []
				#Values
				tmpcolid = imageColumn - sampMin
				for bandid in range(dataset.RasterCount):
					bandValue = bandlines[bandid][tmpcolid]#At this moment, the array starts at 0
					vals.append(bandValue)
				#Writes the values
				idxa = array('L',[idx, idy, timid])
				valsa = array(arraydt, vals)
				idxa.tofile(bfile)
				valsa.tofile(bfile)	
		bfile.close()
	except IOError as e:
		logging.exception("IOError:\n" + str(e.message) + " " + filepath)
	except:
		e = sys.exc_info()[0]
		logging.exception("Unknown exception:\n" + str(e.message) + " " + filepath)
	return bfpath

#********************************************************
#WORKER
#********************************************************
def main(argv):
	t0 = datetime.datetime.now()
	parser = argparse.ArgumentParser(description = "Add pixels from a file to a SCIDB's binary file")
	parser.add_argument("filepath", help = "Path to the file")
	parser.add_argument("binaryFilepath", help = "Path to the (new or existing) binary file for storing the results. Use .sdbbin as file extension")
	parser.add_argument("-lmin", "--lineMin", help = "file start row", type = int, default = 0)
	parser.add_argument("-lmax", "--lineMax", help = "file end row", type = int, default = 0)
	parser.add_argument("-smin", "--sampMin", help = "file start column", type = int, default = 0)
	parser.add_argument("-smax", "--sampMax", help = "file end column", type = int, default = 0)
	parser.add_argument("-dcol", "--deltaColId", help = "Column id displacement", type = int, default = 0)
	parser.add_argument("-drow", "--deltaRowId", help = "Row id displacement", type = int, default = 0)
	parser.add_argument("-dtime", "--deltaTimeId", help = "Time id displacement", type = int, default = 0)
	parser.add_argument("-gdt", "--gdalDatatype", help = "Datatype used when a raster line is read", default = 'GDT_Float32')
	parser.add_argument("--log", help = "Log level", default = 'WARNING')
	#Get parameters
	args = parser.parse_args()
	filepaths = args.filepath
	binaryFilepath = args.binaryFilepath
	lineMin = args.lineMin
	lineMax = args.lineMax
	sampMin = args.sampMin
	sampMax = args.sampMax
	deltaCol_id = args.deltaColId
	deltaRow_id = args.deltaRowId
	timid = args.deltaTimeId
	gdalDatatype = args.gdalDatatype
	log = args.log
	if(lineMax < lineMin or sampMax < sampMin):
		md = getImageMetadata(filepaths)
		if(lineMax == 0):
			lineMax = md['nrow'] - 1
		if(sampMax == 0):
			sampMax = md['ncol'] - 1
	if(lineMax == lineMin and sampMax == sampMin and lineMax == 0):
		md = getImageMetadata(filepaths)
		lineMin = 0
		sampMin = 0
		lineMax = md['nrow'] - 1
		sampMax = md['ncol'] - 1
	####################################################
	# CONFIG
	####################################################
	numeric_loglevel = getattr(logging, log.upper(), None)
	if not isinstance(numeric_loglevel, int):
		raise ValueError('Invalid log level: %s' % log)
	logging.basicConfig(filename = 'log_gdalAdd2bin.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
	logging.info("gdalAdd2bin: " + str(args))
	####################################################
	# SCRIPT
	####################################################
	hpaths = filepaths.split(';')
	print "Adding to binary file..."
	filecount = 0
	for hp in hpaths:
		if os.path.isfile(hp):
			print hp + ' ...'
			tmp = addFile2bin(hp, binaryFilepath, lineMin, lineMax, sampMin, sampMax, deltaCol_id, deltaRow_id, timid, gdalDatatype)
			logging.debug('File: ' + hp + ' added to: ' + binaryFilepath)
			filecount += 1
	t1 = datetime.datetime.now()	
	tt = t1 - t0
	logging.info("Number of files added: " + str(filecount) + " in " + str(tt))

if __name__ == "__main__":
   main(sys.argv[1:])