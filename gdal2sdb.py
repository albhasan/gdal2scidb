from gdal2bin_util import *



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
        self.id = self.satellite + self.sensor + self.path + self.row + str(self.acquisition)
    def __repr__(self):
        return "ImageFile: " + self.filepath
    def getMetadata(self):
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
        col = []
        for fp in filepaths:
            assert type(fp) is str, "ImageFileCol: filepath is not a str: %r" % fp
            col.append(ImageFile(fp))
        self.col = sorted(col, key=lambda imageFile: imageFile.id)
        self.filepaths = []
        for imgf in self.col:
            self.filepaths = self.filepaths + [imgf.filepath]
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
                self.sensor = imgf.sensor
                self.path = imgf.path
                self.row = imgf.row
                self.acquisition =imgf.acquisition
                self.id = self.satellite + self.sensor + self.path + self.row + str(self.acquisition)
                imgfIds.add(self.id)
            assert len(imgfIds) == 1, "Image: The given ImageFiles do not belong to one Image"
            self.col = imgfc
            self.filepaths = imgfc.filepaths
    def __repr__(self):
        st = "Image: " + self.id + "\n"
        for key,value in self.filepaths.items():
            st = st + os.path.basename(str(value)) + "\n"
        return st



class ImageCol:
    """A sorted collection of Images"""
    def __init__(self, filepaths):
        assert type(filepaths) is list, "ImageCol: filepaths is not a list: %r" % filepaths
        self.col = []
        col = []
        for fp in filepaths:
            assert type(fp) is str, "ImageCol: filepath is not a str: %r" % fp
            col.append(ImageFile(fp))
        col = sorted(col, key=lambda imageFile: imageFile.id)
        self.filepaths = []
        for imgf in col:
            self.filepaths = self.filepaths + [imgf.filepath]
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
            self.col.append(Image(flist))
    def getImagesSeries(self):
        uimgsSet = set()    # unique image series
        imgslist = []       # list of ImageSeries
        for img in self.col:
            imgserId = img.satellite + img.sensor + img.path + img.row
            uimgsset.add(imgserId) 
        for uid in uimgsSet:
            flist = []
            for img in self.col:
                imgsid = ImageSeries(img.filepaths.values()).id
                if uid == imgsid:
                    flist = flist + img.filepaths.values()
            imgslist.append(ImageSeries(flist))
        return imgslist



class ImageSeries:
    """A set of images of the same satellite, sensor, path and row but different acquisition time. For creation, use ImageFileCol.getImageSeries"""
    def __init__(self, filepaths):
        #TODO: 
        # - validate all the images belong to the same image series  - raise NameError('Given images belong to many ImageSeries')
        assert type(filepaths) is list, "filepath is not a list: %r" % filepaths
        self.id = ''
        self.filepaths = sortFiles(filepaths)
        if len(self.filepaths) > 0:
            imgfc = ImageFileCol(self.filepaths.values())
            imgsId = set()
            for imgf in imgfc:
                imgsId.add(imgf.id)
                
                
                
            assert len(imgfc.getImageSeries()) == 1, "The given Images do not belong to one ImageSeries"
            imgf = ImageFile(self.filepaths.values()[0])
            self.id = imgf.satellite + imgf.sensor + imgf.path + imgf.row
    def __repr__(self):
        st = "ImageSeries: " + self.id + "\n"
        for img in self.imgs:
            st = st + img.id + "\n"
        return st
    def _countImageSeries(self):
        for img in self.imgs:
            imgsid = ImageSeries(img.filepaths.values()).id

            if uid == imgsid:
                flist = flist + img.filepaths.values()



#class ImageBand:
#    """A set of pixels (observations) of the same variable"""
#    def __init__(self, filepath):
#        self.imagefile = ""




