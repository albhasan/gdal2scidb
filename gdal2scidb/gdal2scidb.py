#!/usr/bin/env python
#gdal2scidb.py
import os
import re
import g2butil as g2bu
from collections import OrderedDict


LANDSAT_COLLECTION_CATEGORY = OrderedDict([('T1','Tier 1'), ('T2','Tier 2'), ('RT','Real Time')])
LANDSAT_PROCESSING_LEVEL = OrderedDict([('L1TP', 'Precision and Terrain Correction'), ('L1GT', 'Systematic Terrain Correction'), ('L1GS', 'SystematicCorrection')])
LANDSAT_SATELLITE = {'4':'Landsat4','5':'Landsat5','7':'Landsat7', '8':'Landsat8'}
LANDSAT_SENSOR = {'C':'OLI/TIRS-Combined', 'O':'OLI-only', 'T':'TIRS-only', 'E':'ETM+', 'T':'TM', 'M':'MSS'}
MODIS_SENSOR = {'MOD':'Terra', 'MYD':'Aqua'}



#TODO:
# - Image: get pixels
# - import code from getPixelImages
# - import code from ymd2tid



class ImageFile:
    """A representation of a file. A file have at least one band"""
    def __init__(self, filepath):
        assert type(filepath) is str, "ImageFile: filepath is not a string: %r" % filepath
        self.filepath    = filepath
        self.reLandsat =     re.compile('^L[CETM][0-9]{14}(LGN|EDC|XXX|AAA)[0-9]{2}.+\.(tif|TIF)$')
        self.reLandsatCol1 = re.compile('^L[A-Z][0-9]{2}_[A-Z][0-9][A-Z]{2}_[0-9]{6}_[0-9]{8}_[0-9]{8}_[0-9]{2}_[A-Z][0-9]_([a-zA-Z]|[0-9]|_)*\.(tif|TIF)$')
        self.reModis =       re.compile('^MOD[0-9]{2}[A-Z][0-9]\.A[0-9]{7}\.h[0-9]{2}v[0-9]{2}\.[0-9]{3}\.[0-9]{13}\.hdf$') # https://lpdaac.usgs.gov/dataset_discovery/modis
        md = self.getFileNameMetadata()
        self.image       = md['image']
        self.type        = md['type']
        self.sensor      = md['sensor']
        self.satellite   = md['satellite']
        self.level       = md['level']
        self.path        = md['path']
        self.row         = md['row']
        self.acquisition = md['acquisition']
        self.processing  = md['processing']
        self.collection  = md['collection']
        self.category    = md['category']
        self.stationId   = md['stationId']
        self.archive     = md['archive']
        self.band        = md['band']
        self.product     = md['product']
        self.sname       = md['sname']
        self.driver      = ""
        self.ncol        = -1
        self.nrow        = -1
        self.bandtype    = []
        self.geotransform = ""
        self.id = self.satellite + "_" + self.level + "_" + self.sensor + "_" + self.path + "_" + self.row + "_" + str(self.acquisition)
    def __repr__(self):
        return "ImageFile: " + self.filepath
    def __lt__(self, other):
        if type(self) != type(other):
            raise ValueError("ImageFile: The given objects are not instances of the same class")
        return self.id < other.id
    def getMetadata(self):
        """Get metadata from GDAL"""
        gmd = g2bu.getGdalMetadata(self.filepath)
        self.driver = gmd['driver']
        self.ncol = gmd['ncol']
        self.nrow = gmd['nrow']
        self.bandtype = gmd['bandtype']
        self.geotransform = gmd['geotransform']
    def getFileNameMetadata(self):
        """Return a dict made of metadata from a file's name using."""
        filename = os.path.basename(self.filepath)
        ftype = 'Unknown'
        fsensor = ''
        fsatellite = ''
        fpath = ''
        frow = ''
        fstationId = ''
        farchive = ''
        fband = ''
        fproclev = ''                                                               # processing correction level
        facqdate = 0                                                                # acquisition date
        fprodate = 0                                                                # processing date
        fcolnum = ''                                                                # collection number
        fcolcat = ''                                                                # collection category
        fprod = ''                                                                  # product
        sname = ''                                                                  # short name
        #
        if self.reLandsat.search(filename):
            # example LC80090452014008LGN00_B1.TIF
            sname       = filename[0:2] + "0"+  filename[2]
            ftype       = "Landsat_untiered"
            fsensor     = LANDSAT_SENSOR[filename[1]]
            fsatellite  = LANDSAT_SATELLITE[str(int(filename[2]))]
            fpath       = filename[3:6]
            frow        = filename[6:9]
            facqdate    = ydoy2ymd(int(filename[9:13]) * 1000 + int(filename[13:16]))
            fstationId  = filename[16:19]
            farchive    = filename[19:21]
            if len(filename) > 24:
                fprod, fband = processLBand(filename[22:].split('.')[0])
        elif self.reLandsatCol1.search(filename):
            # example             LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF
            #                     LC08_L1TP_220071_20170207_20170216_01_T1
            # TOA Reflectance     LC08_L1TP_018060_20140904_20160101_01_T1_toa_*.
            # Surface reflectance LC08_L1TP_233013_2014265LGN00_sr_*.
            #                     LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CX_TX_prod_band.ext
            #                     LE07_L1TP_231064_20160109_20161016_01_T1_sr_band1.tif
            sname       = filename[0:4]
            ftype       = "Landsat_tiered"
            fsensor     = LANDSAT_SENSOR[filename[1]]
            fsatellite  = LANDSAT_SATELLITE[str(int(filename[2:4]))]
            fproclev    = filename[5:9]
            fpath       = filename[10:13]
            frow        = filename[13:16]
            facqdate    = int(filename[17:25])
            fprodate    = int(filename[26:34])
            fcolnum     = filename[35:37]
            fcolcat     = filename[38:40]
            if len(filename) > 44:
                fprod, fband = processLBand(filename[41:].split('.')[0])
        elif self.reModis.search(filename):
            # example MOD13Q1.A2015353.h14v10.005.2016007192511.hdf
            sname       = filename[0:7]
            ftype       = "Modis"
            fsensor     = filename[3:7]
            fsatellite  = filename[0:3]
            fpath       = filename[18:20]
            frow        = filename[21:23]
            facqdate    = ydoy2ymd(int(filename[9:16]))
            fprodate    = ydoy2ymd(int(filename[28:35]))
            fcolnum     = filename[24:27]
        else:
            warn("Unrecognized filename: " + filename)
        return({
        'filepath':     filepath,
        'image':        fsatellite + fsensor + fpath + frow + str(facqdate),
        'type':         ftype,
        'sensor':       fsensor,
        'satellite':    fsatellite,
        'level':        fproclev,
        'path':         fpath,
        'row':          frow,
        'acquisition':  facqdate,
        'processing':   fprodate,
        'collection':   fcolnum,
        'category':     fcolcat,
        'stationId':    fstationId,
        'archive':      farchive,
        'band':         fband,
        'product':      fprod,
        'sname':        sname
        })



