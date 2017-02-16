import argparse
import collections
import os
import re
import sys

from osgeo import gdal # from osgeo import ogr, osr, gdal
from os.path import basename






# python gdal2sdbbin.py "/home/alber/landsat/downloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF" "/home/alber/Desktop"

# python gdal2sdbbin.py "/home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B1.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B2.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B3.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B4.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF" "/home/alber/Desktop"





# regular expressions used to identify the type of image from its file name
reOldLandsatExt = re.compile('^L.[0-9]{14}.[A-Z]{2}[0-9]{2}_B[0-9][0-9]?\.TIF$')
reNewLandsatExt = re.compile('^L[A-Z][0-9]{2}_[A-Z][0-9][A-Z]{2}_[0-9]{6}_[0-9]{8}_[0-9]{8}_[0-9]{2}_[A-Z][0-9]_B[0-9][0-9]?\.TIF$')


## Get some pixels from an image
#
# @param filename A string. The name of the file (no path!)
# @return A string
def getPixels(filename, band):
	try:
    	src_ds = gdal.Open(filename)											# open dataset    
    	srcband = src_ds.GetRasterBand(1)
	except RuntimeError, e:
		print(e)
	    raise
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
		if lastimg == getImageName(os.path.basename(imgfiles[key])):
			pixels = getPixels(imgfiles[key])
		else:
			lastimg = getImageName(os.path.basename(imgfiles[key]))




	# --------------------------------------------------------------------------	
	# open dataset
	#
	# take nxn pixels and upload thenm to a multidimensional array
	
	#
	
	
	
	
if __name__ == "__main__":
   main(sys.argv[1:])

