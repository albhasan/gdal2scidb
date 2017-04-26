import collections
import os
import re
import sys
import numpy
import datetime
# import struct
from gdalconst import *
from osgeo import gdal # from osgeo import ogr, osr, gdal

gdal.UseExceptions()                                                                                                                        # use GDAL's error messages #gdal.DontUseExceptions()

# regular expressions used to identify the type of image from its file name
reLandsat = re.compile('^L[CETM][0-9]{14}(LGN|EDC|XXX|AAA)[0-9]{2}.+\.(tif|TIF)$')
reLandsatCol1 = re.compile('^L[A-Z][0-9]{2}_[A-Z][0-9][A-Z]{2}_[0-9]{6}_[0-9]{8}_[0-9]{8}_[0-9]{2}_[A-Z][0-9]_([a-zA-Z]|[0-9]|_)*\.tif$')
reModis = re.compile('^MOD[0-9]{2}[A-Z][0-9]\.A[0-9]{7}\.h[0-9]{2}v[0-9]{2}\.[0-9]{3}\.[0-9]{13}\.hdf$') # https://lpdaac.usgs.gov/dataset_discovery/modis



## Get the pixels at the same positions from several images
#
# @param filepaths  A string vector. The paths of the files
# @param x          A number. The position of the first pixel in x
# @param y          A number. The position of the first pixel in y
# @param xchunk     A number. The size of the window in x
# @param ychunk     A number. The size of the window in y
# @param dimpos     A numner. Position of the new dimension in the array: 0 at the biginning, -1 at the end
# @return           A numpy array
def getPixelImages(filepaths, x, y, xchunk, ychunk, dimpos = 0):
    res = []
    try:
        pixlist = []
        for filepath in filepaths:
            pixlist.append(getPixels(filepath, x, y, xchunk, ychunk))
        res = numpy.stack(pixlist, axis = dimpos)
    except:
        raise
    return(res)



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
                ds = gdal.Open(filepath, GA_ReadOnly)
                pixlist = []
                for bandid in range(1, ds.RasterCount + 1):
                        band = ds.GetRasterBand(bandid)
                        pixs = band.ReadAsArray(x, y, xchunk, ychunk)
                        pixlist.append(pixs)
                if len(pixlist) == 1:
                        res = pixlist[0]
                elif len(pixlist) > 1:
                        res = numpy.stack(pixlist, axis = dimpos)
        except:
                raise
        finally:
                band = None
                ds = None
        return(res)



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
                raise()
        finally:
                band = None
                ds = None
        return(array)



## Get GDAL metadata from the image
#
# @param filepath   A string.
# @return           A dict
def getGdalMetadata(filepath):
        res = {}
        try:
                path, filename = os.path.split(filepath)
                dataset = gdal.Open(filepath, GA_ReadOnly)                      # open dataset
                driver = dataset.GetDriver().LongName
                ncol = dataset.RasterXSize
                nrow = dataset.RasterYSize
                geotransform = dataset.GetGeoTransform()
                #GeoTransform[0] /* top left x */
                #GeoTransform[1] /* w-e pixel resolution */
                #GeoTransform[2] /* rotation, 0 if image is "north up" */
                #GeoTransform[3] /* top left y */
                #GeoTransform[4] /* rotation, 0 if image is "north up" */
                #GeoTransform[5] /* n-s pixel resolution */ 
                bandtype = []
                for bandid in range(1, dataset.RasterCount + 1):
                        band = dataset.GetRasterBand(bandid)
                        bandtype.append(gdal.GetDataTypeName(band.DataType))
                res = {'file':filepath, 'driver':driver, 'ncol':ncol, 'nrow':nrow, 'bandtype':bandtype, 'geotransform':geotransform}        
        except:
                raise RuntimeError("Could not get image metadata")
        finally:
                dataset = None                                                  # close dataset
        return res



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
            'GDT_Byte':     'f',
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



## Fix the band number in the file's name (padding zeros)
#
# @param filename   A string. The name of the file (no path!)
# @return           A dict
def completeBandNumber(filename):
        res = filename
        if reLandsat.match(filename):
                if(len(filename) == 28):
                        res = filename[:23] + '0' + filename[23:]
        elif reLandsatCol1.match(filename):
                if(len(filename) == 47):
                        res = filename[:42] + '0' + filename[42:]
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
        pos = [0] * len(dims)                                                                                                                # position of n in the array
        top = [0] * len(dims)                                                                                                                 # maximum number of elements on each dimension
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



