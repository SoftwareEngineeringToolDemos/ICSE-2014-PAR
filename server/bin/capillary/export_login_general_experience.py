#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-10-12
# Function: generate general experience (how many issue it has touched) of login
# Parameter: activity_level2
# Output Stream: login_general_experience
# Warning: Touched activities are defined by list

import sys
import leon_lib as lib

# define touched activities
# TODO: are these acts define suitable?
touch_acts = set(['Assignee',
		'Component',
		'OS',
		'Priority',
		'Product',
		'Resolution',
		'Severity',
		'Status',
		'Version',
		'assigned_to',
		'component',
		'op_sys',
		'priority',
		'product',
		'resolution',
		'bug_severity',
		'bug_status',
		'version'])
# dictionary login -> time when it touched new bug -> number of bug
logins = {}
# dictionary login -> set of touched bug id -> earliest time
login_bug_id = {}

def read_body(header, raw, curline):
	bug_id = raw[header['bug_id']]
	login = raw[header['who']]
	when = int(raw[header['when']])
	act = raw[header['what']]

	if act in touch_acts:
		if not logins.has_key(login):
			# never seen this gay, keep it in mind
			logins[login] = {}
		if not login_bug_id.has_key(login):
			# never seen this gay, keep it in mind
			login_bug_id[login] = {}

		if not bug_id in login_bug_id[login]:
			# did not touch this bug before, record it
			if not logins[login].has_key(when):
				logins[login][when] = 0
			logins[login][when] += 1
			login_bug_id[login][bug_id] = when
		else:
			# has touch this bug, look whether this is earlier
			old_when = login_bug_id[login][bug_id]
			if when < old_when:
				# touch earlier, update logins 1) remove from old_when 2) add to new when
				logins[login][old_when] -= 1
				if not logins[login].has_key(when):
					logins[login][when] = 0
				logins[login][when] += 1
				# update login_bug_id
				login_bug_id[login][bug_id] = when

# read activity_level2
lib.read_file(sys.argv[1], lib.empty_header, read_body)

# release resource
login_bug_id = 0

# export a exp sequence of a login
# e.g. input ({time:number,...}):
# {1:1, 3:2, 6:1}
# output(exp@time):
# 1@1 ~> 3@3 ~> 4@6
def export_exp(time_map):
	# sort time_map
	time_list = sorted(time_map.keys())
	# export at time sequence
	exp = 0
	result = ''
	for time in time_list:
		exp += time_map[time]
		result += str(exp) + lib.fsep + str(time) + lib.tsep
	if result.__len__() > 0:
		return result[:-lib.tsep.__len__()]
	else:
		return result

print 'who' + lib.sep + 'exp'
for login in logins:
	result = export_exp(logins[login])
	print login + lib.sep + result
