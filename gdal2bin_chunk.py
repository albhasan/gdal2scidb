import sys
import argparse
import logging
import numpy
from array import array
from gdal2bin_util import *

################################################################################
# MAIN
#
# sdb2bin(files, chunk, chunkTranslation)
#
#-------------------------------------------------------------------------------
# Ubuntu uses an old version of numpy
# sudo easy_install --upgrade numpy
# sudo easy_install --upgrade scipy
#-------------------------------------------------------------------------------
# Use:
# python gdal2bin_chunk.py --output dcsv --tile2id true 0 0 3 3 10 10 /home/alber/Documents/tmp/MOD13Q1.A2013209.h12v10.005.2013226054045.hdf 
################################################################################
def main(argv):
    parser = argparse.ArgumentParser(description = "Export GDAL images to the stdout using SciDB's binary format.")
    parser.add_argument("col", help = "Number of the column from where to start getting data.")
    parser.add_argument("row", help = "Number of the row from where to start getting data.")
    parser.add_argument("colbuf", help = "Number of additional columns to get data from.")
    parser.add_argument("rowbuf", help = "Number of additional rows to get data from.")
    parser.add_argument("coltrans", help = "Translation applied to the column index.")
    parser.add_argument("rowtrans", help = "Translation applied to the row index.")
    parser.add_argument("inputFiles", help = "List of images separated by spaces.", nargs = "+")
    parser.add_argument("--d2tid", help = "Use the date to compute the time_id. Otherwise use the time-ordered cardinal position of the image in the inputFiles. Default = True", default = 'True')
    parser.add_argument("--tile2id", help = "Include the image's tile (e.g path & row) as pixel identifiers. Default = True", default = 'True')
    parser.add_argument("--output", help = "The SciDB format used to export the data [binary, dcsv]. Default = binary", default = 'binary')
    parser.add_argument("--log", help = "Log level. Default = WARNING", default = 'WARNING')
    # Get parameters
    args = parser.parse_args()
    inputFiles = args.inputFiles
    col = int(args.col)
    row = int(args.row)
    colbuf = int(args.colbuf)
    rowbuf = int(args.rowbuf)
    coltrans = int(args.coltrans)
    rowtrans = int(args.rowtrans)
    d2tid = args.d2tid in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    t2id = args.tile2id in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    output = args.output
    log = args.log
    ####################################################
    # CONFIG
    ####################################################
    gdal.UseExceptions()                                                        # use GDAL's error messages #gdal.DontUseExceptions()
    # log
    numeric_loglevel = getattr(logging, log.upper(), None)
    if not isinstance(numeric_loglevel, int):
        raise ValueError('Invalid log level: %s' % log)
    logging.basicConfig(filename = 'log_gdal2bin_chunk.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
    logging.info("gdal2bin_chunk: " + str(args))
    ####################################################
    # SCRIPT
    #---------------------------------------------------
    # [1] image == [n] bands of the same path/row and date
    # [1] image series == [n] images of the same satellite, sensor, path and row but different acquisition time
    # [1] band  == [1]file
    # [1] file  == [n] bands
    ####################################################
    # sort files by image-path/row-band
    files = sortFiles(inputFiles)
    # get files' metadata
    imgseries = set()                                                           # set of series of images
    filesmd = list()                                                            # list of metadata derived from file names
    fmd = ""
    for key,value in files.items():
        fmd = getFileNameMetadata(value)
        filesmd.append(fmd)
        imgseries.add(fmd['satellite'] + fmd['sensor']+ fmd['path'] + fmd['row'])
    # validation
    if len(imgseries) != 1:
        logging.error("Invalid number of time series of images: " + str(imgseries))
        sys.exit(0)
    # NOTE: assume all the images belong to the same path & row or TILE!!!!
    ipath = fmd['path']
    irow = fmd['row']
    # build list of images and filepaths
    imgfiles = imgseries2imgfp(filesmd)                                         # List [img, [filepaths]]
    # validation
    if len(imgfiles) == 0:
        logging.error("No images found")
        sys.exit(0)
    nimg = len(imgfiles[0][1])
    for i in range(1, len(imgfiles)):
        if nimg != len(imgfiles[i][1]):
            logging.error("Inconsistent number of files in images: " + imgfiles[i][0])
            sys.exit(0)
    # get band's datatypes from of a single image
    bandtypes = []                                                              # GDAL band types of an image's bands
    for fp in imgfiles[0][1]:
        bandtypes.append(getGdalMetadata(fp)['bandtype'])
    bandtypes = sum(bandtypes, []) if isinstance(bandtypes[0], list) else bandtypes
    logging.info("Bandtypes: " + str(bandtypes))
    # get time_id transformation parameters
    tidparam = gettimeidparameters(filesmd[0]['sname'])
    #---------------------------------------------------------------------------
    # get pixels from each image
    #---------------------------------------------------------------------------
    tid = -1
    for ifiles in imgfiles:
        if d2tid:
            tid = ymd2tid(int(ifiles[0][-8:]), int(tidparam['origin']), int(tidparam['period']), tidparam['yearly'])
        else:
            tid = tid + 1
        imgpixs = getPixelImages(ifiles[1], col, row, colbuf, rowbuf, -1)       # pixels of the bands of an image. A numpy.ndarray object
        if len(imgpixs.shape) < 3:                                              # not enough pixels left to be read
            logging.warn("Insufficient pixels to read")
            continue
        for i in range(imgpixs.shape[0]):
            rid = i + rowtrans
            for j in range(imgpixs.shape[1]):
                cid = j + coltrans
                pixval = imgpixs[i, j]
                # write the dimensions
                if output == "binary":
                    idxa = array('L',[cid, rid, tid])                           # sdb's array dimensions - L unsigned long
                    if t2id:
                        idxa = array('L',[ipath, irow, cid, rid, tid])
                    idxa.tofile(sys.stdout)
                    # write the data
                    for k in range(len(pixval)):
                        dt = bandtypes[k]
                        idxv = array(mapGdal2python('GDT_' + dt), [pixval[k]])
                        idxv.tofile(sys.stdout)
                elif output == "dcsv":
                    s = "{" + str(cid) + "," + str(rid) + "," + str(tid) + "} "
                    if t2id:
                        s = "{" + str(ipath) + "," + str(irow) + "," + str(cid) + "," + str(rid) + "," + str(tid) + "} "
                    for k in range(len(pixval)):
                        s += str(pixval[k]) + ','                               # NOTE: XXX s += str(pixval[k][0]) + ','
                    sys.stdout.write(s[0:-1] + "\n")
                elif output == "csv":
                    s = str(cid) + "," + str(rid) + "," + str(tid) + ","
                    if t2id:
                        s = str(ipath) + "," + str(irow) + "," + s
                    for k in range(len(pixval)):
                        s += str(pixval[k]) + ','                               # NOTE: XXX s += str(pixval[k][0]) + ','
                    sys.stdout.write(s[0:-1] + "\n")
                else:
                    logging.error("Unknown SciDB format: " + output)
                    sys.exit(0)

# TODO: Write script to split images into chunks and call "this" script

if __name__ == "__main__":
   main(sys.argv[1:])

