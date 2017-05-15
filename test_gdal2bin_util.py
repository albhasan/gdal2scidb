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
import logging
log = 'INFO'
logging.basicConfig(filename = 'log_gdal2bin_util.log', level = getattr(logging, log.upper(), None), format = '%(asctime)s %(levelname)s: %(message)s')
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
        #inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-11/LC82260682013101LGN01_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-04-27/LC82260682013117LGN01_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-13/LC82260682013133LGN01_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260682013149LGN00_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_cfmask_conf.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_cloud.tif"
        #inputFiles = "/home/scidb/MODIS/2010/MOD13Q1.A2010337.h12v10.005.2010355190043.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010177.h12v10.005.2010196020624.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010113.h12v10.005.2010133072929.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010225.h12v10.005.2010252053925.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010209.h12v10.005.2010239173903.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010161.h12v10.005.2010178143649.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010257.h12v10.005.2010282030406.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010241.h12v10.005.2010259062743.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010033.h12v10.005.2010050162915.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010305.h12v10.005.2010322173628.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010193.h12v10.005.2010212005018.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010145.h12v10.005.2010165175205.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010321.h12v10.005.2010339042846.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010129.h12v10.005.2010146170112.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010353.h12v10.005.2011006185024.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010273.h12v10.005.2010291065852.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010017.h12v10.005.2010036003008.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010097.h12v10.005.2010114150000.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010065.h12v10.005.2010084080913.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010289.h12v10.005.2010309022036.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010049.h12v10.005.2010067021119.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010001.h12v10.005.2010027070105.hdf /home/scidb/MODIS/2010/MOD13Q1.A2010081.h12v10.005.2010101105440.hdf"
        #
        #inputFiles = '/media/alber/fd2f2147-f07d-4a8a-9e17-715140f0e470/academicData/inpe/phdCienciaSistemaTerrestre/projects/proyectoDonato/data/MOD11A1.A2015127.h13v11.005.2015128103250.hdf'
        inputFiles = '/home/alber/Desktop/MOD13Q1.A2010081.h12v10.005.2010101105440.hdf'
        #
        #inputFiles = '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-14/LC82260682013165LGN00_sr_cloud.tif'
        #inputFiles = '/home/scidb/MODIS/2010/MOD13Q1.A2010081.h12v10.005.2010101105440.hdf'
        
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
        self.assertEqual(ymd2tid(20000102, 20000101, 8, True), -1)
        self.assertEqual(ymd2tid(20000108, 20000101, 8, True), -1)
        self.assertEqual(ymd2tid(20000110, 20000101, 8, True), -1)

        self.assertEqual(ymd2tid(20000101, 20000101, 16, True), 0)
        self.assertEqual(ymd2tid(20000117, 20000101, 16, True), 1)
        self.assertEqual(ymd2tid(20000202, 20000101, 16, True), 2)
        self.assertEqual(ymd2tid(20000102, 20000101, 16, True), -1)
        self.assertEqual(ymd2tid(20000116, 20000101, 16, True), -1)
        self.assertEqual(ymd2tid(20000118, 20000101, 16, True), -1)

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












        self.assertEqual('foo'.upper(), 'FOO')
if __name__ == '__main__':
	unittest.main()

