#/bin/bash

appRoot="/data/zhengqm/PAR/src/server"
quantileTable="$appRoot"/data/mozilla/quantileTable
threshold="$appRoot"/data/mozilla/predictThresholds

if [ $# -eq 2 ]; then
    $appRoot/bin/application/setThresholdsByQuantiles.py $quantileTable $1 $2 > $threshold
fi
    
sed 's/;/,/g' $threshold


#cat "$threshold"
#> "$threshold"





#model="$appRoot"/data/mozilla/model_assigning.r

#if [ $# -eq 2 ]; then
#	thre=`R --slave <<EOF
#	source("$appRoot/bin/rscript/predictAssi.r")
#	set_threshold("$model",$1,$2)
#	#EOF`
#	echo "$thre" > "$threshold"
#fi
#echo "$threshold"
#sed 's/;/,/g' "$threshold"
