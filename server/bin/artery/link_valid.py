#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-13
# Function: link if the final value (correct column) is valid to level4_assigning
# Parameters: 1) level4_assigning or level4_info
#	      2) activity_level2
#	      3) llevel3
# 	      4) 0-assigning 1-info
# Ouput stream: linked level4_assigning
# Last check: 2013-02-26

# Strategy: the correctness is valid when in one of the following cases:
# 1) the issue has been RESOLVED and the resolution is FIXED, set valid to RESOLVED time
# 2) the issue has been RESOLVED and the resolution is non-FIXED and it has been confirmed, set valid to RESOLVED time
# 3) the issue has been RESOLVED and the resolution is not FIXED and it has not been confirmed, there're validate acts after setting the final value, set valid to the max(RESOLVED time, time of first valid act)
# in other cases, we set valid to -1

# for type == '2'
# 1) the issue has been RESOLVED, set valid to RESOLVED time

import sys
import leon_lib as lib

llevel4_type = sys.argv[4]

# define the fields, which modification may validate the final value
if llevel4_type == '0':
	valid_act = set(['OS','Priority','Severity','Version','Blocks','Depends on','Hardware','Flags','Target Milestone'])
elif llevel4_type == '1':
	valid_act = set(['Product','Component','Blocks','Depends on','Hardware','Flags','Target Milestone'])
	field_set = set(['severity','priority','version','os'])
elif llevel4_type == '2':
	valid_act = set()

# read llevel3 to check resolving time and final resolution
# dictionary bug_id -> resolving time, -1 if not resolved
bug_resolving_time = {}
# set is FIXED
bug_fixed = set()
# set has confirmed bug
bug_confirmed = set()
# dictionary bug_id -> the time final value is set
bug_final_time = {}

def read_llevel3_body(header, raw, curline):
	bug_id = raw[header['bug_id']]

	# resolving time and has been confirmed?
	global bug_resolving_time
	global bug_confirmed
	statuses = raw[header['status']].split(lib.tsep)
	statuses.reverse()
	for status in statuses:
		raw_status = status.split(lib.fsep)
		name = raw_status[0]
		if name == 'RESOLVED' and not bug_resolving_time.has_key(bug_id):
			when = int(raw_status[1])
			bug_resolving_time[bug_id] = when
		elif llevel4_type == '2':
			continue
		elif (name == 'NEW' or name == 'ASSIGNED') and not bug_id in bug_confirmed:
			bug_confirmed.add(bug_id)
		# we do not think REOPEN may change the product assignment
	
	if llevel4_type == '2':
		# llevel4 only considers resolved time
		return
	# bug_final_resolution
	if not bug_resolving_time.has_key(bug_id) or bug_id in bug_confirmed:
		# no need to care about it
		return
	
	global bug_fixed
	final_resolution = (raw[header['resolution']].split(lib.tsep)[-1]).split(lib.fsep)[0]
	if final_resolution == 'FIXED':
		bug_fixed.add(bug_id)

	# setting final value time
	global bug_final_time
	if bug_id in bug_fixed:
		# no need to care about it
		return
	if llevel4_type == '0':
		final_time = int((raw[header['product']].split(lib.tsep)[-1]).split(lib.fsep)[1])
  		bug_final_time[bug_id] = final_time
	elif llevel4_type == '1':
    		# get time for fields in field_set
   		 bug_final_time[bug_id] = {}
		 for field in field_set:
			final_time = int((raw[header[field]].split(lib.tsep)[-1]).split(lib.fsep)[1])
			bug_final_time[bug_id][field] = final_time

# read llevel3
lib.read_file(sys.argv[3], lib.empty_header, read_llevel3_body)

# bug_id -> the first time of verifying the final action
bug_verifying_time = {}

# read activity level2
def read_level2(header, raw, curline):
	global bug_resolving_time
	global bug_confirmed
	global bug_fixed
	global bug_final_time

	bug_id = raw[header['bug_id']]
	
	# we ignore some bugs, because they don't need this information
	if (not bug_resolving_time.has_key(bug_id)) or (bug_id in bug_confirmed) or (bug_id in bug_fixed) or (not bug_final_time.has_key(bug_id)):
		return

	# we really need the time
	when = int(raw[header['when']])
	field = raw[header['what']]
	
	if not field in valid_act:
		return
	elif llevel4_type == '0'  and when > bug_final_time[bug_id]:
		if not bug_verifying_time.has_key(bug_id):
			bug_verifying_time[bug_id] = when
		elif bug_verifying_time[bug_id] > when:
			bug_verifying_time[bug_id] = when
	elif llevel4_type == '1':
		for field in field_set:
			if when > bug_final_time[bug_id][field]:
				if not bug_verifying_time.has_key(bug_id):
					bug_verifying_time[bug_id] = {field:when}
				elif not bug_verifying_time[bug_id].has_key(field):
					bug_verifying_time[bug_id][field] = when
				elif bug_verifying_time[bug_id][field] > when:
					bug_verifying_time[bug_id][field] = when

if llevel4_type != '2':
	lib.read_file(sys.argv[2], lib.empty_header, read_level2)

# link to target file
def link_header(header, raw, curline):
	print curline[:-1] + lib.sep + 'valid_t'

def link_body(header, raw, curline):
	out = curline[:-1] + lib.sep
	bug_id = raw[header['bug_id']]
	when = int(raw[header['when']])
	new = raw[header['new']]
	field = raw[header['field']]
	
	global bug_resolving_time
	global bug_fixed
	global bug_confirmed
	global bug_verifying_time

	if not bug_resolving_time.has_key(bug_id):
		# resolved?
		out += '-1'
	elif llevel4_type == '2':
		# has record in bug_resolving time
		out += str(bug_resolving_time[bug_id])
	elif bug_id in bug_fixed or bug_id in bug_confirmed:
		# fixed? or has been confirmed?
		out += str(bug_resolving_time[bug_id])
	elif not bug_verifying_time.has_key(bug_id):
	# verifying
		out += '-1'
	else:
		if llevel4_type == '0':
			out += str(max(bug_resolving_time[bug_id], bug_verifying_time[bug_id]))
		elif llevel4_type == '1':
			if not bug_verifying_time[bug_id].has_key(field):
				out += '-1'
			else:
				out += str(max(bug_resolving_time[bug_id], bug_verifying_time[bug_id][field]))
	print out

lib.read_file(sys.argv[1], link_header, link_body)