class ImageFileCol:
    """A sorted collection of ImageFile"""
    def __init__(self, filepaths):
        assert type(filepaths) is list, "ImageFileCol: filepaths is not a list: %r" % filepaths
        self.col = []
        for fp in filepaths:
            assert type(fp) is str, "ImageFileCol: filepath is not a str: %r" % fp
            self.col.append(ImageFile(fp))
        self.col.sort()
        self.filepaths = []
        for imgf in self.col:
            self.filepaths.append(imgf.filepath)
        self.it = iter(self.col)
    def __repr__(self):
        st = ["ImageFileCol:"]
        for imgf in self.col:
            st.append(os.path.basename(imgf.filepath))
        return '\n'.join(st)
    def __iter__(self):
        return self
    def next(self):
        try:
            return self.it.next()
        except StopIteration:
            self.it = iter(self.col)
            raise StopIteration



class Image:
    """A set of bands of the same path/row and date. For creation, use ImageFileCol.getImages"""
    def __init__(self, filepaths):
        assert type(filepaths) is list, "Image: filepath is not a list: %r" % filepaths
        self.id = ''
        self.col = []
        imgfc = ImageFileCol(filepaths)
        if len(imgfc.filepaths) > 0:
            imgfIds = set()
            for imgf in imgfc:
                self.satellite = imgf.satellite
                self.level = imgf.level
                self.sensor = imgf.sensor
                self.path = imgf.path
                self.row = imgf.row
                self.acquisition = imgf.acquisition
                self.sname = imgf.sname
                self.id = self.satellite + "_" + self.level + "_" + self.sensor + "_" + self.path + "_" + self.row + "_" + str(self.acquisition)
                imgfIds.add(self.id)
            if len(imgfIds) > 1:
                raise ValueError("Image: The given ImageFiles do not belong to one Image")
            self.col = imgfc
            self.filepaths = imgfc.filepaths
    def __repr__(self):
        st = ["Image: " + self.id]
        for fp in self.filepaths:
            st.append(os.path.basename(fp))
        return '\n'.join(st)
    def __lt__(self, other):
        if type(self) != type(other):
            raise ValueError("Image: The given objects are not instances of the same class")
        return self.id < other.id
    def getMetadata(self):
        self.bandtype = []
        for imgf in self.col:
            imgf.getMetadata()
            self.driver = imgf.driver
            self.ncol = imgf.ncol
            self.nrow = imgf.nrow
            self.bandtypes = self.bandtype + imgf.bandtype
            self.geotransform = imgf.geotransform
    def tid(self):
        """ Compute the time_id of the image """
        origin = 0
        period = 0
        yearly = False
        if self.sname == 'MOD09Q1':
            origin = 20000101
            period = 8
            yearly = True
        elif self.sname == 'MOD13Q1':
            origin = 20000101
            period = 16
            yearly = True
        elif self.sname == 'LD5Original-DigitalNumber' or self.sname == "LC05":
            origin = 19840411
            period = 16
            yearly = False
        elif self.sname == 'LD8Original-DigitalNumber' or self.sname == "LC08":
            origin = 20130418
            period = 16
            yearly = False
        else:
            raise ValueError("Image: Unknown image name")
        return(g2bu.ymd2tid(self.acquisition, origin, period, yearly))
    def getpixels(self, x, y, xchunk, ychunk, dimpos):
        """ Get the pixels """
        return(g2bu.getPixelImages(self.filepaths, x, y, xchunk, ychunk, dimpos))


