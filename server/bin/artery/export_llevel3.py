#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-10-26
# Function: generate llevel3 from linfo_level2 and activity_level2 
# Parameters: 1) linfo_level2
#	      2) activity_level2
# Output stream: llevel3
# Last check: 2013-02-26

import sys
import leon_lib as lib

# 1) read linfo_level2, which records the nearest values of fields
class info_pack:
	def __init__(self):
		self.bug_id = ''
		self.assigned_to = ''
		self.severity = ''
		self.status = ''
		self.cc = ''
		self.component = ''
		self.report_time = 0
		self.os = ''
		self.priority = ''
		self.product = ''
		self.reporter = ''
		self.resolution = ''
		self.target_milestone = ''
		self.version = ''
# dictionary bug_id -> info_pack
info_packs = {}

def read_linfo_level2_body(header, raw, curline):

	global info_packs

	bug_id = raw[header['bug_id']]
	key = raw[header['field']]
	value = raw[header['what']]

	if not info_packs.has_key(bug_id):
		info_packs[bug_id] = info_pack()
		info_packs[bug_id].bug_id = bug_id
	if key == 'assigned_to':
		info_packs[bug_id].assigned_to = value
	elif key == 'severity':
		info_packs[bug_id].severity = value
	elif key == 'status':
		info_packs[bug_id].status = value
	elif key == 'cc':
		info_packs[bug_id].cc = value
	elif key == 'component':
		info_packs[bug_id].component = value
	elif key == 'report_time':
		info_packs[bug_id].report_time = value
	elif key == 'os':
		info_packs[bug_id].os = value
	elif key == 'priority':
		info_packs[bug_id].priority = value
	elif key == 'product':
		info_packs[bug_id].product = value
	elif key == 'reporter':
		info_packs[bug_id].reporter = value
	elif key == 'resolution':
		info_packs[bug_id].resolution = value
	elif key == 'target_milestone':
		info_packs[bug_id].target_milestone = value
	elif key == 'version':
		info_packs[bug_id].version = value

# read linfo_level2
lib.read_file(sys.argv[1], lib.empty_header, read_linfo_level2_body)


# 2) read activity level2
class act_pack:
	def act_pack(self):
		self.time = 0
		self.old = ''
		self.new = ''
		self.who = ''

class issue:
	def __init__(self):
		# basic info
		self.bug_id = ''
		self.reporter = ''
		self.report_time = 0
		# time series
		self.status = []
		self.resolution = []
		self.version = []
		self.os = []
		self.product = []
		self.component = []
		self.severity = []
		self.priority = []
		self.assigned_to = []
		self.target_milestone = []
		self.cc = []

# compare two act_pack by their time
def act_pack_cmp(e1, e2):
	return e1.time - e2.time

# combine information of an issue in linfo_level2 and activity_level2, output an issue in one row
# parameter cur_bug_id
# parameter cur_bug: holds all the information (except bug_id) about the bug

def build_issue_time_series(cur_bug_id, cur_bug):
	global info_packs
	sep = lib.sep
	tsep = lib.tsep
	fsep = lib.fsep

	# basic informatin: reporter, reporting time
	if info_packs.has_key(cur_bug_id):
		cur_bug.reporter = info_packs[cur_bug_id].reporter
		cur_bug.report_time = info_packs[cur_bug_id].report_time
	else:
		# if no information about this bug is recorded in linfo_level1, ignore it.
		# TODO: how many bugs reach here?
		return

	# time series
	# is_inconsist check whether the values in near timestamps are constant
	global is_inconsist
	str_status = build_meta_time_series(cur_bug.status, cur_bug, info_packs[cur_bug_id].status, fsep, tsep)
	str_resolution = build_meta_time_series(cur_bug.resolution, cur_bug, info_packs[cur_bug_id].resolution, fsep, tsep)
	str_component = build_meta_time_series(cur_bug.component, cur_bug, info_packs[cur_bug_id].component, fsep, tsep)
	str_os = build_meta_time_series(cur_bug.os, cur_bug, info_packs[cur_bug_id].os, fsep, tsep)
	str_priority = build_meta_time_series(cur_bug.priority, cur_bug, info_packs[cur_bug_id].priority, fsep, tsep)
	str_product = build_meta_time_series(cur_bug.product, cur_bug, info_packs[cur_bug_id].product, fsep, tsep, True)
	str_severity = build_meta_time_series(cur_bug.severity, cur_bug, info_packs[cur_bug_id].severity, fsep, tsep)
	str_target_milestone = build_meta_time_series(cur_bug.target_milestone, cur_bug, info_packs[cur_bug_id].target_milestone, fsep, tsep)
	str_version = build_meta_time_series(cur_bug.version, cur_bug, info_packs[cur_bug_id].version, fsep, tsep)
	str_assigned_to = build_meta_time_series(cur_bug.assigned_to, cur_bug, info_packs[cur_bug_id].assigned_to, fsep, tsep)
	# bu yong guan xia mian zhe ge
	str_cc = build_complex_time_series(cur_bug.cc, cur_bug, info_packs[cur_bug_id].cc, fsep, tsep)
	
	# print
	print cur_bug_id + sep + cur_bug.reporter + sep + str(cur_bug.report_time) + \
			sep + str_status + sep + str_resolution + \
			sep + str_severity + sep + str_priority + \
			sep + str_os + sep + str_product + sep + str_component + sep + str_version + \
			sep + str_assigned_to + sep + str_target_milestone + sep + str_cc

