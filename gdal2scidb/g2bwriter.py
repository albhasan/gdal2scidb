import os
import sys
import numpy as np
from osgeo import gdal
import gdal2scidb as g2s
import logging
gdal.UseExceptions()

class SdbWriter:
    """Write images to SciDB's binary"""
    def __init__(self):
        self.data = []
    def __repr__(self):
        return "SdbWriter\n"
    def serialize(self, imgser, d2tid, d2att, tile2id, xsize, ysize, coltrans, rowtrans, outputDir, logging):
        assert isinstance(imgser, g2s.ImageSeries), "SdbWriter: Parameter is not an ImageSeries: %r" % str(imgser)
        tid = -1                # time_id
        ofiles = set()          # list of resuntilg files
        for img in imgser:
            tid = tid + 1
            if d2tid:
                tid = img.tid()
            if d2att:
                imgacq = img.acquisition
            bpixarr = []        # list of subdatasets' pixels
            xfrom = 0           # where a chunk starts
            yfrom = 0
            xto = 0             # where a chunk finishes
            yto = 0
            gimg = ""
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
                        bpixarr.append(bpix.astype(np.int64)) # 
                        band = None
                    gimg = None
                elif(img.sname[0:2] == "LC"):
                    for imgf in img.col:
                        logging.debug("SdbWriter: Processing subdataset: " + imgf.filepath)
                        band = gdal.Open(imgf.filepath)
                        xto = band.RasterXSize
                        yto = band.RasterYSize
                        bpix = band.ReadAsArray()
                        bpixarr.append(bpix.astype(np.int64)) # 
                        band = None
            except RuntimeError as e:
                logging.exception("message")
                em = str(e)
                if "not recognized as a supported file format" not in em:
                    raise RuntimeError("SdbWriter: Could not get the pixels out of a band")
            except Exception as e:
                logging.exception("message")
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
                        chunkarr = bpix[xc:(xc + xsize), yc:(yc + ysize)]
                        chunkarrflat = chunkarr.flatten() 
                        assert len(col_id) == len(chunkarrflat)
                        attdat.append(chunkarrflat)
                    #
                    if d2att:
                        attdat.append(np.repeat(imgacq, len(col_id)).astype(np.int64))
                    logging.debug("SdbWriter: Stacking the bands' chunk into one np array")
                    pixflat = np.vstack([crt_id, attdat]).T
                    fname = os.path.join(outputDir, imgser.id + "_" + str(xc) + "_" + str(yc) + ".sdbbin.tmp")
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
        # rename    
        logging.debug("SdbWriter: Removing tmp extension from filenames")
        for of in ofiles:
            basefn = os.path.splitext(of)[0]
            os.rename(of, basefn)





