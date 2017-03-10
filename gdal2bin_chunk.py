import argparse
import logging
import numpy
from gdal2bin_util import *







#********************************************************
# MAIN
#********************************************************
def main(argv):

# use landsat-util to download 
# landsat download -d /home/alber/landsat/downloads/ LC80090452014008LGN00
# tar xjf /home/alber/landsat/downloads/LC80090452014008LGN00.tar.bz -C /home/alber/landsat/downloads

# python gdal2bin_chunk.py "/home/alber/landsat/downloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF" "/home/alber/Desktop"

# python gdal2bin_chunk.py "/home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B2.TIF /home/alber/landsat/downloadsLC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B8.TIF /home/alber/landsat/downloadsLC80090452014008LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_BQA.TIF" "/home/alber/Desktop"



# python gdal2bin_chunk.py "/home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B1.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B2.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B3.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B4.TIF /home/alber/landsat/new/LC08_L1TP_140041_20130503_20161018_01_T1/LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF" "/home/alber/Desktop"



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
inputFiles = "/home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B2.TIF /home/alber/landsatdownloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_BQA.TIF" 
outputFolder = "/home/alber/landsat/downloads"
x = 0
y = 0
xchunk = 0
ychunk = 0
####################################################

####################################################
# SCRIPT
####################################################
flist = inputFiles.split()													# get the list of files
# sort by image-band
imgfiles = {}
for i in range(0, len(flist)):
	imgfiles[completeBandNumber(os.path.basename(flist[i]))] = flist[i]
imgfiles = collections.OrderedDict(sorted(imgfiles.items()))

for key in imgfiles:
	filemd = getFileNameMetadata(key)									# metadata from the file name
	print(filemd['image'], " - ", filemd['band'])



imgband = {}
# group bands into images
lastimg = ""
img = ""
bandid = 0
for key in imgfiles:
	# same image, different band (file)
	# group images
	
	
	
	
	
	
	
	try:
		
		imgmd = getImageMetadata(imgfiles[key])								# gdal metadata
		
		if len(imgmd['bandtype']) == 1:										# single-band image file
		else:																# multi-band image file
			# TODO: reshape array
			raise Exception("Multiband images aren't supported")	
	
	
	
		if img != getFileNameMetadata(key)['image']:							# new image
			bandid = 0
			pixs = getPixels(imgfiles[key], x, y, xchunk, ychunk)				# get the band pixels
			if len(pixs) == 1:													

			else:																

		else:
			bandid++
			# TODO: pixs is a numpy array. Join the band arrays and resha
	except:
		e = sys.exc_info()[0]
		logging.info("gdal2bin_chunk: " + str(e))

	
	
	
	
	
	
if __name__ == "__main__":
   main(sys.argv[1:])

