#!/usr/bin/env python
#gdal2bin_chunkImg.py
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

################################################################################
# NOTES:
# Ubuntu uses an old version of numpy
# sudo easy_install --upgrade numpy
# sudo easy_install --upgrade scipy
#-------------------------------------------------------------------------------
# TODO: 
#-------------------------------------------------------------------------------
# Usage:
# python gdal2binImg.py 57600 48000 40 40 /home/scidb/MOD13Q1/2010/MOD13Q1.A2010081.h12v10.006.2015206075415.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010289.h12v10.006.2015211225405.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010225.h12v10.006.2015210084208.hdf
#-------------------------------------------------------------------------------
#inputFiles = "/home/scidb/MOD13Q1/2010/MOD13Q1.A2010081.h12v10.006.2015206075415.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010289.h12v10.006.2015211225405.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010225.h12v10.006.2015210084208.hdf".split(" ")
#coltrans = 0
#rowtrans = 0
#xsize = 40
#ysize = 40
#d2tid = True
#d2att = False
#tile2id = False
#output = "csv"
#log = "DEBUG"
################################################################################

def main(argv):
    parser = argparse.ArgumentParser(description = "Export GDAL images to chunked files using SciDB's binary format.")    
    parser.add_argument("coltrans",     help = "Translation applied to the column index.")
    parser.add_argument("rowtrans",     help = "Translation applied to the row index.")
    parser.add_argument("xsize",        help = "Chunk size in the x direction.")
    parser.add_argument("ysize",        help = "Chunk size in the y direction.")
    parser.add_argument("inputFiles",   help = "List of images separated by spaces.", nargs = "+")
    parser.add_argument("--d2tid",      help = "Use the date to compute the time_id. Otherwise use the time-ordered cardinal position of the image in the inputFiles. Default = True", default = 'True')
    parser.add_argument("--d2att",      help = "Add the image date as an int32 yyyymmdd attribute (last attribute). Default = False", default = 'False')
    parser.add_argument("--tile2id",    help = "Include the image's tile (e.g path & row) as pixel identifiers. Default = True", default = 'True')
    parser.add_argument("--output",     help = "The SciDB format used to export the data [binary, csv]. Default = binary", default = 'binary')
    parser.add_argument("--log",        help = "Log level. Default = WARNING", default = 'WARNING')
    # Get parameters
    args = parser.parse_args()
    inputFiles = args.inputFiles
    coltrans = int(args.coltrans)
    rowtrans = int(args.rowtrans)
    xsize = int(args.xsize)
    ysize = int(args.ysize)
    d2tid = args.d2tid in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    d2att = args.d2att in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    tile2id = args.tile2id in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    output = args.output
    log = args.log
    ####################################################
    # CONFIG
    ####################################################
    # log
    numeric_loglevel = getattr(logging, log.upper(), None)
    if not isinstance(numeric_loglevel, int):
        raise ValueError('Invalid log level: %s' % log)
    logging.basicConfig(filename = 'gdal2binImg.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
    logging.info("gdal2binImg: " + str(args))
    ####################################################
    # SCRIPT
    ####################################################
    if sys.byteorder != 'little':
        raise ValueError('SciDB requires little endian!')
    # sort files into list of image series
    icol = g2b.ImageCol(inputFiles)
    iserlist = icol.getImagesSeries()
    if len(iserlist) > 1:
        raise ValueError("The given files belong to more than one ImageSeries")
    #---------------------------------------------------------------------------
    for img in iserlist[0]:
        #img.getMetadata()
        if(img.sname[0:3] == "MOD" or img.sname[0:3] == "MYD"):
            # open the HDF once and write the chunks
            try:
                #--------------
                from osgeo import gdal
                import numpy as np
                gdal.UseExceptions()
                # get all the pixels from all bands
                gimg = gdal.Open(img.filepaths[0])
                barr = [] # list of opened subdatasets (bands)
                bpixarr = [] # list of subdatasets' pixels
                t = img.tid()
                for subds in gimg.GetSubDatasets():
                    band = gdal.Open(subds[0])
                    bpix = band.ReadAsArray()
                    barr.append(band)
                    bpixarr.append(bpix.astype(np.int64)) # 
                # chunk the image
                #for xc in range(xsize, band.RasterXSize, xsize):
                for xc in range(xsize, 80, xsize):
                    #for yc in range(ysize, band.RasterYSize, ysize):
                    for yc in range(ysize, 80, ysize):
                        col_id = (np.repeat(range(0, xsize), ysize).astype(np.int64)) + coltrans
                        row_id = np.array((range(0, ysize) * xsize), dtype=np.int64) + rowtrans
                        time_id = np.repeat(t, len(col_id)).astype(np.int64)
                        attdat = [] # list of flat bands' pixels of a chunk
                        for bpix in bpixarr:
                            chunkarr = bpix[(xc - xsize):xsize, (yc - ysize):ysize]
                            attdat.append(chunkarr.flatten())
                        # stack the bands into one array
                        pixflat = np.vstack([col_id, row_id, time_id, attdat]).T
                        fname = "/home/scidb/alber/test_" + str(xc - xsize) + "_" + str(yc - ysize) + ".sdbbin"
                        fsdbbin = open(fname, 'w')
                        pixflat.tofile(fsdbbin)
                        fsdbbin.close() 
                #--------------
            except:
                raise RuntimeError("Could not get the pixels of a band")
            finally:
                band = None
                ds = None
                if not fsdbbin.closed:
                    fsdbbin.close()
        elif(img.sname[0:2] == "LC"):
            # open X images, read, merge, write
            print("not implemented")




if __name__ == "__main__":
   main(sys.argv[1:])

