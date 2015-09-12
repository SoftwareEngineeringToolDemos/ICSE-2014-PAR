#!/bin/bash

if [ $# == 0 ];then
	echo "Usage: ./runR [community name(mozilla/gnome)]"
else
	echo "Now running R to analyze data for community $1"
	cd rscript
R --slave <<EOF
source("rscript.r")
run("$1")
EOF
	echo "Analyze finished"
	cd ..
fi



