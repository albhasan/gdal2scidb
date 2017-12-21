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
# Usage:
# python gdal2binImg.py --log DEBUG 57600 48000 40 40 /home/scidb/alber/test /home/scidb/MOD13Q1/2010/MOD13Q1.A2010081.h12v10.006.2015206075415.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010289.h12v10.006.2015211225405.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010225.h12v10.006.2015210084208.hdf
#-------------------------------------------------------------------------------
# load flat
# iquery -aq "create array MOD13Q1_flat <col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64, day_of_year:int64, reliability:int64> [i=0:*:0:1000000]"
# iquery -aq "input(<col_id:int64, row_id:int64, time_id:int64, ndvi:int64, evi:int64, quality:int64, red:int64, nir:int64, blue:int64, mir:int64, view_zenith:int64, sun_zenith:int64, relative_azimuth:int64, day_of_year:int64, reliability:int64> [i=0:*], '/home/scidb/alber/test/MOD__13Q1_12_10_2680_4520.sdbbin', -2, '(int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64,int64)', 10, shadowArray)"
#
#
# iquery -aq "create array MOD13Q1 <ndvi:int16, evi:int16, quality:uint16, red:int16, nir:int16, blue:int16, mir:int16, view_zenith:int16, sun_zenith:int16, relative_azimuth:int16, day_of_year:int16, reliability:int8> [col_id=0:172799:0:40; row_id=0:86399:0:40; time_id=0:511:0:512]"
# iquery -aq "input()"


#-------------------------------------------------------------------------------
#inputFiles = "/home/scidb/MOD13Q1/2010/MOD13Q1.A2010081.h12v10.006.2015206075415.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010289.h12v10.006.2015211225405.hdf /home/scidb/MOD13Q1/2010/MOD13Q1.A2010225.h12v10.006.2015210084208.hdf".split(" ")
#coltrans = 0
#rowtrans = 0
#xsize = 40
#ysize = 40
#d2tid = True
#d2att = False
#tile2id = False
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
    parser.add_argument("--d2tid",      help = "Use the date to compute the time_id. Otherwise use the time-ordered cardinal position of the image in the inputFiles. Default = True", default = 'True')
    parser.add_argument("--d2att",      help = "Add the image date as an int yyyymmdd attribute (last attribute). Default = False", default = 'False')
    parser.add_argument("--tile2id",    help = "Include the image's tile (e.g path & row) as attribute(first two attributes) . Default = False", default = 'False')
    parser.add_argument("--log",        help = "Log level. Default = WARNING", default = 'WARNING')
    # Get parameters
    args = parser.parse_args()
    inputFiles = args.inputFiles
    coltrans = int(args.coltrans)
    rowtrans = int(args.rowtrans)
    xsize = int(args.xsize)
    ysize = int(args.ysize)
    outputDir = args.outputDir
    d2tid = args.d2tid in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    d2att = args.d2att in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    tile2id = args.tile2id in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
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
    iserlist = icol.getImagesSeries()
    if len(iserlist) > 1:
        logging.error("The given files belong to more than one ImageSeries: " + str(inputFiles))
        raise ValueError("The given files belong to more than one ImageSeries")
    #---------------------------------------------------------------------------
    # Write all the chunks of an image at once. Then add 
    tid = -1
    ofiles = [] # list of resuntilg files
    for img in iserlist[0]:
        logging.debug("Processing image:" + img.id)
        if(img.sname[0:3] == "MOD" or img.sname[0:3] == "MYD"):
            try:
                tid = tid + 1
                if d2tid:
                    tid = img.tid()
                if d2att:
                    imgacq = img.acquisition
                #--------------
                from osgeo import gdal
                import numpy as np
                gdal.UseExceptions()
                # get all the pixels from all bands
                gimg = gdal.Open(img.filepaths[0])
                barr = [] # list of opened subdatasets (bands)
                bpixarr = [] # list of subdatasets' pixels
                for subds in gimg.GetSubDatasets():
                    logging.debug("Processing subdataset:" + str(subds))
                    band = gdal.Open(subds[0])
                    bpix = band.ReadAsArray()
                    barr.append(band)
                    bpixarr.append(bpix.astype(np.int64)) # 
                # chunk the image
                xfrom = 0
                yfrom = 0
                xto = band.RasterXSize
                yto = band.RasterYSize
                for xc in range(xfrom, xto, xsize):
                    for yc in range(yfrom, yto, ysize):
                        logging.debug("Processing chunk: "+  str(xc) + " " + str(yc))
                        col_id = np.array((range(xc, min(xc + xsize, xto)) * min(ysize, yto - yc)), dtype=np.int64) + coltrans
                        row_id = (np.repeat(range(yc, min(yc + ysize, yto)), min(xsize, xto - xc)).astype(np.int64)) + rowtrans
                        time_id = np.repeat(tid, len(col_id)).astype(np.int64)
                        crt_id = []
                        if tile2id:
                            crt_id.append(np.repeat(img.path, len(col_id)).astype(np.int64))
                            crt_id.append(np.repeat(img.row, len(col_id)).astype(np.int64))
                        crt_id.append(col_id)
                        crt_id.append(row_id)
                        crt_id.append(time_id)
                        assert len(col_id) == len(row_id)
                        attdat = [] # list of flat bands' pixels of a chunk
                        for bpix in bpixarr:
                            chunkarr = bpix[xc:(xc + xsize), yc:(yc + ysize)]
                            chunkarrflat = chunkarr.flatten() 
                            assert len(col_id) == len(chunkarrflat)
                            attdat.append(chunkarrflat)
                        #
                        if d2att:
                            attdat.append(np.repeat(imgacq, len(col_id)).astype(np.int64))
                        logging.debug("Stacking the bands' chunk into one np array")
                        pixflat = np.vstack([crt_id, attdat]).T
                        fname = os.path.join(outputDir, iserlist[0].id + "_" + str(xc) + "_" + str(yc) + ".sdbbin.tmp")
                        ofiles.append(fname)
                        fsdbbin = open(fname, 'a')
                        pixflat.tofile(fsdbbin)
                        fsdbbin.close() 
                #--------------
            except Exception as e:
                logging.exception("message")
                raise RuntimeError("Could not get the pixels of a band")
            finally:
                band = None
                ds = None
                if not fsdbbin.closed:
                    fsdbbin.close()
        elif(img.sname[0:2] == "LC"):
            # open X images, read, merge, write
            print("not implemented")
    # remove tmp extension from filename
    for of in ofiles:
        basefn = os.path.splitext(of)[0]
        os.rename(thisFile, basefn)




if __name__ == "__main__":
   main(sys.argv[1:])

