#test_gdal2sdb.py

import unittest
import sys
import datetime
from gdal2sdb import *


class TestClasses(unittest.TestCase):
    def test_ImageFile(self):
        imgf = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.assertEqual(imgf.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif')
        self.assertEqual(imgf.path, '226')
        self.assertEqual(imgf.row,  '066')
        #TODO: other tests MODIS SENTINEL
    def test_ImageFileCol(self):
        inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif"
        imgfc = ImageFileCol(inputFiles.split(" "))
        nimg = imgfc.getImages()
        self.assertEqual(len(nimg), 1)


        inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sensor_azimuth_band4.tif"
        imgfc = ImageFileCol(inputFiles.split(" "))
        nimg = imgfc.getImages()
        self.assertEqual(len(nimg), 2)



if __name__ == '__main__':
	unittest.main()

