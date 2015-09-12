#!/usr/bin/python
"""Author:
    Xie Jialiang
Date:
    2013-11-14
Usage:
    python calculateGLR.py [parameters file] [dictionary of predictors]
Output:
    GLR response
"""

from sys import argv

class GLR(object):
    """General Linear Regression."""
    
    def __init__(self):
        self._parameters = {}

    def read_parameters_from_file(self, parameters_file):
        """Read model parameters from file."""
        
        self._parameters = {}
        in_file = open(parameters_file, 'r')
        for line in in_file:
            fields = line.sep(';')
            self.parameters[fields[0]] = float(fields[1])
        in_file.close()
    
    def parse_predictors_string(self, predictors_string):
        """Parse predictors in string into dictionary."""

        result = {}
        predictors = predictors_string.split(';')
        for predictor in predictors:
            fields = predictor.split(":")
            result[fields[0]] = float(fields[1])
        return result

    def calculate_response(self, predictors_dict):
        """Calculate the response by predictors and parameters."""

        result = 0.0
        for predictor in predictors_dict:
            if not predictor in self._parameters:
                continue
            result += predictors_dict[predictor] * self._parameters[predictor]
        return result
