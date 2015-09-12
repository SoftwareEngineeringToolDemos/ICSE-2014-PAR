#!/bin/bash

# Author: Xie Jialiang
# Date: 2013-02-16
# Function: generate llevel5_* from the very beginning
# Parameter: 1) community name
#	     2) option: noclean
# Write: llevel5_*

echo "String Generate Data ..."

echo "Running Artery Stage 1 ..."
cd ./artery
./run_artery_stage1.sh $1
cd ..
echo "Artery Stage 1 Accomplished"

echo "Running Capillary ..."
cd ./capillary
./run_capillary.sh $1
cd ..
echo "Capillary Accomplished"

echo "Running Artery Stage 2 ..."
cd ./artery
./run_artery_stage2.sh $1
cd ..
echo "Artery Stage 2 Accomplished"

echo "Accomplished! Data was written to ../data/$1"

#if [ $# = 2 -a "$2"x = "noclean"x ]; then
#	echo ".tmp files are in the same folder"
#else
#	echo "Cleanning .tmp"
#	rm ../data/"$1"/*.tmp
#fi