class ImageCol:
    """A sorted collection of Images"""
    def __init__(self, filepaths):
        assert type(filepaths) is list, "ImageCol: filepaths is not a list: %r" % filepaths
        self.col = []
        self.filepaths = ImageFileCol(filepaths).filepaths
        self._getImages()
        self.it = iter(self.col)
    def __repr__(self):
        st = ["ImageCol:"]
        for img in self.col:
            st.append(img.id)
        return '\n'.join(st)
    def __iter__(self):
        return self
    def next(self):
        try:
            return self.it.next()
        except StopIteration:
            self.it = iter(self.col)
            raise StopIteration
    def _getImages(self):
        """Build a python list of Image objects"""
        uimgset = set()  # unique images
        imgfc = ImageFileCol(self.filepaths)
        for imgf in imgfc:
            imgid = Image([imgf.filepath]).id
            uimgset.add(imgid)
        for uid in uimgset:
            flist = []
            for imgf in imgfc:
                imgid = Image([imgf.filepath]).id
                if uid == imgid:
                    flist.append(imgf.filepath)
            self.col = self.col + [Image(flist)]
        self.col.sort()
    def getImagesSeries(self, ignoreLevel = False):
        """Return a python list of ImageSeries objects.

        Keyword arguments:
        ignoreLevel -- Include image's level when testing the image series (default False)

        """
        uimgsSet = set()    # unique image series
        imgslist = []       # list of ImageSeries
        # get unique ids of ImageSeries
        for img in self.col:
            imgserId = ImageSeries(img.filepaths, ignoreLevel).id
            uimgsSet.add(imgserId)
        # build a list of filepaths of each ImageSeries
        for uid in uimgsSet:
            flist = []
            for img in self.col:
                imgsid = ImageSeries(img.filepaths, ignoreLevel).id
                if uid == imgsid:
                    flist = flist + img.filepaths
            imgslist.append(ImageSeries(flist, ignoreLevel))
        return imgslist



class ImageSeries:
    """A set of images of the same satellite, sensor, path and row but different acquisition time. For creation, use ImageFileCol.getImageSeries"""
    def __init__(self, filepaths, ignoreLevel = False):
        """Create an ImageSeries.

        Keyword arguments:
        filepaths   -- List of string. Path to files.
        ignoreLevel -- Include image's level when testing the image series (default False)

        """
        assert type(filepaths) is list, "ImageSeries: filepath is not a list: %r" % filepaths
        self.id = ''
        self.col = ImageCol(filepaths)
        self.filepaths = self.col.filepaths
        if len(self.filepaths) > 0:
            imgsId = set()
            for img in self.col.col:
                self.id = img.satellite + "_" + img.level + "_" + img.sensor + "_" + img.path + "_" + img.row
                if ignoreLevel:
                    self.id = img.satellite + "_" + img.sensor + "_" + img.path + "_" + img.row
                imgsId.add(self.id)
            assert len(imgsId) == 1, "ImageSeries: The given Images do not belong to one ImageSeries"
        self.it = iter(self.col)
    def __repr__(self):
        st = ["ImageSeries: " + self.id]
        for img in self.col.col:
            st.append(img.id)
        return '\n'.join(st)
    def __iter__(self):
        return self
    def next(self):
        try:
            return self.it.next()
        except StopIteration:
            self.it = iter(self.col)
            raise StopIteration



#class ImageBand:
#    """A set of pixels (observations) of the same variable"""
#    def __init__(self, image, driver, ncol, nrow, bandtype, geotransform):
#        self.image = image
#        self.driver = driver
#        self.ncol = ncol
#        self.nrow = nrow
#        self.bandtype = bandtype
#        self.geotransform = geotransform
#    def __repr__(self):
#        st = "ImageBand:" + "\n  Image: " + self.image.id + "\n  Driver: " + self.driver + "\n  N Col: " + self.ncol + "\n  N Row: " + self.nrow + "\n  Band type: " + self.bandtype
