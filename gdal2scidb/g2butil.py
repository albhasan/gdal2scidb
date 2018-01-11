#!/usr/bin/env python
#g2butil.py
import collections
import os
import re
import sys
import numpy
import datetime
from warnings import warn

try:
    from osgeo import gdal # ogr, osr
    from gdalconst import *
    gdal.UseExceptions()	                                                    # use GDAL's error messages #gdal.DontUseExceptions()
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')



# regular expressions used to identify the type of image from its file name
reLandsat = re.compile('^L[CETM][0-9]{14}(LGN|EDC|XXX|AAA)[0-9]{2}.+\.(tif|TIF)$')
reLandsatCol1 = re.compile('^L[A-Z][0-9]{2}_[A-Z][0-9][A-Z]{2}_[0-9]{6}_[0-9]{8}_[0-9]{8}_[0-9]{2}_[A-Z][0-9]_([a-zA-Z]|[0-9]|_)*\.(tif|TIF)$')
reModis = re.compile('^MOD[0-9]{2}[A-Z][0-9]\.A[0-9]{7}\.h[0-9]{2}v[0-9]{2}\.[0-9]{3}\.[0-9]{13}\.hdf$') # https://lpdaac.usgs.gov/dataset_discovery/modis



## Get some pixels from an image
#
# @param filepath   A string. The path of the file
# @param idband     A number. The id of the band to retrieve data from
# @param x          A number. The position of the first pixel in x
# @param y          A number. The position of the first pixel in y
# @param xchunk     A number. The size of the window in x
# @param ychunk     A number. The size of the window in y
# @return           A numpy array
def getBandPixels(filepath, idband, x, y, xchunk, ychunk):
    try:
        raster = filepath
        ds = gdal.Open(raster)
        band = ds.GetRasterBand(idband)
        array = band.ReadAsArray(x, y, xchunk, ychunk)
    except:
        raise RuntimeError("Could not get the pixels of a band")
    finally:
        band = None
        ds = None
    return(array)



## Match the GDAL to python datatypes
#
# @param gdalType   A string. The name of the GDAL datatype
# @return           A string. The type code
def mapGdal2python(gdalType):
    # http://www.gdal.org/gdal_8h.html
    # http://docs.python.org/2/library/array.html
    #
    #GDT_Unknown    Unknown or unspecified type
    #GDT_Byte       Eight bit unsigned integer
    #GDT_UInt16     Sixteen bit unsigned integer
    #GDT_Int16      Sixteen bit signed integer
    #GDT_UInt32     Thirty two bit unsigned integer
    #GDT_Int32      Thirty two bit signed integer
    #GDT_Float32    Thirty two bit floating point
    #GDT_Float64    Sixty four bit floating point
    #GDT_CInt16     Complex Int16
    #GDT_CInt32     Complex Int32
    #GDT_CFloat32   Complex Float32
    #GDT_CFloat64   Complex Float64
    #
    # Type code     C Type          Python Type         Minimum size in bytes
    # 'c'           char            character           1
    # 'b'           signed char     int                 1
    # 'B'           unsigned char   int                 1
    # 'u'           Py_UNICODE      Unicode character   2
    # 'h'           signed short    int                 2
    # 'H'           unsigned short  int                 2
    # 'i'           signed int      int                 2
    # 'I'           unsigned int    long                2
    # 'l'           signed long     int                 4
    # 'L'           unsigned long   long                4
    # 'f'           float           float               4
    # 'd'           double          float               8
    try:
        res = {
            'GDT_Byte':     'B',
            'GDT_Int16':    'h',
            'GDT_UInt16':   'H',
            'GDT_Int32':    'i',
            'GDT_UInt32':   'I',
            'GDT_Float32':  'f',
            'GDT_Float64':  'd',
            'GDT_CInt16':   'h',
            'GDT_CInt32':   'i',
            'GDT_CFloat32': 'f',
            'GDT_CFloat64': 'd'
        }[gdalType]
    except KeyError:
        res = 'f'
    return res



