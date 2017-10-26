#!/bin/bash

# get the time_id from the query
export TID=$(iquery -aq "between(MOD13Q1,52800,48000,0,52800,48000,500)" | awk -F } '{if (NR!=1) { print $1 }}' | awk -F , '{ print $3 }')

# create a list of numbers
export NUM=$(seq 0 $(echo $TID | awk '{print $NF}'))

# compare

diff <(echo "$TID") <(echo "$NUM")






$(comm -23 <(echo "$TID") <(echo "$NUM"));


