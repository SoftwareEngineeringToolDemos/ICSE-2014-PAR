#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-11
# Function: generate llevel4_info from llevel3
# Paremeters: llevel3
# Output stream: llevel4_info

import sys
import level3_lib as lib3
import leon_lib as lib

file = open(sys.argv[1], 'r')

def get_time(actpack):
	return actpack.when

def print_modifiers_and_transfer_info(actpacks, left_status_time, right_status_time, title, answer, is_rej, products):
	[left, right] = lib3.find_info_within_time_range(actpacks, get_time, left_status_time, right_status_time)
	if left != -1:
		# has version activities
		for index in range(left, right):
			login = actpacks[index].login
			time = actpacks[index].when
			# find product value at that time
			product_index = lib3.binary_search(products, get_time, time)
			product_value = products[product_index].value
			new = actpacks[index].value
			old = '---'
			if index > 0:
				old = actpacks[index-1].value
				print bug_id + lib.sep + title + lib.sep + login + lib.sep + str(time) + lib.sep + old + lib.sep + new + lib.sep + answer + lib.sep + product_value
	if is_rej:
		return
	# status transfer triage
	new_index = lib3.binary_search(actpacks, get_time, right_status_time)
	new = actpacks[new_index].value
	# finad product value at that time
	product_index = lib3.binary_search(products, get_time, right_status_time)
	product_value = products[product_index].value
	old = new

	print bug_id + lib.sep + title + lib.sep + status_login + lib.sep + str(right_status_time) + lib.sep + old + lib.sep + new + lib.sep + answer + lib.sep + product_value

fields = {}

first_line = True
for curline in file:
	# make field index hash
	if first_line:
		raw = curline[:-1].split(lib.sep)
		index = 0
		for field in raw:
			fields[field] = index
			index += 1
		first_line = False
		print 'bug_id;field;login;when;old;new;final;tt_prod'
		continue
	# data
	raw = curline[:-1].split(lib.sep)
	bug_id = raw[fields['bug_id']]

	# prepare act_pack
	resos = lib3.build_act_packs(raw[fields['resolution']])
	versions = lib3.build_act_packs(raw[fields['version']])
	oses = lib3.build_act_packs(raw[fields['os']])
	severities = lib3.build_act_packs(raw[fields['severity']])
	priorities = lib3.build_act_packs(raw[fields['priority']])
	products = lib3.build_act_packs(raw[fields['product']])
	# find final values (answers of the fields)
	version_answer = versions[-1].value
	os_answer = oses[-1].value
	severity_answer = severities[-1].value
	priority_answer = priorities[-1].value
	# find triage phase
	# process if one was found
	# the start time of a phase, -1 means not found start point(UNCONFIRMED) yet
	left_status_time = -1

	statuses = lib3.build_act_packs(raw[fields['status']])
	for status in statuses:
		status_name = status.value
		status_time = status.when
		status_login = status.login

		if left_status_time == -1:
			if status_name == 'UNCONFIRMED':
				left_status_time = status_time
		else:
			# wait for the end of triage phase
			if status_name == 'NEW' or status_name == 'ASSIGNED' or status_name == 'RESOLVED':
				right_status_time = status_time
				# get the resolution if case of 'RESOLVED'
				is_rej = False
				if status_name == 'RESOLVED':
					is_rej = True
					index = lib3.binary_search(resos, get_time, status_time)
					if index >= 0:
						resolution = resos[index].value
						if resolution == 'FIXED':
							is_rej = False
				# find activities
				# version, os, severity, priority
				print_modifiers_and_transfer_info(versions, left_status_time, right_status_time, 'version', version_answer, is_rej, products)
				print_modifiers_and_transfer_info(oses, left_status_time, right_status_time, 'os', os_answer, is_rej, products)
				print_modifiers_and_transfer_info(severities, left_status_time, right_status_time, 'severity', severity_answer, is_rej, products)
				print_modifiers_and_transfer_info(priorities, left_status_time, right_status_time, 'priority', priority_answer, is_rej, products)
				# reset status
				left_status_time = -1
file.close()

