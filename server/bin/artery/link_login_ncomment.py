#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-22
# Function: link comment number to llevel4_*
# Parameters: 1) llevel4_*
#	      2) login_comment_number
# Output Stream: linked llevel4_*

import sys
import leon_lib as lib

# read login_comment_number
login_cmt = {}

def read_login_comment_number(header, raw, curline):
	global login_cmt
	login = raw[header['login']]
	raw_cmt = raw[header['cmt_num']].split(lib.tsep)
	cmt_num = []
	for str_num in raw_cmt:
		raw_num = str_num.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_num[0])
		newpack.when = int(raw_num[1])
		cmt_num.append(newpack)
	login_cmt[login] = cmt_num

lib.read_file(sys.argv[2], lib.empty_header, read_login_comment_number)

# link to target file

def link_header(header, raw, curline):
	print curline[:-1] + lib.sep + 'cmt_num'

def link_body(header, raw, curline):
	global login_cmt
	login = raw[header['login']]
	when = int(raw[header['when']])

	num = 0
	if login_cmt.has_key(login):
		index = lib.binary_search(login_cmt[login], lib.func_time, when)
		if index >= 0:
			num = login_cmt[login][index].data
	print curline[:-1] + lib.sep + str(num)

lib.read_file(sys.argv[1], link_header, link_body)

