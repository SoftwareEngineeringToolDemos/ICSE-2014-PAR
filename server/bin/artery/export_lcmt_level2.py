#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-20
# Function: generate lcmt_level2 from info_level1
# Input Stream: info_level1
# Output Stream: lcmt_level2

import leon_lib as lib

class comment:
	def __init__(self):
		self.when = ''
		self.text_count = 0
		self.who = ''
	def set_time(self, timestamp):
		import time
		raw = timestamp.split(' ')
		# TODO: check to time transform code. there may be timezone problem.
		# input time stamp: 1998-4-07 11:56:14 -0700
		# expect output: integer of timestamp (seconds since 1970-01-01 00:00:00 GMT)
		date = time.strptime(raw[0] + ' ' + raw[1],'%Y-%m-%d %H:%M:%S')
		timezone = raw[2]
		offset = int(timezone[1:3]) * 3600 + int(timezone[3:5])*60
		if timezone[0] == '-':
			offset = -offset
		self.when = str(int(time.mktime(date) - time.timezone - offset))

class description:
	def __init__(self):
		self.bug_id = ''
		self.has_keywords = False
		self.has_stacktrace = False
		self.length = 0
print 'bug_id' + lib.sep + 'unknown' + lib.sep + 'who' + lib.sep + 'when' + lib.sep + 'what' + lib.sep + 'old' + lib.sep + 'new'
while 1:
	try:
		curline = raw_input()
	except EOFError:
		break

	raw = curline.split(lib.sep)

	cmts = {}
	for item in raw:
		kv = item.split('=')
		if kv.__len__() != 2:
			continue

		key = kv[0]
		value = kv[1]

		if key == 'Bug#':
			bug_id = value
		elif key[:5] == 'long:':
			subkey = key.split(':')
			cmt_id = subkey[1]
			if not cmts.has_key(cmt_id):
				cmts[cmt_id] = comment()
			if subkey[2] == 'bug_when':
				cmts[cmt_id].set_time(value)
			elif subkey[2] == 'text':
				cmts[cmt_id].text_count = value.__len__()
			elif subkey[2] == 'who':
				cmts[cmt_id].who = value
	
	for cmt_id in cmts:
		print bug_id + lib.sep + lib.sep + cmts[cmt_id].who + lib.sep + cmts[cmt_id].when + lib.sep + 'comment' + lib.sep + lib.sep + str(cmts[cmt_id].text_count)
