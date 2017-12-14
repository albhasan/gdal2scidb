#!/usr/bin/env python
#test_g2butil.py
import os
import sys
import unittest
import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import g2butil

class g2butil_testCase(unittest.TestCase):
    def test_upper(self):
        inputFiles = '/home/alber/Desktop/MOD13Q1.A2010081.h12v10.005.2010101105440.hdf'

        self.assertEqual(g2butil.date2ydoy(datetime.date(2007, 12, 31)), 2007365)
        self.assertEqual(g2butil.date2ydoy(datetime.date(2007, 1, 1)), 2007001)
        self.assertEqual(g2butil.date2ydoy(datetime.date(2000, 12, 31)), 2000366)
        self.assertEqual(g2butil.date2ydoy(datetime.date(2000, 2, 29)), 2000060)
        self.assertEqual(g2butil.date2ydoy(datetime.date(2001, 3, 1)), 2001060)

        self.assertEqual(g2butil.ydoy2ymd(2007365), 20071231)
        self.assertEqual(g2butil.ydoy2ymd(2007001), 20070101)
        self.assertEqual(g2butil.ydoy2ymd(2000366), 20001231)
        self.assertEqual(g2butil.ydoy2ymd(2000060), 20000229)
        self.assertEqual(g2butil.ydoy2ymd(2001060), 20010301)

        self.assertEqual(g2butil.ymd2ydoy(20071231), 2007365)
        self.assertEqual(g2butil.ymd2ydoy(20070101), 2007001)
        self.assertEqual(g2butil.ymd2ydoy(20001231), 2000366)
        self.assertEqual(g2butil.ymd2ydoy(20000229), 2000060)
        self.assertEqual(g2butil.ymd2ydoy(20010301), 2001060)

        self.assertEqual(g2butil.ymd2tid(20000101, 20000101, 8, True), 0)
        self.assertEqual(g2butil.ymd2tid(20000109, 20000101, 8, True), 1)
        self.assertEqual(g2butil.ymd2tid(20000117, 20000101, 8, True), 2)
        self.assertEqual(g2butil.ymd2tid(20000102, 20000101, 8, True), 0)
        self.assertEqual(g2butil.ymd2tid(20000108, 20000101, 8, True), 0)
        self.assertEqual(g2butil.ymd2tid(20000110, 20000101, 8, True), 0)

        self.assertEqual(g2butil.ymd2tid(20000101, 20000101, 16, True), 0)
        self.assertEqual(g2butil.ymd2tid(20000117, 20000101, 16, True), 1)
        self.assertEqual(g2butil.ymd2tid(20000202, 20000101, 16, True), 2)
        self.assertEqual(g2butil.ymd2tid(20000102, 20000101, 16, True), 0)
        self.assertEqual(g2butil.ymd2tid(20000116, 20000101, 16, True), 0)
        self.assertEqual(g2butil.ymd2tid(20000118, 20000101, 16, True), 0)

        self.assertEqual(g2butil.ymd2tid(20000101, 20000101, 16, True), 0)
        self.assertEqual(g2butil.ymd2tid(20001218, 20000101, 16, True), 22)
        self.assertEqual(g2butil.ymd2tid(20010101, 20000101, 16, True), 23)
        self.assertEqual(g2butil.ymd2tid(20011219, 20000101, 16, True), 45)
        self.assertEqual(g2butil.ymd2tid(20020101, 20000101, 16, True), 46)

        # tid2ymd and ymd2tid are complementary
        ori = 20000101
        per = 16
        y = True
        self.assertEqual(g2butil.tid2ymd(g2butil.ymd2tid(20000101, ori, per, y), ori, per, y), 20000101)
        self.assertEqual(g2butil.tid2ymd(g2butil.ymd2tid(20001218, ori, per, y), ori, per, y), 20001218)
        self.assertEqual(g2butil.tid2ymd(g2butil.ymd2tid(20010101, ori, per, y), ori, per, y), 20010101)
        self.assertEqual(g2butil.tid2ymd(g2butil.ymd2tid(20011219, ori, per, y), ori, per, y), 20011219)
        self.assertEqual(g2butil.tid2ymd(g2butil.ymd2tid(20020101, ori, per, y), ori, per, y), 20020101)

        inputFiles = '/home/scidb/LANDSAT/landsat8Original/SurfaceReflectance/2013/2013-06-30/LC82260672013181LGN00_cfmask.tif'
        imgseriesmd = []
        for f in inputFiles.split():
            imgseriesmd.append(g2butil.getFileNameMetadata(f))
        self.assertEqual(len(imgseriesmd), 1)


if __name__ == '__main__':
	unittest.main()

