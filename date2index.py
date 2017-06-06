#!/usr/bin/python
import sys
import argparse
from gdal2bin_util import ymd2tid

def main(argv):
    parser = argparse.ArgumentParser(description = "Compute a SciDB time index from a date.")
    parser.add_argument("ymd", help = "A date represented by numbers like this: YYYYMMDD")
    parser.add_argument("origin", help = "An date YYYYMMDD. The day when the time_id is 0")
    parser.add_argument("period", help = "The number of days between two consequtive time_id")
    parser.add_argument("--yearly", help = "Do the dates yearly match January the 1st? (Default = True)", default = 'True')
    # get parameters
    args = parser.parse_args()
    ymd = int(args.ymd)
    origin = int(args.origin)
    period = int(args.period)
    yearly = args.yearly in ['True', 'true', 'T', 't', 'YES', 'yes', 'Y', 'y']
    # script
    print(str(ymd2tid(ymd, origin, period, yearly)))

if __name__ == "__main__":
   main(sys.argv[1:])

