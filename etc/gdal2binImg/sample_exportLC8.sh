#!/bin/bash
################################################################################
# EXPORT LANDSAT 8 COLLECTION 1 IMAGE SERIES TO SCIDB BINARY FILES
################################################################################

IPATH=226                                 # LANDSAT PATH
IROW=064                                  # LANDSAT ROW


FILES=$(find -L /home/scidb/LANDSAT8/SurfaceReflectanceC1 -type f | grep "LC08_L1(GT|TP)$IPATH$IROW" | sort | head -n $FIRST)




