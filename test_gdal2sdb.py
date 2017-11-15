#test_gdal2sdb.py

import unittest
import sys
import datetime
from gdal2sdb import *


class TestClasses(unittest.TestCase):
    def test_ImageFile(self):
        imgf = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.assertEqual(imgf.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif')
        self.assertEqual(imgf.image, 'Landsat8OLI/TIRS Combined22606620150706')
        self.assertEqual(imgf.type, 'Landsat_tiered')
        self.assertEqual(imgf.sensor, 'OLI/TIRS Combined')
        self.assertEqual(imgf.satellite, 'Landsat8')
        self.assertEqual(imgf.level, 'Precision and Terrain Correction')
        self.assertEqual(imgf.path, '226')
        self.assertEqual(imgf.row, '066')
        self.assertEqual(imgf.acquisition, 20150706)
        self.assertEqual(imgf.processing, 20170407)
        self.assertEqual(imgf.collection, '01')
        self.assertEqual(imgf.category, 'Tier 1')
        self.assertEqual(imgf.stationId, '')
        self.assertEqual(imgf.archive, '')
        self.assertEqual(imgf.band, 'band03')
        self.assertEqual(imgf.product, 'sr')
        self.assertEqual(imgf.sname, 'LC08')
        # requires a real image and gdal
        imgf.getMetadata()
        self.assertEqual(imgf.driver, 'GeoTIFF')
        self.assertEqual(imgf.ncol, 7661)
        self.assertEqual(imgf.nrow, 7791)
        self.assertEqual(imgf.bandtype, ['Int16'])
        self.assertEqual(imgf.geotransform, (706785.0, 30.0, 0.0, -843885.0, 0.0, -30.0))

        imgf = ImageFile("/home/scidb/MODIS/2010/MOD13Q1.A2010241.h11v10.006.2015210102523.hdf")
        self.assertEqual(imgf.filepath, '/home/scidb/MODIS/2010/MOD13Q1.A2010241.h11v10.006.2015210102523.hdf')
        self.assertEqual(imgf.image, 'MOD13Q1111020100829')
        self.assertEqual(imgf.type, 'Modis')
        self.assertEqual(imgf.sensor, '13Q1')
        self.assertEqual(imgf.satellite, 'MOD')
        self.assertEqual(imgf.level, '')
        self.assertEqual(imgf.path, '11')
        self.assertEqual(imgf.row, '10')
        self.assertEqual(imgf.acquisition, 20100829)
        self.assertEqual(imgf.processing, 20150729)
        self.assertEqual(imgf.collection, '006')
        self.assertEqual(imgf.category, '')
        self.assertEqual(imgf.stationId, '')
        self.assertEqual(imgf.archive, '')
        self.assertEqual(imgf.band, '')
        self.assertEqual(imgf.product, '')
        self.assertEqual(imgf.sname, 'MOD13Q1')
        # requires a real image and gdal
        imgf.getMetadata()
        self.assertEqual(imgf.driver, 'Hierarchical Data Format Release 4')
        #self.assertEqual(imgf.ncol, 512)
        #self.assertEqual(imgf.nrow, 512)
        self.assertEqual(imgf.bandtype, ['Int16', 'Int16', 'UInt16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Byte'])
        self.assertEqual(imgf.geotransform, (0.0, 1.0, 0.0, 0.0, 0.0, 1.0))






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

