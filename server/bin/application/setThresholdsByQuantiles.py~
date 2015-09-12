#!/usr/bin/python

"""
Author: Leon Xie
Date: 11/12/2013
Usage: setThresholdsByQuantiles.py 
"""

import sys
import predictedIssueTableReader


if __name__ == '__main__':
    reader = predictedIssueTableReader.PredictedIssueTableReader(',')
    min_quantile = float(sys.argv[2])
    max_quantile = float(sys.argv[3])

    min_threshold = reader.GetThresholdByQuantile(sys.argv[1], min_quantile)
    max_threshold = reader.GetThresholdByQuantile(sys.argv[1], max_quantile)

    res = ';'.join([str(min_quantile), str(min_threshold), \
                          str(max_quantile), str(max_threshold)])
    
    print res
    

    
