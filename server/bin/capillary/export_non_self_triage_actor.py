#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-10-20
# Function: generate reporter(self-triage-actor) namelist
# Parameters: 1) linfo_level2
#	      2) activity_level2
# Output Stream: namelist of reporter
# Strategy: if we find a gay touch an issue not reported by itself, it is not self-triager.

import sys
import leon_lib as lib

# get issue reporter
# dictionary bug_id -> reporter
issue_reporter = {}
def read_body(header, raw, curline):
	global issue_reporter
	bug_id = raw[header['bug_id']]
	field = raw[header['field']]
	what = raw[header['what']]

	if field == 'reporter':
		issue_reporter[bug_id] = what
lib.read_file(sys.argv[1], lib.empty_header, read_body)

# only reporter
# dictionary login -> the first time she touched others issues, -1 means never
touch_others = {}
def read_act_body(header, raw, curline):
	global touch_others
	global issue_reporter
	issue = raw[header['bug_id']]
	actor = raw[header['who']]

	if not touch_others.has_key(actor):
		# the first time we meet the gay, assume it only touch its own issues
		touch_others[actor] = -1
	
	# if exist not self triage, set it false
	if issue_reporter.has_key(issue):
		reporter = issue_reporter[issue]
		if reporter != actor:
			when = int(raw[header['when']])
			if touch_others[actor] == -1:
				touch_others[actor] = when
			elif touch_others[actor] > when:
				touch_others[actor] = when

# read activity_level2
lib.read_file(sys.argv[2], lib.empty_header, read_act_body)

# output
print 'who' + lib.sep + 'when'
for actor in touch_others:
	if touch_others[actor] > 0:
		print actor + lib.sep + str(touch_others[actor])
