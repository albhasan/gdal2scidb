#!/usr/bin/env python
#test_gdal2sdb.py

import unittest
import sys
import datetime
from gdal2sdb import *


# TODO:
# -


class gdal2sdb_testCase(unittest.TestCase):
    def setUp(self):
        self.inputFiles1 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif"
        self.inputFiles2 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sensor_azimuth_band4.tif"
        self.inputFiles3 = "/home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140330_20170424_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140314_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140415_20170423_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150112_20170415_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160131_20170330_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160319_20170328_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20131224_20170427_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150301_20170412_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20130412_20170505_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150418_20170409_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140210_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150128_20170413_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20130514_20170504_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140226_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140125_20170426_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160216_20170329_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20151230_20170331_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20141211_20170416_01_T2_B1.TIF"
    #def tearDown(self):


class ImageFile_testCase(gdal2sdb_testCase):
    """ Test ImageFile objects """
    def test_creation_landsat(self):
        imgf = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.assertEqual(imgf.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif')
        self.assertEqual(imgf.image, 'Landsat8OLI/TIRS-Combined22606620150706')
        self.assertEqual(imgf.type, 'Landsat_tiered')
        self.assertEqual(imgf.sensor, 'OLI/TIRS-Combined')
        self.assertEqual(imgf.satellite, 'Landsat8')
        self.assertEqual(imgf.level, 'Precision-and-Terrain-Correction')
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
        #self.imgf.getMetadata()
        #self.assertEqual(imgf.driver, 'GeoTIFF')
        #self.assertEqual(imgf.ncol, 7661)
        #self.assertEqual(imgf.nrow, 7791)
        #self.assertEqual(imgf.bandtype, ['Int16'])
        #self.assertEqual(imgf.geotransform, (706785.0, 30.0, 0.0, -843885.0, 0.0, -30.0))
    def test_creation_landsatOld(self):
        """ Test the creation of objects of the pre-tier landsat images """
        imgf = ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band2.tif")
        self.assertEqual(imgf.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band2.tif')
        self.assertEqual(imgf.image, 'Landsat8OLI/TIRS-Combined22606120130529')
        self.assertEqual(imgf.type, 'Landsat_untiered')
        self.assertEqual(imgf.sensor, 'OLI/TIRS-Combined')
        self.assertEqual(imgf.satellite, 'Landsat8')
        self.assertEqual(imgf.level, '')
        self.assertEqual(imgf.path, '226')
        self.assertEqual(imgf.row, '061')
        self.assertEqual(imgf.acquisition, 20130529)
        self.assertEqual(imgf.processing, 0)
        self.assertEqual(imgf.collection, '')
        self.assertEqual(imgf.category, '')
        self.assertEqual(imgf.stationId, 'LGN')
        self.assertEqual(imgf.archive, '00')
        self.assertEqual(imgf.band, 'band02')
        self.assertEqual(imgf.product, 'sr')
        self.assertEqual(imgf.sname, 'LC08')
    def test_creation_modis(self):
        """ Test the creation of MODIS objects """
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
        #self.imgf.getMetadata()
        #self.assertEqual(imgf.driver, 'Hierarchical Data Format Release 4')
        #self.assertEqual(imgf.ncol, 512)
        #self.assertEqual(imgf.nrow, 512)
        #self.assertEqual(imgf.bandtype, ['Int16', 'Int16', 'UInt16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Int16', 'Byte'])
        #self.assertEqual(imgf.geotransform, (0.0, 1.0, 0.0, 0.0, 0.0, 1.0))



class ImageFileCol_testCase(gdal2sdb_testCase):
    """ Test ImageFileCol objects  """
    def test_iterate(self):
        """ Is iterator re-setting? """
        filepaths = self.inputFiles1.split(" ")
        ifc = ImageFileCol(filepaths)
        count = 0
        for imgf in ifc:
            count = count + 1
        self.assertEqual(count, len(filepaths))
        count = 0
        count = 0
        for imgf in ifc:
            count = count + 1
        self.assertEqual(count, len(filepaths))
    def test_iterate_order(self):
        """ Are the ImageFileCol objects iterated in order?  """
        filepathsList = [self.inputFiles1.split(" "), self.inputFiles2.split(" "), self.inputFiles3.split(" ")]
        for filepaths in filepathsList:
            ifc = ImageFileCol(filepaths)
            first = True
            last_id          = ''
            for imgf in ifc:
                if first:
                    last_id = imgf.id
                    first = False
                else:
                    self.assertTrue(imgf.id >= last_id)
                    last_id = imgf.id



class Image_TestCase(gdal2sdb_testCase):
    """ Test Image objects  """
    #TODO:
    # - what is the ID of images???? Should "Systematic-Terrain-Correction_OLI" be included? Sorting is done using the ID
    # - create tests for MODIS and old landsat
    def test_creation_landsat(self):
        """ Test object creation """
        img = Image(self.inputFiles1.split(" "))
        self.assertEqual(img.id, "Landsat8_Systematic-Terrain-Correction_OLI/TIRS-Combined_226_064_20150111")
        self.assertRaises(ValueError, Image, self.inputFiles2.split(" "))
        self.assertRaises(ValueError, Image, self.inputFiles3.split(" "))



class ImageCol_TestCase(gdal2sdb_testCase):
    """ Test ImageCol objects  """
    def test_iterate(self):
        """ is the iterator re-setting? """
        imgcol = ImageCol(self.inputFiles1.split(" "))
        count = 0
        for img in imgcol:
            count = count + 1
        self.assertEqual(count, 1)
        count = 0
        for img in imgcol:
            count = count + 1
        self.assertEqual(count, 1)
    def test_iterate_order(self):
        """ Is iterator ordered? """
        filepathsList = [self.inputFiles1.split(" "), self.inputFiles2.split(" "), self.inputFiles3.split(" ")]
        for filepaths in filepathsList:
            ic = ImageCol(filepaths)
            first = True
            last_id   = ''
            for img in ic:
                if first:
                    last_id          = img.id
                    first = False
                else:
                    self.assertTrue(img.id          >= last_id)
                    last_id          = img.id



class ImageSeries_TestCase(gdal2sdb_testCase):
    """ Test ImageSeries objects  """
    def test_iterate(self):
        """ is the iterator re-setting? """
        imgser = ImageSeries(self.inputFiles3.split(" "))
        count1 = 0
        for img in imgser:
            count1 = count1 + 1
        count2 = 0
        for img in imgser:
            count2 = count2 + 1
        self.assertEqual(count1, count2)
    def test_iterate_order(self):
        """ Is iterator ordered? """
        filepathsList = [self.inputFiles3.split(" ")]
        for filepaths in filepathsList:
            iser = ImageSeries(filepaths)
            first = True
            last_id   = ''
            for img in iser:
                if first:
                    last_id          = img.id
                    first = False
                else:
                    self.assertTrue(img.id          >= last_id)
                    last_id          = img.id



#class ImageSeriesTestCase(unittest.TestCase):
#    def setUp(self):
#    def tearDown(self):



#inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_radsat_qa.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_MASK.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_pixel_qa.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_evi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sensor_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_ndvi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_aerosol.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sensor_zenith_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_solar_zenith_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band7.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_solar_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_savi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band6.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band5.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_pixel_qa.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_solar_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_ndvi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_savi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_solar_zenith_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_MASK.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sensor_zenith_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_evi.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_radsat_qa.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_aerosol.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sensor_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-27/LC08_L1TP_226064_20151127_20170401_01_T2_sr_band7.tif"
#imgfc = ImageFileCol(inputFiles.split(" "))
#imglist = imgfc.getImages()
#img0 = imglist[0]
#img1 = imglist[1]
#
#imgslist = imgfc.getImageSeries()
#imgslist    
#
#imgslist = ImageSeries(["/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band6.tif"])
#imgslist
#imgslist.id
#imgslist.filepaths
#
#inputFiles = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band6.tif"
#imgf = ImageFile([inputFiles])


if __name__ == '__main__':
	unittest.main()
