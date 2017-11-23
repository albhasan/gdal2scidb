#test_gdal2sdb.py

import unittest
import sys
import datetime
from gdal2sdb import *


# TODO:
# - 

def suite():
    suite1 = unittest.TestLoader().loadTestsFromTestCase(ImageFileTestCase)
    suite1 = unittest.TestLoader().loadTestsFromTestCase(ImageFileColTestCase)
    #return suite
    #suite1 = module1.TheTestSuite()
    #suite2 = module2.TheTestSuite()
    alltests = unittest.TestSuite([suite1, suite2])
    return alltests



class ImageFile_testCase(unittest.TestCase):
    def setUp(self):
        self.ifLandsat = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.ifLandsatOld = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band2.tif")
        self.ifModis   = ImageFile("/home/scidb/MODIS/2010/MOD13Q1.A2010241.h11v10.006.2015210102523.hdf")
    def tearDown(self):
        self.ifLandsat = None
        self.ifModis = None
    def test_creation_landsat(self):
        #imgf = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.assertEqual(self.ifLandsat.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif')
        self.assertEqual(self.ifLandsat.image, 'Landsat8OLI/TIRS Combined22606620150706')
        self.assertEqual(self.ifLandsat.type, 'Landsat_tiered')
        self.assertEqual(self.ifLandsat.sensor, 'OLI/TIRS Combined')
        self.assertEqual(self.ifLandsat.satellite, 'Landsat8')
        self.assertEqual(self.ifLandsat.level, 'Precision and Terrain Correction')
        self.assertEqual(self.ifLandsat.path, '226')
        self.assertEqual(self.ifLandsat.row, '066')
        self.assertEqual(self.ifLandsat.acquisition, 20150706)
        self.assertEqual(self.ifLandsat.processing, 20170407)
        self.assertEqual(self.ifLandsat.collection, '01')
        self.assertEqual(self.ifLandsat.category, 'Tier 1')
        self.assertEqual(self.ifLandsat.stationId, '')
        self.assertEqual(self.ifLandsat.archive, '')
        self.assertEqual(self.ifLandsat.band, 'band03')
        self.assertEqual(self.ifLandsat.product, 'sr')
        self.assertEqual(self.ifLandsat.sname, 'LC08')
        # requires a real image and gdal
        #self.ifLandsat.getMetadata()
        #self.assertEqual(self.ifLandsat.driver, 'GeoTIFF')
        #self.assertEqual(self.ifLandsat.ncol, 7661)
        #self.assertEqual(self.ifLandsat.nrow, 7791)
        #self.assertEqual(self.ifLandsat.bandtype, ['Int16'])
        #self.assertEqual(self.ifLandsat.geotransform, (706785.0, 30.0, 0.0, -843885.0, 0.0, -30.0))
    def test_creation_landsatOld(self):
        #imgf = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.assertEqual(self.ifLandsatOld.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band2.tif')
        self.assertEqual(self.ifLandsatOld.image, 'Landsat8OLI/TIRS Combined22606120130529')
        self.assertEqual(self.ifLandsatOld.type, 'Landsat_untiered')
        self.assertEqual(self.ifLandsatOld.sensor, 'OLI/TIRS Combined')
        self.assertEqual(self.ifLandsatOld.satellite, 'Landsat8')
        self.assertEqual(self.ifLandsatOld.level, '')
        self.assertEqual(self.ifLandsatOld.path, '226')
        self.assertEqual(self.ifLandsatOld.row, '061')
        self.assertEqual(self.ifLandsatOld.acquisition, 20130529)
        self.assertEqual(self.ifLandsatOld.processing, 0)
        self.assertEqual(self.ifLandsatOld.collection, '')
        self.assertEqual(self.ifLandsatOld.category, '')
        self.assertEqual(self.ifLandsatOld.stationId, 'LGN')
        self.assertEqual(self.ifLandsatOld.archive, '00')
        self.assertEqual(self.ifLandsatOld.band, 'band02')
        self.assertEqual(self.ifLandsatOld.product, 'sr')
        self.assertEqual(self.ifLandsatOld.sname, 'LC08')
    def test_creation_modis(self):
        self.assertEqual(self.ifModis.filepath, '/home/scidb/MODIS/2010/MOD13Q1.A2010241.h11v10.006.2015210102523.hdf')
        self.assertEqual(self.ifModis.image, 'MOD13Q1111020100829')
        self.assertEqual(self.ifModis.type, 'Modis')
        self.assertEqual(self.ifModis.sensor, '13Q1')
        self.assertEqual(self.ifModis.satellite, 'MOD')
        self.assertEqual(self.ifModis.level, '')
        self.assertEqual(self.ifModis.path, '11')
        self.assertEqual(self.ifModis.row, '10')
        self.assertEqual(self.ifModis.acquisition, 20100829)
        self.assertEqual(self.ifModis.processing, 20150729)
        self.assertEqual(self.ifModis.collection, '006')
        self.assertEqual(self.ifModis.category, '')
        self.assertEqual(self.ifModis.stationId, '')
        self.assertEqual(self.ifModis.archive, '')
        self.assertEqual(self.ifModis.band, '')
        self.assertEqual(self.ifModis.product, '')
        self.assertEqual(self.ifModis.sname, 'MOD13Q1')
        # requires a real image and gdal
        #self.ifModis.getMetadata()
        #self.assertEqual(self.ifModis.driver, 'Hierarchical Data Format Release 4')
        #self.assertEqual(self.ifModis.ncol, 512)
        #self.assertEqual(self.ifModis.nrow, 512)
        #self.assertEqual(self.ifModis.bandtype, ['Int16', 'Int16', 'UInt16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Byte'])
        #self.assertEqual(self.ifModis.geotransform, (0.0, 1.0, 0.0, 0.0, 0.0, 1.0))



