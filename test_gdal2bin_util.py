import unittest
import sys
import datetime
from gdal2bin_util import *

class TestStringMethods(unittest.TestCase):

	def test_upper(self):

		filepaths = "#/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260672013181LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260612013181LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260622013181LGN00_sr_cloud.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260612013181LGN00_cfmask.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260672013181LGN00_sr_band2.tif /home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260622013181LGN00_sr_band6.tif /this/must/fail/LC82260672013213ALA00_cfmask.tif /home/scidb/MODIS/2005/MOD13Q1.A2005353.h11v07.005.2008091034316.hdf /home/scidb/MODIS/2005/MOD13Q1.A2003353.h10v11.005.2008041120050.hdf /home/scidb/MODIS/2005/MOD13Q1.A2015353.h10v11.005.2016007192946.hdf"

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


		self.assertEqual('foo'.upper(), 'FOO')
if __name__ == '__main__':
	unittest.main()

