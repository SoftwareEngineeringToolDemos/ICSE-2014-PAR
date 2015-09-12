#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-05-23
# Function: link correct or not to level4_info
# Parameters: 1) level4_info
# Output stream: linked level4_info

import sys
import leon_lib as lib


# read target file

def read_llevel4_info_header(header, raw, curline):
	print curline[:-1] + lib.sep + 'correct'

def read_llevel4_info_body(header, raw, curline):
	new = raw[header['new']].lower()
	final = raw[header['final']].lower()
	print curline[:-1] + lib.sep + str(new == final)

lib.read_file(sys.argv[1], read_llevel4_info_header, read_llevel4_info_body)