## Match the GDAL to a datatype
#
# @param gdalType   A string. The name of the GDAL datatype
# @return           A number
def mapGdaldatatype2(gdalType):
    try:
        res = {
            'GDT_Unknown':      0,
            'GDT_Byte':         1,
            'GDT_UInt16':       2,
            'GDT_Int16':        3,
            'GDT_UInt32':       4,
            'GDT_Int32':        5,
            'GDT_Float32':      6,
            'GDT_Float64':      7,
            'GDT_CInt16':       8,
            'GDT_CInt32':       9,
            'GDT_CFloat32':     10,
            'GDT_CFloat64':     11,
            'GDT_TypeCount':    12
        }[gdalType]
    except KeyError:
        raise()
    return res



## Get the number of consequtive repetitions in a vector
#
# @param vec    A list of values that could repeat themselvec along the list
# @return       Two lists. One made of elements found and the other with their respective last positions
def findrep(vec):
    el = []
    pos = []
    if len(vec) > 0:
        el.append(vec[0])
        for i in range(len(vec)):
            if(vec[i] != el[len(el) - 1]):
                pos.append(i - 1)
                el.append(vec[i])
        pos.append(i)
    return el, pos



## Transform a position from a single-dimension to a multi-dimension array
#
# @param n      An integer >= 0. The index of a position in a single-dimensional array
# @param dims   An integer array. The number of positions on each dimension in the multi-dimensional array
# @return       An integer array >= 0. The position of n in an array of len(dims)-dimensions. The dimension to the right changes faster
def n2pos(n, dims):
    pos = [0] * len(dims)                                                       # position of n in the array
    top = [0] * len(dims)                                                       # maximum number of elements on each dimension
    for i in reversed(range(len(dims))):
        tot = 1
        for j in range(i, len(dims)):
            tot = tot * dims[j]
        top[i] = tot
    if n > top[0] or n < 0:
        raise ValueError('Invalid index n')
    top.append(1)
    test = n
    for i in range(len(pos)):
        pos[i] = test // top[i + 1]
        test = test - (pos[i] * top[i + 1])
    return(pos)




def getFileNameMetadata(filepath):
    """DEPRECATED. Return a dict made of metadata from a file's name using.

    Keyword arguments:
    filepath -- A string. A path to a file

    """
    filename = os.path.basename(filepath)
    sensorLandsat = {'C':'OLI/TIRS-Combined', 'O':'OLI-only', 'T':'TIRS-only', 'E':'ETM+', 'T':'TM', 'M':'MSS'}
    satelliteLandsat = {'4':'Landsat4','5':'Landsat5','7':'Landsat7', '8':'Landsat8'}
    processingLevelLandsat = {'L1TP':'L1TP', 'L1GT':'L1GT', 'L1GS':'L1GS'} # processingLevelLandsat = {'L1TP':'Precision-and-Terrain-Correction', 'L1GT':'Systematic-Terrain-Correction', 'L1GS':'Systematic-Correction'}
    collectionCategoryLandsat = {'RT':'Real Time', 'T1':'Tier 1', 'T2':'Tier 2'}
    sensorModis = {'MOD':'Terra', 'MYD':'Aqua'}
    #
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
    if reLandsat.search(filename):
        # example LC80090452014008LGN00_B1.TIF
        sname       = filename[0:2] + "0"+  filename[2]
        ftype       = "Landsat_untiered"
        fsensor     = sensorLandsat[filename[1]]
        fsatellite  = satelliteLandsat[str(int(filename[2]))]
        fpath       = filename[3:6]
        frow        = filename[6:9]
        facqdate    = ydoy2ymd(int(filename[9:13]) * 1000 + int(filename[13:16]))
        fstationId  = filename[16:19]
        farchive    = filename[19:21]
        if len(filename) > 24:
            fprod, fband = processLBand(filename[22:].split('.')[0])
    elif reLandsatCol1.search(filename):
        # example             LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF
        #                     LC08_L1TP_220071_20170207_20170216_01_T1
        # TOA Reflectance     LC08_L1TP_018060_20140904_20160101_01_T1_toa_*.
        # Surface reflectance LC08_L1TP_233013_2014265LGN00_sr_*.
        #                     LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CX_TX_prod_band.ext
        #                     LE07_L1TP_231064_20160109_20161016_01_T1_sr_band1.tif
        sname       = filename[0:4]
        ftype       = "Landsat_tiered"
        fsensor     = sensorLandsat[filename[1]]
        fsatellite  = satelliteLandsat[str(int(filename[2:4]))]
        fproclev    = processingLevelLandsat[filename[5:9]]
        fpath       = filename[10:13]
        frow        = filename[13:16]
        facqdate    = int(filename[17:25])
        fprodate    = int(filename[26:34])
        fcolnum     = filename[35:37]
        fcolcat     = collectionCategoryLandsat[filename[38:40]]
        if len(filename) > 44:
            fprod, fband = processLBand(filename[41:].split('.')[0])
    elif reModis.search(filename):
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



