import os
import sys
import numpy as np
from osgeo import gdal
import gdal2scidb as g2s
import g2butil as g2bu
import logging
gdal.UseExceptions()

class SdbWriter:
    """Write images to SciDB's binary"""
    def __init__(self):
        self.data = []
    def __repr__(self):
        return "SdbWriter\n"
    def serialize(self, imgser, d2tid, d2att, tile2id, xsize, ysize, coltrans, rowtrans, outputDir, l2att, c2att, logging):
        """Write an a set of images (an ImageSeries object) into chunks.

        Keyword arguments:
        imgser    -- An ImageSeries object.
        d2tid     -- A boolean. Should the date be used to compute the time_id of each image?
        d2att     -- A boolean. Should the date be added as an extra attribute to the chunk?
        tile2id   -- A boolean. SHould the image's tile (path & row) be included as extra attributes to the chunk?
        xsize     -- An integer. The chunk size in the x direction
        ysize     -- An integer. The chunk size in the y direction
        coltrans  -- An integer. A translation applied to the columns
        rowtrans  -- An integer. A translation applied to the rows
        outputDir -- A string. The path where to store the resulting chunks
        l2att     -- A boolean. Should the image's level be added to the each chunk?
        c2att     -- A boolean. Should the image's category be added to the each chunk?
        logging   -- A logging object
        """
        assert isinstance(imgser, g2s.ImageSeries), "SdbWriter: Parameter is not an ImageSeries: %r" % str(imgser)
        tid = -1                                                                # time_id
        ofiles = set()                                                          # list of resuntilg files
        for img in imgser:
            tid = tid + 1
            if d2tid:
                tid = img.tid()
            if d2att:
                imgacq = img.acquisition
            bpixarr = []                                                        # list of subdatasets' pixels
            xfrom = 0                                                           # where a chunk starts
            yfrom = 0
            xto = 0                                                             # where a chunk finishes
            yto = 0
            gimg = ""
            lev = -1
            cat = -1
            # get all the pixels from all bands
            try:
                if(img.sname[0:3] == "MOD" or img.sname[0:3] == "MYD"):
                    gimg = gdal.Open(img.filepaths[0])
                    for subds in gimg.GetSubDatasets():
                        logging.debug("SdbWriter: Processing subdataset:" + str(subds))
                        band = gdal.Open(subds[0])
                        xto = band.RasterXSize
                        yto = band.RasterYSize
                        bpix = band.ReadAsArray()
                        bpixarr.append(bpix.astype(np.int64))
                        band = None
                    gimg = None
                elif(img.sname[0:2] == "LC"):
                    lev = g2s.LANDSAT_PROCESSING_LEVEL.keys().index(img.level)
                    cat = g2s.LANDSAT_COLLECTION_CATEGORY.keys().index(img.category)
                    for imgf in img.col:
                        logging.debug("SdbWriter: Processing subdataset: " + imgf.filepath)
                        band = gdal.Open(imgf.filepath)
                        xto = band.RasterXSize
                        yto = band.RasterYSize
                        bpix = band.ReadAsArray()
                        bpixarr.append(bpix.astype(np.int64))
                        band = None
                else:
                    logging.exception("Unknown image. Image id: " + img.id)
                    raise RuntimeError("SdbWriter: Could not get the pixels out of a band")
            except RuntimeError as e:
                logging.exception("message")
                logging.exception("Image id: " + img.id)
                em = str(e)
                if "not recognized as a supported file format" not in em:
                    raise RuntimeError("SdbWriter: Could not get the pixels out of a band")
            except Exception as e:
                logging.exception("message")
                logging.exception("Image id: " + img.id)
                raise RuntimeError("SdbWriter: Could not get the pixels out of a band")
            finally:
                if 'band' in locals():
                    band = None
                if 'gimg' in locals():
                    gimg = None
            # chunk the pixels
            for xc in range(xfrom, xto, xsize):
                for yc in range(yfrom, yto, ysize):
                    logging.debug("SdbWriter: Processing chunk: "+  str(xc) + " " + str(yc))
                    col_id = np.array((range(xc, min(xc + xsize, xto)) * min(ysize, yto - yc)), dtype=np.int64) + coltrans
                    row_id = (np.repeat(range(yc, min(yc + ysize, yto)), min(xsize, xto - xc)).astype(np.int64)) + rowtrans
                    time_id = np.repeat(tid, len(col_id)).astype(np.int64)
                    crt_id = []
                    if tile2id:
                        crt_id.append(np.repeat(img.path, len(col_id)).astype(np.int64))
                        crt_id.append(np.repeat(img.row, len(col_id)).astype(np.int64))
                    crt_id.append(col_id)
                    crt_id.append(row_id)
                    crt_id.append(time_id)
                    assert len(col_id) == len(row_id)
                    attdat = []                                                 # list of flat bands' pixels of a chunk
                    for bpix in bpixarr:
                        chunkarr = bpix[yc:(yc + ysize), xc:(xc + xsize)]       # chunkarr = bpix[xc:(xc + xsize), yc:(yc + ysize)]
                        chunkarrflat = chunkarr.flatten()
                        assert len(col_id) == len(chunkarrflat)
                        attdat.append(chunkarrflat)
                    if d2att:
                        attdat.append(np.repeat(imgacq, len(col_id)).astype(np.int64))
                    if l2att:
                        attdat.append(np.repeat(lev, len(col_id)).astype(np.int8))
                    if c2att:
                        attdat.append(np.repeat(cat, len(col_id)).astype(np.int8))
                    logging.debug("SdbWriter: Stacking the bands' chunk into one np array")
                    pixflat = np.vstack([crt_id, attdat]).T
                    fname = os.path.join(outputDir, g2bu.getValidFilename(imgser.id) + "_" + str(xc) + "_" + str(yc) + ".sdbbin.tmp")
                    ofiles.add(fname)
                    try:
                        fsdbbin = open(fname, 'a')
                        pixflat.tofile(fsdbbin)
                        fsdbbin.close()
                    except Exception as e:
                        logging.exception("message")
                        raise RuntimeError("SdbWriter: Could not chunk the pixels out of a band")
                    finally:
                        if 'fsdbbin' in locals():
                            if not fsdbbin.closed:
                                fsdbbin.close()
        # rename the output files
        logging.debug("SdbWriter: Removing tmp extension from filenames")
        for of in ofiles:
            basefn = os.path.splitext(of)[0]
            os.rename(of, basefn)
