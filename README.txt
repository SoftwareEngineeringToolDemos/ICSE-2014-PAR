Prerequisite
- 1 Python 2.7
- 2 R

How to deploy PAR

I. deploy backend
- 1 unpack server folder to any place, say "$par"
- 3 run data generation pipeline: cd bin; make llevel5 com=mozilla
- 4 train model: ./runR.sh mozilla
- 4 copy output file: cp rscript/predictedIssues.res ../data/mozilla/.
- 5 edit $par/server/bin/runPredictMoz.sh, line 3: appRoot="$par/server"
- 6 same to $par/server/bin/setThresholdMoz.sh, line 3
- 7 Delete all the quote(") in the first line of $par/data/mozilla/predictedIssues.res 
- 8 generate quantile table: python $par/server/bin/application/generateQuantileTable.py $par/server/data/mozilla/predictedIssues.res > $par/server/data/mozilla/quantileTable

II. deploy frontend (apache server is required)
- 1 unpack front folder/* to apache www folder
- 2 edit www/predict.php, line 12, change the path to $par/server/bin/runPredictMoz.sh
- 3 edit www/setThreshold.php, line 14, change the path to $par/server/bin/setThresholdMoz.sh
- 4 start apache server, you should be able to access the site (index.html).
- 5 pay attention to execution permission of *.sh/*.py files and read/write permission of data files.
- 6 pay attention to the action attributes of html forms in *.html and *.php 
