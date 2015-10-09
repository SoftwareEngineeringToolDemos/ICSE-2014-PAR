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

=====================================================================================

# PAR

***

This repository is contains information related to the tool PAR developed by Dr. Jialiang Xie, Dr. Qimu Zheng, Dr. Minghui Zhou, and Dr. Audris Mockus. 
The tool was originally presented in [this paper](http://dl.acm.org/citation.cfm?id=2591073&CFID=706774826&CFTOKEN=98353804).

This repository _is not_ the original repository for this tool. Here are some links to the original project:
* [The Official Project Page, including source code](https://github.com/minghuizhou/PAR.git)
* [A Video of the Tool](http://youtu.be/IuykbzSTj8s)

In this repository, for PAR you will find:
* :white_check_mark: [Source code](https://github.com/SoftwareEngineeringToolDemos/ICSE-2014-PAR) (available)
* :x: Executable tool (not available)

This repository was constructed by [Yi-Chun Chen(RimiChen)](https://github.com/RimiChen) under the supervision of [Emerson Murphy-Hill](https://github.com/CaptainEmerson). 

Thank for all assistances from Dr. Minghui Zhou and her colleagues. 
Though I had not successfully downloaded installation required data and failed to get it work, due to the limited network speed.


-------------------------------
Some installation instruction from authors: (for who want to get it work)

Note,  you need to get two data files (info_level1 and activity_level2) from below and put them on the directory of PAR/server/data/mozilla/:

https://passion-lab.org/subtopic/data_mozilla.php
Click "Bug", and:

at Level 1, click "Info Data" (info_level1, 3.1G)

at Level 2, click   "Activity Data" (activity_level2, 538M)


==================================================================================
This README document is created for CSC 510 Software engineering course, NCSU, 2015 fall.
and by
* Name: Yi-Chun Chen
* UnityID: ychen4
* Team: Onslow

* Studied paper: ICSE- 2014 "Product assignment recommender."

==================================================================================

