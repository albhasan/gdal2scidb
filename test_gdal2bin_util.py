# mandatory
import unittest
import sys
import datetime
from gdal2bin_util import *
#-------------------------------------
# test
import collections
import os
import re
import sys
import numpy
import datetime
import struct
from array import array
import logging
log = 'INFO'
logging.basicConfig(filename = 'log_gdal2bin_test.log', level = getattr(logging, log.upper(), None), format = '%(asctime)s %(levelname)s: %(message)s')
#-------------------------------------
col = 0
row = 0
colbuf = 75
rowbuf = 75
coltrans = 48000
rowtrans = 48000
d2tid = False
#-------------------------------------

logging.info("test_gdal2bin_util")

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260672013181LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260612013181LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260622013181LGN00_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260612013181LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260672013181LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260622013181LGN00_sr_band6.tif /this/must/fail/LC82260672013213ALA00_cfmask.tif /home/scidb/MODIS/2005/MOD13Q1.A2005353.h11v07.005.2008091034316.hdf /home/scidb/MODIS/2005/MOD13Q1.A2003353.h10v11.005.2008041120050.hdf /home/scidb/MODIS/2005/MOD13Q1.A2015353.h10v11.005.2016007192946.hdf"

        inputFiles = '/home/alber/Desktop/MOD13Q1.A2010081.h12v10.005.2010101105440.hdf'

        col = 0
        row = 0
        colbuf = 75
        rowbuf = 75
        coltrans = 48000
        rowtrans = 48000

        self.assertEqual(date2ydoy(datetime.date(2007, 12, 31)), 2007365)
        self.assertEqual(date2ydoy(datetime.date(2007, 1, 1)), 2007001)
        self.assertEqual(date2ydoy(datetime.date(2000, 12, 31)), 2000366)
        self.assertEqual(date2ydoy(datetime.date(2000, 2, 29)), 2000060)
        self.assertEqual(date2ydoy(datetime.date(2001, 3, 1)), 2001060)

        self.assertEqual(ydoy2ymd(2007365), 20071231)
        self.assertEqual(ydoy2ymd(2007001), 20070101)
        self.assertEqual(ydoy2ymd(2000366), 20001231)
        self.assertEqual(ydoy2ymd(2000060), 20000229)
        self.assertEqual(ydoy2ymd(2001060), 20010301)

        self.assertEqual(ymd2ydoy(20071231), 2007365)
        self.assertEqual(ymd2ydoy(20070101), 2007001)
        self.assertEqual(ymd2ydoy(20001231), 2000366)
        self.assertEqual(ymd2ydoy(20000229), 2000060)
        self.assertEqual(ymd2ydoy(20010301), 2001060)



        self.assertEqual(ymd2tid(20000101, 20000101, 8, True), 0)
        self.assertEqual(ymd2tid(20000109, 20000101, 8, True), 1)
        self.assertEqual(ymd2tid(20000117, 20000101, 8, True), 2)
        self.assertEqual(ymd2tid(20000102, 20000101, 8, True), 0)
        self.assertEqual(ymd2tid(20000108, 20000101, 8, True), 0)
        self.assertEqual(ymd2tid(20000110, 20000101, 8, True), 0)

        self.assertEqual(ymd2tid(20000101, 20000101, 16, True), 0)
        self.assertEqual(ymd2tid(20000117, 20000101, 16, True), 1)
        self.assertEqual(ymd2tid(20000202, 20000101, 16, True), 2)
        self.assertEqual(ymd2tid(20000102, 20000101, 16, True), 0)
        self.assertEqual(ymd2tid(20000116, 20000101, 16, True), 0)
        self.assertEqual(ymd2tid(20000118, 20000101, 16, True), 0)

        self.assertEqual(ymd2tid(20000101, 20000101, 16, True), 0)
        self.assertEqual(ymd2tid(20001218, 20000101, 16, True), 22)
        self.assertEqual(ymd2tid(20010101, 20000101, 16, True), 23)
        self.assertEqual(ymd2tid(20011219, 20000101, 16, True), 45)
        self.assertEqual(ymd2tid(20020101, 20000101, 16, True), 46)


        # tid2ymd and ymd2tid are complementary
        ori = 20000101
        per = 16
        y = True
        self.assertEqual(tid2ymd(ymd2tid(20000101, ori, per, y), ori, per, y), 20000101)
        self.assertEqual(tid2ymd(ymd2tid(20001218, ori, per, y), ori, per, y), 20001218)
        self.assertEqual(tid2ymd(ymd2tid(20010101, ori, per, y), ori, per, y), 20010101)
        self.assertEqual(tid2ymd(ymd2tid(20011219, ori, per, y), ori, per, y), 20011219)
        self.assertEqual(tid2ymd(ymd2tid(20020101, ori, per, y), ori, per, y), 20020101)


        inputFiles = '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260672013181LGN00_cfmask.tif'
        imgseriesmd = []
        for f in inputFiles.split():
            imgseriesmd.append(getFileNameMetadata(f))
        self.assertEqual(len(imgseriesmd), 1)




        inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-08-17/LC82260612013229LGN00_sr_band7.tif"
        files = sortFiles(inputFiles.split())
        imgseries = set()                                                           # set of series of images
        filesmd = list()                                                            # list of metadata derived from file names
        for key,value in files.items():
            fmd = getFileNameMetadata(value)
            filesmd.append(fmd)
            imgseries.add(fmd['satellite'] + fmd['sensor']+ fmd['path'] + fmd['row'])
        imgfiles = imgseries2imgfp(filesmd)                                         # List [img, [filepaths]]
        self.assertEqual(len(imgfiles), 2)


        # test on server


