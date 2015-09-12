#!/bin/bash

appRoot='/data/zhengqm/PAR/src/server'
predictedIssue=$appRoot'/data/mozilla/predictedIssues.res'
threshold="$appRoot"/data/mozilla/predictThresholds

predictedResult=`$appRoot/bin/application/checkMetricsAndDoPredict.py $predictedIssue $1 $threshold`

echo "$predictedResult"


#model=$appRoot'/data/mozilla/model_assigning.r'

#buginfo=`$appRoot/bin/application/extractInfoByBugID.py $appRoot/data/mozillaNew/linfo_level2.tmp $appRoot/data/mozillaNew/lactivity_level2.tmp $1 $appRoot/data/mozillaNew/product_convertion`

#product=`echo $buginfo | awk -F ',' '{print $4}'`
#buginfo=`echo $buginfo | sed 's/,/ /g'`

#buginfo=($buginfo)
#if [ ${buginfo[0]} = "False" ]; then
#	echo "Error,$product"
#	exit 1
#fi

#metrics=`$appRoot/bin/application/queryMetrics.py $appRoot/data/mozillaNew/product_information_assi $appRoot/data/mozillaNew/login_product_information_assi $appRoot/data/mozillaNew/login_peer_info $appRoot/data/mozillaNew/login_ncomment $appRoot/data/mozillaNew/login_role  ${buginfo[1]} ${buginfo[2]} "$product"`


#pro=`R --slave <<EOF
#source("$appRoot/bin/rscript/predictAssi.r")
#predict_from_file("$2", "$1")
#predict_from_input("$model", $metrics, "$product")
#EOF`

#pro=($pro)
#pro=${pro[1]}

#threshold=`cat $appRoot/data/mozillaNew/predictThreshold`
#threshold=($threshold)
#minThr=${threshold[2]}
#maxThr=${threshold[3]}

#echo "${buginfo[1]},${buginfo[2]},$product,$metrics,$pro,$minThr,$maxThr"
