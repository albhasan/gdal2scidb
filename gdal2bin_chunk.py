import sys
import argparse
import logging
import numpy
from array import array
from gdal2bin_util import *



#********************************************************
# MAIN
#********************************************************
def main(argv):
	parser = argparse.ArgumentParser(description = "Exports GDAL images to the stdout using SciDB's binary format.")
	parser.add_argument("inputFiles", help = "List of images separated by spaces.")
	parser.add_argument("col", help = "Number of the column from where to start getting data.")
	parser.add_argument("row", help = "Number of the row from where to start getting data.")
	parser.add_argument("colbuf", help = "Number of additional columns to get data from.")
	parser.add_argument("rowbuf", help = "Number of additional rows to get data from.")
	parser.add_argument("--log", help = "Log level. Default = WARNING", default = 'WARNING')
	#Get paramters
	args = parser.parse_args()
	inputFiles = args.inputFiles
	col = int(args.col)
	row = int(args.row)
	colbuf = int(args.colbuf)
	rowbuf = int(args.rowbuf)
	log = args.log
	####################################################
	# CONFIG
	####################################################
	gdal.UseExceptions()														# use GDAL's error messages #gdal.DontUseExceptions()
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
	bandtypes = []																# GDAL band types of an images
	if fileperband:
		for img in imgset:
			ifiles = []															# a list of paths to bands of the same image
			for md in imgfilesmd:
				if img == md['image']:
					ifiles.append(md['filepath'])
			imgpixlist.append(getPixelImages(ifiles, col, row, colbuf, rowbuf, 0)) 	# get the pixels of all the bands (files) of a single image
		# get band's datatypes using the bands of the last image
		for i in ifiles:
			bandtypes.append(getImageMetadata(i)['bandtype'])
	else:
		for ifile in imgfiles:
			imgpixlist.append(getPixels(ifile, x, y, xchunk, ychunk, 0))
		bandtypes = getImageMetadata(ifile)['bandtype']

	# unlist band types
	if isinstance(bandtypes[0], list):	
		bandtypes = sum(bandtypes, [])

	# cast to array
	# re-arrange dimensions from:	band_id, col_id, row_id, time_id
	# to:							col_id, row_id, time_id, band_id
	pixarrays = numpy.transpose(numpy.stack(imgpixlist, axis = 1))

	# write the binary
	bandtyp, bandpos = findrep(bandtypes)										# lists of consequetive band types and their positions
	for cid in range(pixarrays.shape[0]):
		for rid in range(pixarrays.shape[1]):
			for tid in range(pixarrays.shape[2]):
				idxa = array('L',[cid, rid, tid]) 								# sdb's array dimensions - L unsigned long
				idxa.tofile(sys.stdout)
				s = 0
				for i in range(len(bandtyp)):
					valsa = array(mapGdal2python(bandtyp[i]), pixarrays[cid, rid, tid][s:bandpos[i]])
					valsa.tofile(sys.stdout)
					s = bandpos[i] + 1


	
if __name__ == "__main__":
   main(sys.argv[1:])

