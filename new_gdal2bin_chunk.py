import sys
import argparse
import logging
import numpy
from array import array
from gdal2bin_util import *

################################################################################
# NOTES:
# Ubuntu uses an old version of numpy
# sudo easy_install --upgrade numpy
# sudo easy_install --upgrade scipy
#-------------------------------------------------------------------------------
# TODO: Test
#-------------------------------------------------------------------------------
# Use:
# see test.sh
################################################################################

def main(argv):
    parser = argparse.ArgumentParser(description = "Export GDAL images' segments to the stdout using SciDB's binary format.")
    parser.add_argument("col",          help = "Number of the column from where to start getting data.")
    parser.add_argument("row",          help = "Number of the row from where to start getting data.")
    parser.add_argument("colbuf",       help = "Number of additional columns to get data from.")
    parser.add_argument("rowbuf",       help = "Number of additional rows to get data from.")
    parser.add_argument("coltrans",     help = "Translation applied to the column index.")
    parser.add_argument("rowtrans",     help = "Translation applied to the row index.")
    parser.add_argument("inputFiles",   help = "List of images separated by spaces.", nargs = "+")
    parser.add_argument("--d2tid",      help = "Use the date to compute the time_id. Otherwise use the time-ordered cardinal position of the image in the inputFiles. Default = True", default = 'True')
    parser.add_argument("--d2att",      help = "Add the image date as an int32 yyyymmdd attribute (last attribute). Default = False", default = 'False')
    parser.add_argument("--tile2id",    help = "Include the image's tile (e.g path & row) as pixel identifiers. Default = True", default = 'True')
    parser.add_argument("--output",     help = "The SciDB format used to export the data [binary, csv]. Default = binary", default = 'binary')
    parser.add_argument("--log",        help = "Log level. Default = WARNING", default = 'WARNING')
    # Get parameters
    args = parser.parse_args()
    inputFiles = args.inputFiles
    col = int(args.col)
    row = int(args.row)
    colbuf = int(args.colbuf)
    rowbuf = int(args.rowbuf)
    coltrans = int(args.coltrans)
    rowtrans = int(args.rowtrans)
    d2tid = args.d2tid in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    d2att = args.d2att in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    t2id = args.tile2id in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    output = args.output
    log = args.log
    ####################################################
    # CONFIG
    ####################################################
    gdal.UseExceptions()
    # log
    numeric_loglevel = getattr(logging, log.upper(), None)
    if not isinstance(numeric_loglevel, int):
        raise ValueError('Invalid log level: %s' % log)
    logging.basicConfig(filename = 'log_gdal2bin_chunk.log', level = numeric_loglevel, format = '%(asctime)s %(levelname)s: %(message)s')
    logging.info("gdal2bin_chunk: " + str(args))
    ####################################################
    # SCRIPT
    #---------------------------------------------------
    # [1] image == [n] bands of the same path/row and date
    # [1] image series == [n] images of the same satellite, sensor, path and row but different acquisition time
    # [1] band  == [1]file
    # [1] file  == [n] bands
    ####################################################
    # sort files by image-path/row-band
    imgfcol = ImageFileCol(inputFiles)
    

if __name__ == "__main__":
   main(sys.argv[1:])