# return a string of the sequence of <value,time> tuples of a field
# parameter act_packs: array of the target field
# parameter cur_bug: in case of needing additional information of the bug
# parameter info_pack_field: the value in linfo_level2
# parameter fsep, tsep: separaters
# parameter check_consistancy: need to check consistancy of values between times
# description: logically, the input of act_packs would be (if it is not empty):
#   <value_old1,value_new1,logina,time1><value_old2,value_new2,loginb,time2>...<value_oldn,value_newn,loginx,timen>
# the loop builds the string from tail to head with the value_new. so after the loop, we get result string:
#   value_new1->value_new2->...->value_newn
# note that there's still an initial value, so we append it after the loop, and we get:
#   value_old1->value_new1->value_new2->...->value_newn
# consistancy is checked as value_new(i) == value_old(i+1) ?

def build_meta_time_series(act_packs, cur_bug, info_pack_field, fsep, tsep, check_consistancy = False):
	global is_inconsist
	if check_consistancy:
		is_inconsist = is_inconsist and False
	result = ''
	# scan through the array
	# the length of array will greater than 0 if the bug has been recorded in activity_level2
	if act_packs.__len__() > 0:
		# reverse sort, we need to imply the value from now to past
		act_packs = sorted(act_packs, act_pack_cmp, reverse = True)
		# construct string
		# info_pack_field holds the current value
		after = info_pack_field
		for pack in act_packs:
			write_info = pack.new
			if check_consistancy:
				# do renaming here
				write_info = after
			# add to result string
			result = str(write_info) + fsep + str(pack.time) + fsep + str(pack.who) + tsep + result
			# check consistancy
			if check_consistancy:
				global inconsist_bug
				global inconsist_reason
				before = pack.new
				if before != after:
					is_inconsist = True
					inconsist_bug.add(cur_bug.bug_id)
					if not inconsist_reason.has_key(before):
						inconsist_reason[before] = {}
					if not inconsist_reason[before].has_key(after):
						inconsist_reason[before][after] = 0
					inconsist_reason[before][after] += 1
				after = pack.old
		pack = act_packs[-1]
		# pack holds the initial value of the field
		result = str(pack.old) + fsep + str(cur_bug.report_time) + fsep + str(cur_bug.reporter) + tsep + result
	else:
		# if reaches here, the field has never been modified since bug reported 
		result = str(info_pack_field) + fsep + str(cur_bug.report_time) + fsep + str(cur_bug.reporter) + tsep
	return result[:-fsep.__len__()-1]

def build_complex_time_series(act_packs, cur_bug, info_pack_field, fsep, tsep):
	result = ''
	# only count number
	# begin from latest
	cur_count = 0
	if info_pack_field != '':
		cur_count = int(info_pack_field.split(':').__len__())
	# sort
	act_packs = sorted(act_packs, act_pack_cmp, reverse = True)
	# activity info
	for pack in act_packs:
		result = str(cur_count) + fsep + str(pack.time) + fsep + str(pack.who) + tsep + result
		minus_count = 0
		if pack.old != '':
			minus_count = pack.old.split(', ').__len__()
		add_count = 0
		if pack.new != '':
			add_count = pack.new.split(', ').__len__()
		cur_count = cur_count + minus_count - add_count
	result = str(cur_count) + fsep + str(cur_bug.report_time) + fsep + str(cur_bug.reporter) + tsep + result
	
	return result[:-fsep.__len__()-1]

inconsist_reason = {}
inconsist_bug = set()
is_inconsist = False

print 'bug_id' + lib.sep + 'reporter' + lib.sep + 'report_time' + lib.sep + 'status' + lib.sep + 'resolution' + lib.sep + 'severity' + lib.sep + 'priority' + lib.sep + 'os' + lib.sep + 'product' + lib.sep + 'component' + lib.sep + 'version' + lib.sep + 'assigned_to' + lib.sep + 'target_milestone' + lib.sep + 'cc'

# begin to read activity_level2
# the input file has been sorted by bug_id, so after we read all the lines about a bug, we can set down to deal with it.
# in other words, we deal with a bug when we see a new bug_id

cur_bug_id = ''
cur_bug = issue()

def read_activity_level2_body(header, raw, curline):
	global cur_bug_id
	global cur_bug

	# we pack the information in a row into class pack
	bug_id = raw[header['bug_id']]
	what = raw[header['what']]
	pack = act_pack()
	pack.time = int(raw[header['when']])
	pack.who = raw[header['who']]
	pack.old = raw[header['old']]
	pack.new = raw[header['new']]

	if bug_id != cur_bug_id:
		# we find a new bug (except cur_bug_id == ''. it happens at the first line of the first bug)
		if cur_bug_id != '':
			# ok, we see a new bug, meaning the information of cur_bug has been collected. so deal with it.
			build_issue_time_series(cur_bug_id, cur_bug)
		# initialize for new bug
		cur_bug = issue()
		cur_bug_id = bug_id
		cur_bug.bug_id = bug_id
	
	# append the pack to cooresponding array
	if what == 'Assignee':
		cur_bug.assigned_to.append(pack)
	elif what == 'CC':
		cur_bug.cc.append(pack)
	elif what == 'Component':
		cur_bug.component.append(pack)
	elif what == 'OS':
		cur_bug.os.append(pack)
	elif what == 'Priority':
		cur_bug.priority.append(pack)
	elif what == 'Product':
		cur_bug.product.append(pack)
	elif what == 'Resolution':
		cur_bug.resolution.append(pack)
	elif what == 'Severity':
		cur_bug.severity.append(pack)
	elif what == 'Status':
		cur_bug.status.append(pack)
	elif what == 'Target Milestone':
		cur_bug.target_milestone.append(pack)
	elif what == 'Version':
		cur_bug.version.append(pack)

lib.read_file(sys.argv[2], lib.empty_header, read_activity_level2_body)

# note that we need to deal with the last one. it would be ignored by the loop
if cur_bug_id != '':
	build_issue_time_series(cur_bug_id, cur_bug)
