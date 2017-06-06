#!/usr/bin/python
import sys
import argparse
from gdal2bin_util import ymd2tid
from gdal2bin_util import ydoy2ymd

def main(argv):
    parser = argparse.ArgumentParser(description = "Compute a SciDB time index from a date.")
    parser.add_argument("ymd", help = "A date represented by numbers like YYYYMMDD or YYYYDOY")
    parser.add_argument("origin", help = "An date YYYYMMDD. The day when the time_id is 0")
    parser.add_argument("period", help = "The number of days between two consequtive time_id")
    parser.add_argument("--yearly", help = "Do the dates yearly match January the 1st? (Default = True)", default = 'True')
    # get parameters
    args = parser.parse_args()
    ymd = args.ymd
    origin = args.origin
    period = args.period
    yearly = args.yearly in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    # script
    if len(ymd) == 8:
        print(str(ymd2tid(int(ymd), int(origin), int(period), yearly)))
    elif len(ymd) == 7:
        print(str(ymd2tid(ydoy2ymd(int(ymd)), int(origin), int(period), yearly)))
    else:
        print("-1")

if __name__ == "__main__":
   main(sys.argv[1:])

