from gdal2bin_util import *
# [1] image == [n] bands of the same path/row and date
# [1] image series == [n] images of the same satellite, sensor, path and row but different acquisition time
# [1] band  == [1]file
# [1] file  == [n] bands


class ImageSeries:
    """A set of images of the same satellite, sensor, path and row but different acquisition time. For creation, use ImageFileCol.getImageSeries"""
    def __init__(self, filepaths):
        self.filepaths = sortFiles(filepaths)
        self.id = ''
        if len(self.filepaths) > 0:
            imgf = ImageFile(filepaths[0])
            self.id = imgf.satellite + imgf.sensor + imgf.path + imgf.row
        #TODO: here I go - Build Images out of the given paths!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __repr__(self):
        st = "ImageSeries: " + self.id + "\n"
        for key,value in self.filepaths.items():
            st = st + os.path.basename(str(value)) + "\n"
        return st

#class ImageBand:
#    """A set of pixels (observations) of the same variable"""
#    def __init__(self, filepath):
#        self.imagefile = ""

class Image:
    """A set of bands of the same path/row and date. For creation, use ImageFileCol.getImages"""
    def __init__(self, filepaths):
        self.filepaths = sortFiles(filepaths)
        self.id = ''
        #TODO: Validate all the filepaths belong to the same image?
        if len(self.filepaths) > 0:
            imgf = ImageFile(filepaths[0])
            self.id = imgf.satellite + imgf.sensor + imgf.path + imgf.row + str(imgf.acquisition)
    def __repr__(self):
        st = "Image: " + self.id + "\n"
        for key,value in self.filepaths.items():
            st = st + os.path.basename(str(value)) + "\n"
        return st

class ImageFileCol:
    """A sorted collection of ImageFile"""
    def __init__(self, filepaths):
        self.filepaths = sortFiles(filepaths)
        self.col = []
        for key,val in self.filepaths.items():
            self.col.append(ImageFile(val))
        self.it = iter(self.col)
    def __repr__(self):
        st = "ImageFileCol: \n"
        for key,value in self.filepaths.items():
            st = st + os.path.basename(str(value)) + "\n"
        return st
    def __iter__(self):
        return self
    def next(self):
        return self.it.next()
    def getImages(self):
        uimgset = set()  # unique images
        imglist = []     # list of Image objects
        for imgf in self.col:
            imgid = Image([imgf.filepath]).id
            uimgset.add(imgid)
        for uid in uimgset:
            flist = []
            for imgf in self.col:
                imgid = Image([imgf.filepath]).id 
                if uid == imgid:
                    flist.append(imgf.filepath)
            imglist.append(Image(flist))
        return imglist
    def getImageSeries(self):
        imgs = self.getImages()
        uimgsset = set()  # unique image series
        imgslist = []     # list of ImageSeries objects
        for imgf in self.col:
            imgsid = ImageSeries([imgf.filepath]).id
            uimgsset.add(imgsid) 
        for uid in uimgsset:
            flist = []
            for img in imgs:
                imgsid = ImageSeries(img.filepaths.values()).id
                print(imgsid)
                if uid == imgsid:
                    flist = flist + img.filepaths.values()
            print(flist)
            imgslist.append(ImageSeries(flist))
        return imgslist

class ImageFile:
    """A representation of a file. A file have at least one band"""
    def __init__(self, filepath):
        md = getFileNameMetadata(filepath)
        self.md = md
        self.filepath = md['filepath']
        self.image = md['image']
        self.type = md['type']
        self.sensor = md['sensor']
        self.satellite = md['satellite']
        self.level = md['level']
        self.path = md['path']
        self.row = md['row']
        self.acquisition = md['acquisition']
        self.processing = md['processing']
        self.collection = md['collection']
        self.category = md['category']
        self.stationId = md['stationId']
        self.archive = md['archive']
        self.band = md['band']
        self.product = md['product']
        self.sname = md['sname']
        self.driver = ""
        self.ncol = -1
        self.nrow = -1
        self.bandtype = []
        self.geotransform = ""
    def __repr__(self):
        return "ImageFile: " + os.path.basename(self.filepath)
    def getMetadata(self):
        gmd = getGdalMetadata(self.filepath)
        self.driver = gmd['driver']
        self.ncol = gmd['ncol']
        self.nrow = gmd['nrow']
        self.bandtype = gmd['bandtype']
        self.geotransform = gmd['geotransform']

