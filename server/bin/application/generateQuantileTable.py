#!/usr/bin/python

"""
Author: Leon Xie
Date: 11/12/2013
Usage: generateQuantileTable.py predictedIssue (obtainted by running runR.sh) issue ID
Output: predicted result and metrics ....
"""

import sys
import predictedIssueTableReader

if __name__ == '__main__':
    reader = predictedIssueTableReader.PredictedIssueTableReader(',')
    quantile_value_list = reader.GenerateQuantileTable(sys.argv[1])

    index = 0
    for quantile_value in quantile_value_list:
        print ';'.join([ str(index), str(quantile_value) ])
        index += 1
    
