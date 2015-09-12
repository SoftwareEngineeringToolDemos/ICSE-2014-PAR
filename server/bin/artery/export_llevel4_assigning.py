#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-8
# Function: generate product-assigning activities from llevel3
# Parameters: llevel3
# Output Stream: 1) llevel4_assigning
#	         2) product convertion
# Warning: component-assigning and product-component assigning output have been disable
# Warning: assignments because of product convertion will be ignored

import sys
# TODO: move level3_lib into leon_lib and resolve the duplication
import level3_lib as lib3
import leon_lib as lib

# read product convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[2])

# read llevel3
file = open(sys.argv[1], 'r')
err = open('export_assigning.log', 'w')
err.write('bug_id')
has_output = False

# TODO: the function should be duplicated with that in leon_lib. remove it
def get_time(actpack):
	return actpack.when

# TODO: replace actpack with what we have defined in leon_lib

# extract the activities in actpacks between left_status_time and right_status_time. generate a verified activity if is_rej == False
def print_modifiers_and_transfer_info(actpacks, left_status_time, right_status_time, title, answer, is_rej):
	global has_output
	# get the range of indexes of wanted activities
	[left, right] = lib3.find_info_within_time_range(actpacks, get_time, left_status_time, right_status_time)
	# TODO: make sure what would happend if left == -1
	if left != -1:
		# find activities
		for index in range(left, right):
			login = actpacks[index].login
			time = actpacks[index].when
			new = actpacks[index].value
			old = '---'
			# get the old value
			if index > 0:
				old = actpacks[index-1].value
				has_output = True
				# ignore the assignments because of product convertion
				if not convertion.is_correct(old, new):
					print bug_id + lib.sep + title + lib.sep + login + lib.sep + str(time) + lib.sep + convertion.rename(old) + lib.sep + convertion.rename(new) + lib.sep + answer
	# status transfer triage
	# only consider confirmed as activity
	if is_rej:
		return
	new_index = lib3.binary_search(actpacks, get_time, right_status_time)
	new = actpacks[new_index].value
	old = new
	has_output = True
	print bug_id + lib.sep + title + lib.sep + status_login + lib.sep + str(right_status_time) + lib.sep + convertion.rename(old) + lib.sep + convertion.rename(new) + lib.sep + answer

# begin to read llevel3
# TODO: put the loop into our framework
fields = {}
first_line = True
for curline in file:
	# make field index hash
	# TODO: remove it when put into framework, because it has been implemented
	if first_line:
		raw = curline[:-1].split(lib.sep)
		index = 0
		for field in raw:
			fields[field] = index
			index += 1
		first_line = False
		print 'bug_id' + lib.sep + 'field' + lib.sep + 'login' + lib.sep + 'when' + lib.sep + 'old' + lib.sep + 'new' + lib.sep + 'final'
		continue
	# data
	raw = curline[:-1].split(lib.sep)
	bug_id = raw[fields['bug_id']]

	# prepare act_pack
	# build the array from string
	resos = lib3.build_act_packs(raw[fields['resolution']])
	product = lib3.build_act_packs(raw[fields['product']])
	statuses = lib3.build_act_packs(raw[fields['status']])
	
	# find final values (answers of the fields)
	product_answer = product[-1].value
	
	# now scan the statuses and find traige activities
	# traige activities are modifications between UNCONFIRMED and NEW/RESOLVED and
	#   when comfirming the bug (set status to NEW), several activities are made to varifiy each fields 
	# strategy: we scan the statues to find the point of UNCONFIRMED (left) and ASSIGNED/NEW/RESOLVED (right), then extract activities between
	
	# we has not find the left yet, so set it -1
	left_status_time = -1
	has_output = False

	for status in statuses:
		status_name = status.value
		status_time = status.when
		status_login = status.login

		if left_status_time == -1:
			# we've not entering the zone, we expect UNCONFIRMED
			if status_name == 'UNCONFIRMED':
				left_status_time = status_time
		else:
			# we've in the zone, so we expect the end of it (ASSIGNED/NEW/RESOLVED)
			if status_name == 'NEW' or status_name == 'ASSIGNED' or status_name == 'RESOLVED':
				right_status_time = status_time
				# there're two case if we got RESOLVED
				# - bug may be directly fixed
				# - bug may be rejected
				# to distinguish them, we need to check the resolution
				is_rej = False
				if status_name == 'RESOLVED':
					# by default, we assume the bug is rejected
					is_rej = True
					# TODO: use the one in leon_lib
					index = lib3.binary_search(resos, get_time, status_time)
					if index >= 0:
						resolution = resos[index].value
						if resolution == 'FIXED':
							is_rej = False
				# find and print the activities within left and right 
				print_modifiers_and_transfer_info(product, left_status_time, right_status_time, 'product', product_answer, is_rej)
				# reset status
				left_status_time = -1
	if not has_output:
		# TODO: how many bug reach here and why?
		err.write(bug_id + '\n')
file.close()
err.close()