import sys
import argparse
import logging
import numpy
from array import array
from gdal2bin_util import *
#find /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17 -type f -name 'LC08_L1TP_226064_20140617_20170421_01_T1*'
inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_savi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_ndvi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_solar_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_aerosol.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_MASK.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_pixel_qa.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sensor_zenith_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_solar_zenith_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_evi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_radsat_qa.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2014/2014-06-17/LC08_L1TP_226064_20140617_20170421_01_T1_sensor_azimuth_band4.tif"

col = 0
row = 0
colbuf = 40
rowbuf = 40
coltrans = 0
rowtrans = 0
d2tid = True
d2att = True
t2id = True
output = 'binary'
log = 'DEBUG'
####################################################
# CONFIG
####################################################
gdal.UseExceptions()
# log
numeric_loglevel = getattr(logging, log.upper(), None)
#if not isinstance(numeric_loglevel, int):
#        raise ValueError('Invalid log level: %s' % log)

####################################################
# SCRIPT
#---------------------------------------------------
# [1] image == [n] bands of the same path/row and date
# [1] image series == [n] images of the same satellite, sensor, path and row but different acquisition time
# [1] band  == [1]file
# [1] file  == [n] bands
####################################################
# sort files by image-path/row-band
files = sortFiles(inputFiles.split())# sortFiles(inputFiles)
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
        #sys.exit(0)

imgtype = imgseries.pop()
# NOTE: assume all the images belong to the same path & row or TILE!!!!
ipath = fmd['path']
irow = fmd['row']
# build list of images and filepaths
imgfiles = imgseries2imgfp(filesmd)                                         # List [img, [filepaths]]
# validation
if len(imgfiles) == 0:
        logging.error("No images found")
        #sys.exit(0)
nimg = len(imgfiles[0][1])
for i in range(1, len(imgfiles)):
        if nimg != len(imgfiles[i][1]):
                logging.error("Inconsistent number of files in images: " + imgfiles[i][0])
                #sys.exit(0)
# get band's datatypes from of a single image
bandtypes = []                                                              # GDAL band types of an image's bands
for fp in imgfiles[0][1]:
        bandtypes.append(getGdalMetadata(fp)['bandtype'])

bandtypes = sum(bandtypes, []) if isinstance(bandtypes[0], list) else bandtypes
logging.info("Bandtypes: " + str(bandtypes))
# get time_id transformation parameters
tidparam = gettimeidparameters(filesmd[0]['sname'])
tid = -1
ifiles = imgfiles[0]
tid = ymd2tid(int(ifiles[0][-8:]), int(tidparam['origin']), int(tidparam['period']), tidparam['yearly']) # forget
d2att = getFileNameMetadata(ifiles[1][0])['acquisition']
imgpixs = getPixelImages(ifiles[1], col, row, colbuf, rowbuf, -1)       # pixels of the bands of an image. A numpy.ndarray object

i = range(imgpixs.shape[0])[0]









if __name__ == '__main__':
	unittest.main()

