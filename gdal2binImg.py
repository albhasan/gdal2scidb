#!/usr/bin/env python
#gdal2binImg.py
import os
import sys
import argparse
import logging
import inspect
#from array import array

# import module from subfolder "gdal2scidb"
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0], "gdal2scidb")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import gdal2scidb as g2b
import g2bwriter as g2bw

################################################################################
# NOTES:
# Ubuntu uses an old version of numpy
# sudo easy_install --upgrade numpy
# sudo easy_install --upgrade scipy
#-------------------------------------------------------------------------------
# Usage:
# python gdal2binImg.py --log ERROR 57600 48000 40 40 /home/scidb/alber/test /home/scidb/MOD13Q1/2010/MOD13Q1.A2010081.h12v10.006.2015206075415.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010289.h12v10.006.2015211225405.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010225.h12v10.006.2015210084208.hdf
#-------------------------------------------------------------------------------
# load flat
# iquery -aq "CREATE ARRAY testG2B  <col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64,day_of_year:int64, reliability:int64>[i=0:*]"
# iquery -naq "load(testG2B, '/home/scidb/alber/test/MOD__13Q1_12_10_960_600.sdbbin', -2, '(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)', 0, shadowArray)"
# iquery -aq "op_count(testG2B)"
#-------------------------------------------------------------------------------
#inputFiles = "/home/scidb/MOD13Q1/2010/MOD13Q1.A2010081.h12v10.006.2015206075415.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010289.h12v10.006.2015211225405.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010225.h12v10.006.2015210084208.hdf".split(" ")
#coltrans = 0
#rowtrans = 0
#xsize = 40
#ysize = 40
#d2tid = True
#d2att = False
#tile2id = False
#ignoreLevel = False
#log = "DEBUG"
################################################################################

def main(argv):
    parser = argparse.ArgumentParser(description = "Export GDAL images to chunked files using SciDB's binary format.")    
    parser.add_argument("coltrans",     help = "Translation applied to the column index.")
    parser.add_argument("rowtrans",     help = "Translation applied to the row index.")
    parser.add_argument("xsize",        help = "Chunk size in the x direction.")
    parser.add_argument("ysize",        help = "Chunk size in the y direction.")
    parser.add_argument("outputDir",    help = "Output directory.")
    parser.add_argument("inputFiles",   help = "List of images separated by spaces.", nargs = "+")
    parser.add_argument("--tile2id",    help = "Include the image's tile (e.g path & row) as attributes (first two attributes) . Default = False", default = 'False')
    parser.add_argument("--d2tid",      help = "Use the date to compute the time_id. Otherwise use the time-ordered cardinal position of the image in the inputFiles. Default = True", default = 'True')
    parser.add_argument("--d2att",      help = "Add the image date as an int yyyymmdd attribute (last attribute). Default = False", default = 'False')
    parser.add_argument("--l2att",      help = "Add the image level as attribute. Default = False", default = 'False')
    parser.add_argument("--c2att",      help = "Add the image category as attribute. Default = False", default = 'False')
    parser.add_argument("--ignoreLevel",help = "Ignore the image's processing level when building ImageSeries. Default = False", default = 'False')
    parser.add_argument("--log",        help = "Log level. Default = WARNING", default = 'WARNING')
    # Get parameters
    args = parser.parse_args()
    inputFiles = args.inputFiles
    coltrans = int(args.coltrans)
    rowtrans = int(args.rowtrans)
    xsize = int(args.xsize)
    ysize = int(args.ysize)
    outputDir = args.outputDir
    trueList = ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    tile2id = args.tile2id in trueList
    d2tid = args.d2tid in trueList
    d2att = args.d2att in trueList
    l2att = args.l2att in trueList
    c2att = args.c2att in trueList
    ignoreLevel = args.ignoreLevel in trueList
    log = args.log
    ####################################################
    # CONFIG
    ####################################################
    # log
    numeric_loglevel = getattr(logging, log.upper(), None)
    if not isinstance(numeric_loglevel, int):
        raise ValueError('Invalid log level: %s' % log)
    logging.basicConfig(filename = 'gdal2binImg.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
    logging.info("------------")
    logging.info("gdal2binImg: " + str(args))
    ####################################################
    # SCRIPT
    ####################################################
    if sys.byteorder != 'little':
        raise ValueError('SciDB requires little endian!')
    # sort files into list of image series
    icol = g2b.ImageCol(inputFiles)
    iserlist = icol.getImagesSeries(ignoreLevel)
    if len(iserlist) > 1:
        logging.error("The given files belong to more than one ImageSeries: " + str(inputFiles))
        raise ValueError("The given files belong to more than one ImageSeries")
    # Write all the chunks of an image at once
    logging.debug("Calling the writer...")
    sdbw = g2bw.SdbWriter()
    sdbw.serialize(iserlist[0], d2tid, d2att, tile2id, xsize, ysize, coltrans, rowtrans, outputDir, l2att, c2att, logging)




if __name__ == "__main__":
   main(sys.argv[1:])

