#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-10-14
# Function: get info_level2 from info_level1
# Input stream: info_level1
# Output stream: linfo_level2
# Last check: 2013-02-26

import leon_lib as lib

# title
print 'bug_id' + lib.sep + 'field' + lib.sep + 'what'
# content
while 1:
	try:
		curline = raw_input()
	except EOFError:
		break
	
	raw = curline.split(lib.sep)
	
	bug_id = ''
	for item in raw:
		kv = item.split('=')
		if kv.__len__() != 2:
			continue

		key = kv[0]
		value = kv[1]

		if key == 'Bug#':
			bug_id = value
		elif key == 'assigned_to':
			print bug_id + lib.sep + 'assigned_to' + lib.sep + value
		elif key == 'bug_severity':
			print bug_id + lib.sep + 'severity' + lib.sep + value
		elif key == 'bug_status':
			print bug_id + lib.sep + 'status' + lib.sep + value
		elif key == 'cc':
			print bug_id + lib.sep + 'cc' + lib.sep + value
		elif key == 'component':
			print bug_id + lib.sep + 'component' + lib.sep + value
		elif key == 'creation_ts':
			print bug_id + lib.sep + 'report_time' + lib.sep + value
		elif key == 'op_sys':
			print bug_id + lib.sep + 'os' + lib.sep + value
		elif key == 'priority':
			print bug_id + lib.sep + 'priority' + lib.sep + value
		elif key == 'product':
			print bug_id + lib.sep + 'product' + lib.sep + value
		elif key == 'reporter':
			print bug_id + lib.sep + 'reporter' + lib.sep + value
		elif key == 'resolution':
			print bug_id + lib.sep +'resolution' + lib.sep + value
		elif key == 'target_milestone':
			print bug_id + lib.sep + 'target_milestone' + lib.sep + value
		elif key == 'version':
			print bug_id + lib.sep + 'version' + lib.sep + value
