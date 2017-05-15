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
#
# find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013 -name 'LC822606*tif'
# find /home/scidb/MODIS -type f -name '*h12v10*'
#
# python gdal2bin_chunk.py "/home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_solar_zenith_band4.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_solar_azimuth_band4.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_radsat_qa.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_band1.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_pixel_qa.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_band4.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_band7.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_band3.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_band5.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_band2.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_cloud_qa.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sr_atmos_opacity.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sensor_zenith_band4.tif /home/alber/landsat/collection1/LE072310652016012501T1-SC20170407161252/LE07_L1TP_231065_20160125_20161015_01_T1_sensor_azimuth_band4.tif" 75 75 75 75
#
# Ubuntu uses an old version of numpy
# sudo easy_install --upgrade numpy
# sudo easy_install --upgrade scipy
################################################################################
def main(argv):
    parser = argparse.ArgumentParser(description = "Export GDAL images to the stdout using SciDB's binary format.")
    parser.add_argument("inputFiles", help = "List of images separated by spaces.")
    parser.add_argument("col", help = "Number of the column from where to start getting data.")
    parser.add_argument("row", help = "Number of the row from where to start getting data.")
    parser.add_argument("colbuf", help = "Number of additional columns to get data from.")
    parser.add_argument("rowbuf", help = "Number of additional rows to get data from.")
    parser.add_argument("coltrans", help = "Translation applied to the column index.")
    parser.add_argument("rowtrans", help = "Translation applied to the row index.")
    parser.add_argument("--d2tid", help = "Use the date to compute the time_id. Otherwise use the time-ordered cardinal position of the image in the inputFiles. Default = True", default = 'True')
    parser.add_argument("--log", help = "Log level. Default = WARNING", default = 'WARNING')
    #Get paramters
    args = parser.parse_args()
    inputFiles = args.inputFiles
    col = int(args.col)
    row = int(args.row)
    colbuf = int(args.colbuf)
    rowbuf = int(args.rowbuf)
    coltrans = int(args.coltrans)
    rowtrans = int(args.rowtrans)
    d2tid = args.d2tid in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
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
    files = sortFiles(inputFiles.split())
    # get files' metadata
    imgseries = set()                                                           # set of series of images
    filesmd = list()                                                            # list of metadata derived from file names
    for key,value in files.items():
        fmd = getFileNameMetadata(value)
        filesmd.append(fmd)
        imgseries.add(fmd['satellite'] + fmd['sensor']+ fmd['path'] + fmd['row'])
    # validation
    if len(imgseries) != 1:
        logging.error("Invalid number of time series of images: " + imgseries)
        sys.exit(0)
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
    #
    bandtypes = sum(bandtypes, []) if isinstance(bandtypes[0], list) else bandtypes
    # get time_id parameters
    tidparam = gettimeidparameters(filesmd[0]['sname'])
    # get pixels from each image    
    tid = -1
    for ifiles in imgfiles:
        if d2tid:
            tid = ymd2tid(int(ifiles[0][-8:]), int(tidparam['origin']), int(tidparam['period']), tidparam['yearly'])
        else:
            tid = tid + 1
        imgpixs = getPixelImages(ifiles[1], col, row, colbuf, rowbuf, -1)       # pixels of the bands of an image. A numpy.ndarray object
        for i in range(imgpixs.shape[0]): # rowbuf
            rid = i + rowtrans
            for j in range(imgpixs.shape[1]): # colbuf
                cid = j + coltrans
                pixval = imgpixs[i, j]
                # write the dimensions as binary
                idxa = array('L',[cid, rid, tid])                               # sdb's array dimensions - L unsigned long
                idxa.tofile(sys.stdout)
                # write the data as binary
                for k in range(len(pixval)):
                    dt = bandtypes[k]
                    idxv = array(mapGdal2python('GDT_' + dt), [pixval[k]])
                    idxv.tofile(sys.stdout)
    

    
if __name__ == "__main__":
   main(sys.argv[1:])

