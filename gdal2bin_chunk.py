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
#
# landsat search --cloud 4 --start "january 10 2014" --end "january 10 2014" -p 009,045
# landsat search --cloud 0 --start "january 1 2014" --end "december 31 2014" -p 009,045 | grep sceneID
# landsat download -d /home/alber/landsat/downloads/ LC80090452014360LGN00 LC80090452014344LGN00 LC80090452014328LGN00 

# tar xjf /home/alber/landsat/downloads/LC80090452014008LGN00.tar.bz -C /home/alber/landsat/downloads
# tar xjf /home/alber/landsat/downloads/LC80090452014360LGN00.tar.bz -C /home/alber/landsat/downloads
# tar xjf /home/alber/landsat/downloads/LC80090452014344LGN00.tar.bz -C /home/alber/landsat/downloads
# tar xjf /home/alber/landsat/downloads/LC80090452014328LGN00.tar.bz -C /home/alber/landsat/downloads

# python gdal2bin_chunk.py "/home/alber/landsat/downloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF" "/home/alber/Desktop"

# python gdal2bin_chunk.py "/home/alber/landsat/downloads/LC80090452014360LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B2.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B2.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B2.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B2.TIF" "/home/alber/Desktop"

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

inputFiles = "/home/alber/landsat/downloads/LC80090452014360LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B2.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B9.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B2.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B1.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B2.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B8.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B10.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B11.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B6.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_B3.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B4.TIF /home/alber/landsat/downloads/LC80090452014344LGN00_B7.TIF /home/alber/landsat/downloads/LC80090452014360LGN00_B5.TIF /home/alber/landsat/downloads/LC80090452014008LGN00_BQA.TIF /home/alber/landsat/downloads/LC80090452014328LGN00_B2.TIF"

outputFolder = "/home/alber/landsat/downloads"
x = 0
y = 0
xchunk = 75
ychunk = 75
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

# get image names and files metadata
imgset = set()
imgfilesmd = list()
for key in imgfiles:
	filemd = getFileNameMetadata(imgfiles[key])								# get metadata from the file name
	imgfilesmd.append(filemd)												
	imgset.add(filemd['image'])												# get images' names

# a file per band or file per image?
fileperband = True
if len(imgset) == len(imgfiles):
	fileperband = False

# get pixels from each file ordered by band
imgpixlist = []
if fileperband:
	for img in imgset:
		ifiles = []															# a list of paths to bands of the same image
		for md in imgfilesmd:
			if img == md['image']:
				ifiles.append(md['filepath'])
		imgpixlist.append(getPixelImages(ifiles, x, y, xchunk, ychunk, 0)) 	# get the pixels of all the bands (files) of a single image
else:
	for ifile in imgfiles:
		imgpixlist.append(getPixels(ifile, x, y, xchunk, ychunk, 0))

pixarrays = numpy.stack(imgpixlist, axis = -1) 								# pixarrays dimensions are band, colid, rowid, time id

# write the binary






	
	
	
	
if __name__ == "__main__":
   main(sys.argv[1:])

