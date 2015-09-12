#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-12-20
# Function: generate login comment number
# Parameter: lcmt_level2
# Output Stream: login_ncomment

import sys
import leon_lib as lib

# dictionary login -> when -> comment number
logins = {}

def read_lcmt_level2_body(header, raw, curline):
	global logins

	login = raw[header['who']]
	when = int(raw[header['when']])
	month_aligned_when = lib.month_align(when)

	# count
	if not logins.has_key(login):
		logins[login] = {}
	if not logins[login].has_key(month_aligned_when):
		logins[login][month_aligned_when] = 0
	logins[login][month_aligned_when] += 1

lib.read_file(sys.argv[1], lib.empty_header, read_lcmt_level2_body)

# output result
print 'login' + lib.sep + 'cmt_num'
for login in logins:
	out = login + lib.sep
	dates = sorted(logins[login].keys())
	cur_num = 0
	for date in dates:
		cur_num += logins[login][date]
		out += str(cur_num) + lib.fsep + str(date) + lib.tsep
	print out[:-lib.tsep.__len__()]