class ImageFileCol_testCase(unittest.TestCase):
    def setUp(self):
        inputFiles1 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif"
        inputFiles2 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sensor_azimuth_band4.tif"
        self.ifcLandsat1 = ImageFileCol(inputFiles1.split(" "))
        self.ifcLandsat2 = ImageFileCol(inputFiles2.split(" "))
    def tearDown(self):
        self.ifcLandsat1 = None
        self.ifcLandsat2 = None
    def iterate(self):
        count = 0
        for imgf in self.ifcLandsat1:
            count = count + 1
        self.assertEqual(count, 4)
        # is iterator re-setting?
        count = 0
        for imgf in self.ifcLandsat1:
            count = count + 1
        self.assertEqual(count, 4)
        #TODO: is iterator ordered?



class ImageTestCase(unittest.TestCase):
    def setUp(self):
        inputFiles1 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif"
        self.iLandsat1 = Image(inputFiles1.split(" "))
    def tearDown(self):
        self.iLandsat1 = None
    def test_creation_landsat(self):
        self.assertEqual(self.iLandsat1.id, "Landsat8OLI/TIRS Combined22606420150111")



class ImageColTestCase(unittest.TestCase):
    def setUp(self):
        inputFiles3 = "/home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140330_20170424_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140314_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140415_20170423_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150112_20170415_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160131_20170330_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160319_20170328_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20131224_20170427_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150301_20170412_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20130412_20170505_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150418_20170409_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140210_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150128_20170413_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20130514_20170504_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140226_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140125_20170426_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160216_20170329_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20151230_20170331_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20141211_20170416_01_T2_B1.TIF"
        filepaths = inputFiles3.split(" ")
        self.imgcol = ImageCol(filepaths)
    def tearDown(self):
        self.imgser = None
    def iterate(self):
        count = 0
        for img in self.imgcol:
            count = count + 1
        self.assertEqual(count, 4)
        # is iterator re-setting?
        count = 0
        for imgf in self.imgcol:
            count = count + 1
        self.assertEqual(count, 4)
        #TODO: is iterator ordered?



#class ImageSeriesTestCase(unittest.TestCase):
#    def setUp(self):
#    def tearDown(self):









if __name__ == '__main__':
	unittest.main()

