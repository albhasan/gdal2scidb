#!/usr/bin/env python
#test_gdal2scidb.py
import os
import sys
import unittest
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gdal2scidb as g2s

class gdal2sdb_testCase(unittest.TestCase):
    def setUp(self):
        self.inputFiles1 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif"
        self.inputFiles2 = "/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band1.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-01-11/LC08_L1GT_226064_20150111_20170414_01_T2_sensor_azimuth_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band3.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sr_band4.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-11-11/LC08_L1TP_226064_20151111_20170402_01_T2_sensor_azimuth_band4.tif"
        self.inputFiles3 = "/home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140330_20170424_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140314_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140415_20170423_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150112_20170415_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160131_20170330_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160319_20170328_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20131224_20170427_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150301_20170412_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20130412_20170505_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150418_20170409_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140210_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20150128_20170413_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20130514_20170504_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140226_20170425_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20140125_20170426_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20160216_20170329_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20151230_20170331_01_T2_B1.TIF /home/alber/Documents/data/LANDSAT/sample/LC08_L1GT_233066_20141211_20170416_01_T2_B1.TIF"
        self.inputFiles4 = "/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v07.006.2015149070621.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v08.006.2015149070549.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v09.006.2015149070546.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v07.006.2015149070600.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v08.006.2015149070652.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v09.006.2015149070653.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v10.006.2015149070617.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v11.006.2015149071707.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h11v07.006.2015149070608.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h11v08.006.2015149070644.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v07.006.2015149070621.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v08.006.2015149070549.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v09.006.2015149070546.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v07.006.2015149070600.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v08.006.2015149070652.hdf /dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h10v09.006.2015149070653.hdf"
    #def tearDown(self):


class ImageFile_testCase(gdal2sdb_testCase):
    """ Test ImageFile objects """
    def test_creation_landsat(self):
        imgf = g2s.ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif")
        self.assertEqual(imgf.filepath, '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectanceC1/2015/2015-07-06/LC08_L1TP_226066_20150706_20170407_01_T1_sr_band3.tif')
        self.assertEqual(imgf.image, 'Landsat8OLI/TIRS-Combined22606620150706')
        self.assertEqual(imgf.type, 'Landsat_tiered')
        self.assertEqual(imgf.sensor, 'OLI/TIRS-Combined')
        self.assertEqual(imgf.satellite, 'Landsat8')
        self.assertEqual(imgf.level, 'L1TP')
        self.assertEqual(imgf.path, '226')
        self.assertEqual(imgf.row, '066')
        self.assertEqual(imgf.acquisition, 20150706)
        self.assertEqual(imgf.processing, 20170407)
        self.assertEqual(imgf.collection, '01')
        self.assertEqual(imgf.category, 'T1')
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
        imgf = g2s.ImageFile("/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-05-29/LC82260612013149LGN00_sr_band2.tif")
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
        imgf = g2s.ImageFile("/home/scidb/MODIS/2010/MOD13Q1.A2010241.h11v10.006.2015210102523.hdf")
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
        ifc = g2s.ImageFileCol(filepaths)
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
            ifc = g2s.ImageFileCol(filepaths)
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
    def test_creation_landsat(self):
        """ Test object creation """
        img = g2s.Image(self.inputFiles1.split(" "))
        self.assertEqual(img.id, "Landsat8_L1GT_OLI/TIRS-Combined_226_064_20150111")
        self.assertRaises(ValueError, g2s.Image, self.inputFiles2.split(" "))
        self.assertRaises(ValueError, g2s.Image, self.inputFiles3.split(" "))
    def test_creation_modis(self):
        self.assertRaises(ValueError, g2s.Image, self.inputFiles4.split(" "))
    def test_tid_modis(self):
        img1 = g2s.Image(["/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2002201.h09v07.006.2015149070621.hdf"])
        self.assertEqual(img1.tid(), 12)
        img2 = g2s.Image(["/dados1/modisOriginal/MYD13Q1.A2015009.h10v11.006.2015295082855.hdf"])
        self.assertEqual(img2.tid(), 299)
        #
        MYD_imgs = "MYD13Q1.A2002201.h09v07.006.2015149070621.hdf MYD13Q1.A2002217.h09v07.006.2015150072435.hdf MYD13Q1.A2002233.h09v07.006.2015150082506.hdf MYD13Q1.A2002249.h09v07.006.2015150213455.hdf MYD13Q1.A2002265.h09v07.006.2015151112240.hdf".split(" ")
        MYD_tids = range(12, 12 + len(MYD_imgs))
        for i in range(0, len(MYD_imgs)):
            img = g2s.Image([MYD_imgs[i]])
            self.assertEqual(img.tid(), MYD_tids[i])
        MYD_imgs = "/net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003009.h09v07.006.2015154120433.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003025.h09v07.006.2015154130406.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003041.h09v07.006.2015155183029.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003057.h09v07.006.2015157002919.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003073.h09v07.006.2015157003709.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003089.h09v07.006.2015157051115.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003105.h09v07.006.2015158152139.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003121.h09v07.006.2015158153743.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003137.h09v07.006.2015158153805.hdf /net/150.163.2.38/dados1/modisOriginal/MYD13Q1/MYD13Q1.A2003153.h09v07.006.2015158183627.hdf".split(" ")
        MYD_tids = range(23, 23 + len(MYD_imgs))
        for i in range(0, len(MYD_imgs)):
            img = g2s.Image([MYD_imgs[i]])
            self.assertEqual(img.tid(), MYD_tids[i])
        MOD_imgs = "/dados1/modisOriginal/MOD13Q1.A2000049.h09v07.006.2015136104539.hdf /dados1/modisOriginal/MOD13Q1.A2000065.h09v07.006.2015136021937.hdf /dados1/modisOriginal/MOD13Q1.A2000081.h09v07.006.2015136040647.hdf /dados1/modisOriginal/MOD13Q1.A2000097.h09v07.006.2015136040649.hdf".split(" ")
        MOD_tids = range(3, 3 + len(MOD_imgs))
        for i in range(0, len(MOD_imgs)):
            img = g2s.Image([MOD_imgs[i]])
            self.assertEqual(img.tid(), MOD_tids[i])



class ImageCol_TestCase(gdal2sdb_testCase):
    """ Test ImageCol objects  """
    def test_iterate(self):
        """ is the iterator re-setting? """
        imgcol = g2s.ImageCol(self.inputFiles1.split(" "))
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
            ic = g2s.ImageCol(filepaths)
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
    def test_landsat(self):
        infiles = '/home/scidb/LANDSAT8/SurfaceReflectanceC1/2015/2015-06-22/LC08_L1TP_224066_20150622_20170407_01_T1_sr_band1.tif /home/scidb/LANDSAT8/SurfaceReflectanceC1/2015/2015-03-16/LC08_L1GT_224066_20150316_20170412_01_T2_sr_band1.tif'
        self.assertRaises(AssertionError, g2s.ImageSeries, infiles.split(" "))
        g2s.ImageSeries(infiles.split(" "), True)
    def test_iterate(self):
        """ is the iterator re-setting? """
        imgser = g2s.ImageSeries(self.inputFiles3.split(" "))
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
            iser = g2s.ImageSeries(filepaths)
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