## Process the metadata related to the band in a landsat filename
#
# @param filename   A string. The string regarding band or product/band information (no file extension)
# @return           A dict
def processLBand(band):
# test if the band contains product information
    fprod = ''
    fband = ''
    if band.count('_') == 0:
        fband = band
    elif band.count('_') == 1:
        fprod = band.split('_')[0]
        fband = band.split('_')[1]
    elif band.count('_') == 2:
        fprod = band.split('_')[0] + '_' + band.split('_')[1]
        fband = band.split('_')[2]
    if fband.find('band') != -1 and len(fband) == 5:                            # add a padding 0 to the band number
        fbnum = '0' + fband[4]
        fband = fband[0:4] + fbnum
    return(fprod, fband)



# Sort images by satellite, path, row and date
#
# @param filepaths  A list. The paths to the files
# @ return          An OrderedDict image-band and filepaths
def sortFiles(filepaths):
    imgfiles = {}
    for filepath in filepaths:
        fmd = getFileNameMetadata(filepath)
        if fmd['type'] != 'Unknown':
            imgfiles[fmd['image'] + fmd['band']] = filepath
    return(collections.OrderedDict(sorted(imgfiles.items())))



# Transform a date into year-day-of-the-year
#
# @param d  A datetime.date object
# @return   An integer YYYYDOY
def date2ydoy(d):
    return(d.year * 1000 + int(d.strftime('%j')))



# Transform year-day-of-the-year into a date
#
# @param yyyydoy    An int YYYYDOY
# @return           An datetime object
def ydoy2date(yyyydoy):
    year = yyyydoy/1000
    doy = yyyydoy - year * 1000
    return datetime.datetime(year, 1, 1) + datetime.timedelta(doy - 1)



# Transform year-day-of-the-year into a date
#
# @param yyyydoy    An int YYYYDOY
# @return           An integer YYYYMMDD
def ydoy2ymd(yyyydoy):
    d = ydoy2date(yyyydoy)
    return(d.year * 10000 + d.month * 100 + d.day)



# Transform date into a year-day-of-the-year
#
# @param ymd    An int YYYYMMDD
# @return       An integer YYYYDOY
def ymd2ydoy(ymd):
    y,m,d = ymd2ymd(ymd)
    return(date2ydoy(datetime.date(y, m, d)))



# Transform a a time_id index into a date YYYMMDD
#
# @param tid    An int. The time_id to transform
# @param origin An int YYYYMMDD. The day of when the time_id == 0
# @param period An int. The number of days between observations
# @param yearly A boolean. Do the dates yearly match January the 1st?
# @return       An int representing a date YYYYMMDD
def tid2ymd(tid, origin, period, yearly):
    ppy = 0
    ny = 0
    ntids = tid
    # cast YYYYDDMMs to date ints
    ory,orm,or_d = ymd2ymd(origin)
    if yearly:
        ppy = 1 + 365/period                                                    # periods per year
        ny = tid / ppy                                                          # number of years
        ntids = tid % ppy
    d = datetime.datetime(ory + ny, orm, or_d) + datetime.timedelta(days = ntids * period)
    return(d.year * 10000 + d.month * 100 + d.day)



