#!/bin/bash
################################################################################
# REPORT NON-SEQUENTIAL TIME_IDs
#-------------------------------------------------------------------------------
# Usage:
# ./reportMissingTIDs.sh MOD13Q1 52800 48000 0 400
################################################################################

if (( $# != 5 )); then
    echo "ERROR:Illegal number of parameters"
    echo ""
    echo "Report non-sequential time_id in a 3D SciDB array"    
    echo "Usage ./reportMissingTIDs.sh array 52800 48000 0 400"
    echo "Where:"
    echo "-array         Name of a 3D SciDB array"
    echo "-col_id        Column ID"
    echo "-row_id        Row ID"
    echo "-time_id_from  time_id from where to start"
    echo "-time_id_to  time_id where to stop"
    exit 1
fi


ARRAY=$1
CID=$2
RID=$3
TID1=$4
TID2=$5


# get the list of time_id from the query
TID=$(iquery -aq "between($ARRAY,$CID,$RID,$TID1,$CID,$RID,$TID2)" | awk -F } '{if (NR!=1) { print $1 }}' | awk -F , '{ print $3 }')



# create a list of numbers
NUM=$(seq $TID1 $TID2)

# compare & report
diff <(echo "$TID") <(echo "$NUM") | grep ">" | awk '{print $2}'

