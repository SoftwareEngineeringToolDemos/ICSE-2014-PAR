#!/usr/bin/python

"""
Author: Leon Xie
Date: 11/12/2013
Usage: checkMetricsAndDoPredict.py predictedIssue (obtainted by running runR.sh) issue ID
Output: predicted result and metrics ....
"""

import sys
import predictedIssueTableReader


if __name__ == "__main__":
    predict = predictedIssueTableReader.PredictedIssueTableReader(',')
    if len(sys.argv) > 3:
        predict.ReadThreshold(sys.argv[3])
    print predict.DoCheckMetricsAndDoPredict(sys.argv[1], sys.argv[2])