# Get the parameters of the time_id index
#
# @param ymd    An string. The type of image imagetype
# @return       An dict of parameters: A string id, an int (YYYYMMDD) representing the date of the first image (time_id == 0),  the period (int, number of days between images) and a boolean flag if the dates resatrt yearly (i.e the first image of each year matches January the 1st)
def gettimeidparameters(imagetype):
    res = {'Unknown'}
    if imagetype == 'MOD09Q1':
        res = {'id':'MOD09Q1', 'origin':20000101, 'period':8, 'yearly':True}
    elif imagetype == 'MOD13Q1':
        res = {'id':'MOD13Q1', 'origin':20000101, 'period':16, 'yearly':True}
    elif imagetype == 'Landsat5' or imagetype == 'LC5' or imagetype == 'LC05':
        res = {'id':'LD5Original-DigitalNumber', 'origin':19840411, 'period':16, 'yearly':False}
    elif imagetype == 'Landsat8' or imagetype == 'LC8' or imagetype == 'LC08':
        res = {'id':'LD8Original-DigitalNumber', 'origin':20130418, 'period':16, 'yearly':False}
    return(res)



# Split a date into its parts
#
# @param ymd    An int YYYYMMDD
# @return       Three integers year, month, day
def ymd2ymd(ymd):
    y = ymd/10000
    m = (ymd - y * 10000)/100
    d = (ymd - y * 10000 - m * 100)
    return(y, m, d)



# Transform a date into a time_id index
#
# @param ymd    An int YYYYMMDD
# @param origin An int YYYYMMDD. The day when the time_id == 0
# @param period An int. The number of days between observations
# @param yearly A boolean. Do the dates yearly match January the 1st?
# @return       An integer. The time_id matching ymd or 0 is ymd doesn't match
def ymd2tid(ymd, origin, period, yearly):
    # image, origin, period, yearly
    # [MOD09Q1, 20000101, 8, True]
    # [MOD13Q1, 20000101, 16, True]
    # [LD5Original-DigitalNumber, 19840411, 16, False]
    # [LD8Original-DigitalNumber, 20130319, 16, False] # [LD8Original-DigitalNumber, 20130418, 16, False]
    res = 0
    dy = 0
    # cast YYYYDDMMs to dates
    ymdy,ymdm,ymdd = ymd2ymd(ymd)
    ory,orm,or_d = ymd2ymd(origin)
    dtymd = datetime.datetime(ymdy, ymdm, ymdd)
    dtor = datetime.datetime(ory, orm, or_d)
    if yearly:
        dy = 1 + 365/period                                                     # periods per year
        dtor = datetime.datetime(ymdy, 1, 1)
    ndays = (dtymd - dtor).days                                                 # days from origin to ymd
    if ndays % period == 0:
        res = ndays/period + (ymdy - ory) * dy
    return(res)



## Get GDAL metadata from the image
#
# @param filepath   A string.
# @return           A dict
def getGdalMetadata(filepath):
    res = {}
    try:
        path, filename = os.path.split(filepath)
        ext = os.path.splitext(filename)[1][1:]
        dataset = gdal.Open(filepath, GA_ReadOnly)                              # open dataset
        driver = dataset.GetDriver().LongName
        geotransform = dataset.GetGeoTransform()
        bandtype = []
        ncol = -1
        nrow = -1
        if(ext == 'hdf'):                                                       # modis
            for sdsname in dataset.GetSubDatasets():
                sds = gdal.Open(sdsname[0])
                for bandid in range(1, sds.RasterCount + 1):
                    band = sds.GetRasterBand(bandid)
                    bandtype.append(gdal.GetDataTypeName(band.DataType))
        else:                                                                   # landsat?
            ncol = dataset.RasterXSize     # TODO: ncol & nrow are wrongly reported for HDFs
            nrow = dataset.RasterYSize
            for bandid in range(1, dataset.RasterCount + 1):
                band = dataset.GetRasterBand(bandid)
                bandtype.append(gdal.GetDataTypeName(band.DataType))
        res = {'file':filepath, 'driver':driver, 'ncol':ncol, 'nrow':nrow, 'bandtype':bandtype, 'geotransform':geotransform}
    except IOError:
        raise IOError("Cannot open:" + filepath)
    except:
        raise RuntimeError("Could not get image metadata from: " + filepath)
    finally:
        dataset = None                                                          # close dataset
    return res