# Is the given year a leap year?
#
# @param year   An integer. The year to test
# @return       A boolean
def isLeapYear(year):
        leapyear = False
        if year % 4 != 0:
                leapyear = False
        elif year % 100 != 0:
                leapyear = True
        elif year % 400 == 0:
                leapyear = True
        return(leapyear)



# Transform a date into year-day-of-the-year
#
# @param d  A datetime.date object
# @return   An integer YYYYDOY
def date2ydoy(d):
        return(d.year * 1000 + int(d.strftime('%j')))



# Transform year-day-of-the-year into a date
#
# @param yyyydoy    An int YYYYDOY
# @return           An integer YYYYMMDD
def ydoy2ymd(yyyydoy):
        year = yyyydoy/1000
        doy = yyyydoy - year * 1000
        d = datetime.datetime(year, 1, 1) + datetime.timedelta(doy - 1)
        return(d.year * 10000 + d.month * 100 + d.day)



# Transform date into a year-day-of-the-year
#
# @param ymd    An int YYYYMMDD
# @return       An integer YYYYDOY
def ymd2ydoy(ymd):
        y = ymd/10000
        m = (ymd - y * 10000)/100
        d = (ymd - y * 10000 - m * 100)
        return(date2ydoy(datetime.date(y, m, d)))



## Get the metadata from a file's name
#
# @param filepath   A string. The path to the file
# @return           A dict
def getFileNameMetadata(filepath):
        filename = os.path.basename(filepath)
        sensorLandsat = {'C':'OLI/TIRS Combined', 'O':'OLI-only', 'T':'TIRS-only', 'E':'ETM+', 'T':'TM', 'M':'MSS'}
        satelliteLandsat = {'7':'Landsat7', '8':'Landsat8'}
        processingLevelLandsat = {'L1TP':'Precision Terrain', 'L1GP':'Systematic Terrain', 'L1GS':'Systematic'}
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
        fproclev = ''                                                           # processing correction level
        facqdate = 0                                                            # acquisition date
        fprodate = 0                                                            # processing date
        fcolnum = ''                                                            # collection number
        fcolcat = ''                                                            # collection category
        #
        if reLandsat.search(filename):
                # example LC80090452014008LGN00_B1.TIF
                ftype       = "Landsat_untiered"
                fsensor     = sensorLandsat[filename[1]]
                fsatellite  = satelliteLandsat[str(int(filename[2]))]
                fpath       = filename[3:6]
                frow        = filename[6:9]
                facqdate    = ydoy2ymd(int(filename[9:13]) * 1000 + int(filename[13:16]))
                fstationId  = filename[16:19]
                farchive    = filename[19:21]
                if len(filename) > 24:
                    fband = filename[22:].split('.')[0]
        elif reLandsatCol1.search(filename):
                # example LC08_L1TP_140041_20130503_20161018_01_T1_B5.TIF
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
                    fband = filename[42:].split('.')[0]
        elif reModis.search(filename):
                # example MOD13Q1.A2015353.h14v10.005.2016007192511.hdf
                ftype                 = "Modis"
                fsensor                = filename[3:7]
                fsatellite        = filename[0:3]
                fpath                = filename[18:20]
                frow                = filename[21:23]
                facqdate        = ydoy2ymd(int(filename[9:16]))
                fprodate        = ydoy2ymd(int(filename[28:35]))
                fcolnum                = filename[24:27]
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
        'band':         fband
        })



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



# Sort files' metadata into images and file-paths
#
# @param imgseriesmd    A list of file metadata of a image series
# @ return              A list of images and ther matching filepaths [img, [filepaths]]
def imgseries2imgfp(imgseriesmd):
    imgfiles = []
    ifiles = []
    if len(filesmd) > 1:
        lastimg = filesmd[0]['image']
        for fmd in filesmd:
            if lastimg != fmd['image']:
                imgfiles.append([lastimg, ifiles])
                ifiles = []
            ifiles.append(fmd['filepath'])
            lastimg = fmd['image']
        imgfiles.append([lastimg, ifiles])
    return(imgfiles)






