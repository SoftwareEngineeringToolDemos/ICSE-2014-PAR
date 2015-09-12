#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-02-20
# Function: generate llevel4_filtering from llevel3
# Parameter: llevel3
# Output Stream: llevel4_filtering

import sys
import level3_lib as lib

file = open(sys.argv[1], 'r')

def get_time(actpack):
	return actpack.when

def print_modifiers_and_transfer_info(actpacks, left_status_time, right_status_time, title, answer):
	[left, right] = lib.find_info_within_time_range(actpacks, get_time, left_status_time, right_status_time)
	if left != -1:
		# has version activities
		for index in range(left, right):
			login = actpacks[index].login
			time = actpacks[index].when
			new = actpacks[index].value
			old = '---'
			if index > 0:
				old = actpacks[index-1].value
				print bug_id + ';' + title + ';' + login + ';' + str(time) + ';' + old + ';' + new + ';' + answer
	# status transfer triage
	new_index = lib.binary_search(actpacks, get_time, status_time)
	new = actpacks[new_index].value
	old = new
	print bug_id + ';' + title + ';' + status_login + ';' + str(status_time) + ';' + old + ';' + new + ';' + answer

fields = {}

first_line = True
for curline in file:
	# make field index hash
	if first_line:
		raw = curline[:-1].split(';')
		index = 0
		for field in raw:
			fields[field] = index
			index += 1
		first_line = False
		print 'bug_id;field;login;when;new;final;new_reso;final_reso;tt_prod'
		continue
	# data
	raw = curline[:-1].split(';')
	bug_id = raw[fields['bug_id']]

	# find triage phase
	# process if one was found
	# the start time of a phase, -1 means not found start point(UNCONFIRMED) yet
	left_status_time = -1

	resolutions = lib.build_act_packs(raw[fields['resolution']])
	resolution_final = resolutions[-1].value
	
	statuses = lib.build_act_packs(raw[fields['status']])
	status_final = statuses[-1].value
	products = lib.build_act_packs(raw[fields['product']])

	# answer
	answer = ''
	if resolution_final == 'FIXED':
		answer = 'confirm'
	elif resolution_final == '---':
		# not resolved yet, skip
		continue
	else:
		answer = 'reject'

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
				
				product_index = lib.binary_search(products, get_time, status_time)
				product = products[product_index].value

				if status_name == 'NEW' or status_name == 'ASSIGNED':
					# confirm activity
					act = 'confirm'
					print bug_id + ';confirm;' + status_login + ';' + str(status_time) + ';' + act + ';' + answer + ';confirm;' + resolution_final + ';' + product
				else:
					# resolved, look at resolution
					resolution_index = lib.binary_search(resolutions, get_time, status_time)
					resolution = resolutions[resolution_index].value
					if resolution != 'FIXED':
						act = 'reject'
						print bug_id + ';confirm;' + status_login + ';' + str(status_time) + ';' + act + ';' + answer + ';' + resolution + ';' + resolution_final + ';' + product
					else:
						# directly fixed
						act = 'confirm'
						print bug_id + ';confirm;' + status_login + ';' + str(status_time) + ';' + act + ';' + answer + ';confirm;' + resolution_final + ';' + product
				
				left_status_time = -1
file.close()