## Get pixels from an image
#
# @param filepath   A string. The path of the file
# @param x          A number. The position of the first pixel in x
# @param y          A number. The position of the first pixel in y
# @param xchunk     A number. The size of the window in x
# @param ychunk     A number. The size of the window in y
# @param dimpos     A number. Position of the new dimension in the array: 0 at the biginning, -1 at the end
# @return           A numpy array
def getPixels(filepath, x, y, xchunk, ychunk, dimpos):
    res = []
    try:
        path, filename = os.path.split(filepath)
        ext = os.path.splitext(filename)[1][1:]
        ds = gdal.Open(filepath, GA_ReadOnly)
        pixlist = []
        if(ext == 'hdf'):
            for sdsname in ds.GetSubDatasets():
                sds = gdal.Open(sdsname[0])
                for bandid in range(1, sds.RasterCount + 1):
                    band = sds.GetRasterBand(bandid)
                    pixs = band.ReadAsArray(x, y, xchunk, ychunk)
                    pixlist.append(pixs)
        else:
            for bandid in range(1, ds.RasterCount + 1):
                band = ds.GetRasterBand(bandid)
                pixs = band.ReadAsArray(x, y, xchunk, ychunk)
                pixlist.append(pixs)
        if len(pixlist) == 1:
            res = pixlist[0]
        elif len(pixlist) > 1:
            res = numpy.stack(pixlist, axis = dimpos)
    except:
        raise RuntimeError("Could not get the pixels from: " + filepath)
    finally:
        band = None
        ds = None
    return(res)



# Build a list of images and filepaths out of metadata
#
# @param imgseriesmd    A list of file metadata of a image series
# @return               A list of images and ther matching filepaths [img, [filepaths]]
def imgseries2imgfp(imgseriesmd):
    res = []
    imgfiles = []
    ifiles = []
    for i in range(len(imgseriesmd)):
        fl = []
        fmd = imgseriesmd[i]
        if fmd['image'] in imgfiles:
            imgpos = [j for j, x in enumerate(imgfiles) if x == fmd['image']]   # get the image position in the list
            fl = ifiles[imgpos[0]]                                              # get the file list of the image
            fl.append(fmd['filepath'])
            ifiles[imgpos[0]] = fl                                              # update the file list
        else:
            imgfiles.append(fmd['image'])
            ifiles.append([fmd['filepath']])
    for i in range(len(imgfiles)):
        tl =  [imgfiles[i], ifiles[i]]
        res.append(tl)
    return(res)



## Get the pixels at the same positions from several images
#
# @param filepaths  A string vector. The paths of the files
# @param x          A number. The position of the first pixel in x
# @param y          A number. The position of the first pixel in y
# @param xchunk     A number. The size of the window in x
# @param ychunk     A number. The size of the window in y
# @param dimpos     A number. Position of the new dimension in the array: 0 at the biginning, -1 at the end
# @return           A numpy array
def getPixelImages(filepaths, x, y, xchunk, ychunk, dimpos):
    res = []
    try:
        pixlist = []
        for filepath in filepaths:
            pixlist.append(getPixels(filepath, x, y, xchunk, ychunk, dimpos))
        res = numpy.stack(pixlist, axis = dimpos)
    except:
        raise
    return(res)
