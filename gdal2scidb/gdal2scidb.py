from gdal2bin_util import *



#TODO:
# - Image: get pixels
# - import code from getPixelImages
# - import code from getFileNameMetadata
# - import code from ymd2tid



class ImageFile:
    """A representation of a file. A file have at least one band"""
    def __init__(self, filepath):
        assert type(filepath) is str, "ImageFile: filepath is not a string: %r" % filepath
        md = getFileNameMetadata(filepath)
        self.filepath    = md['filepath']
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
        gmd = getGdalMetadata(self.filepath)
        self.driver = gmd['driver']
        self.ncol = gmd['ncol']
        self.nrow = gmd['nrow']
        self.bandtype = gmd['bandtype']
        self.geotransform = gmd['geotransform']



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
        st = "ImageFileCol: \n"
        for imgf in self.col:
            st = st + os.path.basename(imgf.filepath) + "\n"
        return st
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
        st = "Image: " + self.id + "\n"
        for fp in self.filepaths:
            st = st + os.path.basename(fp) + "\n"
        return st
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
        elif self.sname == 'LD5Original-DigitalNumber':
            origin = 19840411
            period = 16
            yearly = False
        elif self.sname == 'LD8Original-DigitalNumber':
            origin = 20130418
            period = 16
            yearly = False
        else:
            raise ValueError("Image: Unknown image name")
        return(ymd2tid(self.acquisition, origin, period, yearly))
    def getpixels(self, x, y, xchunk, ychunk, dimpos):
        """ Get the pixels """
        return(getPixelImages(self.filepaths, x, y, xchunk, ychunk, dimpos))


class ImageCol:
    """A sorted collection of Images"""
    def __init__(self, filepaths):
        assert type(filepaths) is list, "ImageCol: filepaths is not a list: %r" % filepaths
        self.col = []
        self.filepaths = ImageFileCol(filepaths).filepaths
        self._getImages()
        self.it = iter(self.col)
    def __repr__(self):
        st = "ImageCol: \n"
        for img in self.col:
            st = st + img.id + "\n"
        return st
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
    def getImagesSeries(self):
        """Return a python list of ImageSeries objects"""
        uimgsSet = set()    # unique image series
        imgslist = []       # list of ImageSeries
        for img in self.col:
            imgserId = ImageSeries(img.filepaths).id
            uimgsSet.add(imgserId)
        for uid in uimgsSet:
            flist = []
            for img in self.col:
                imgsid = ImageSeries(img.filepaths).id
                if uid == imgsid:
                    flist = flist + img.filepaths
            imgslist.append(ImageSeries(flist))
        return imgslist



class ImageSeries:
    """A set of images of the same satellite, sensor, path and row but different acquisition time. For creation, use ImageFileCol.getImageSeries"""
    def __init__(self, filepaths):
        assert type(filepaths) is list, "ImageSeries: filepath is not a list: %r" % filepaths
        self.id = ''
        self.col = ImageCol(filepaths)
        self.filepaths = self.col.filepaths
        if len(self.filepaths) > 0:
            imgsId = set()
            for img in self.col.col:
                self.id = img.satellite + "_" + img.level + "_" + img.sensor + "_" + img.path + "_" + img.row
                imgsId.add(self.id)
            assert len(imgsId) == 1, "ImageSeries: The given Images do not belong to one ImageSeries"
        self.it = iter(self.col)
    def __repr__(self):
        st = "ImageSeries: " + self.id + "\n"
        for img in self.col.col:
            st = st + img.id + "\n"
        return st
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
  
