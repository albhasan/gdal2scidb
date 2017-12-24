#!/usr/bin/env python
# parsesdb.py
import os
import sys
import argparse
import struct as st
################################################################################
# Parse a binary file
#-------------------------------------------------------------------------------
# Usage:
# python parsesdb.py ~/alber/test/MOD__13Q1_12_10_3560_720.sdbbin qqqqqqqqqqqqqqq
################################################################################
def main(argv):
    parser = argparse.ArgumentParser(description = "Parse a binary file in SciDB format.")
    parser.add_argument("inputFile",     help = "Path to a binary file.")
    parser.add_argument("fmt",           help = "Format string according to python's struct module.")
    #
    args = parser.parse_args()
    inputFile = args.inputFile
    fmt = args.fmt
    #
    try:
        f = open(inputFile, "rb")
        sz = st.calcsize(fmt)
        byte = f.read(sz)
        while byte != "":
            print(st.unpack(fmt, byte))
            byte = f.read(sz)
    except Exception as e:
        print("message")
        raise RuntimeError("Error!")
    finally:
        if not f.closed:
            f.close()

if __name__ == "__main__":
   main(sys.argv[1:])

