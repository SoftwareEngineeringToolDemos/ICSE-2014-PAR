#!/usr/bin/python

# Author: Xie Jialiang
# Data: 2012-12-20
# Function: generate login experience
# Parameters: 1) llevel4_filtering
#	      2) llevel4_assigning
#	      3) llevel4_info
#	      4) llevel3
#	      5) product_convertion
# Output Stream: login_experience

import sys
import leon_lib as lib

# read product convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[5])

# read leon_level3
resolved_time = lib.resolved_time_checker()
resolved_time.read(sys.argv[4])

# read final product
bug_final_product = {}
def read_final_product_body(header, raw, curline):
	global bug_final_product
	bug_id = raw[header['bug_id']]
	final_product = (raw[header['product']].split(lib.tsep)[-1]).split(lib.fsep)[0]
	bug_final_product[bug_id] = final_product
lib.read_file(sys.argv[4], lib.empty_header, read_final_product_body)

# add to dict
def add_to_dict(dict, a, b, c):
	if not dict.has_key(a):
		dict[a] = {}
	if not dict[a].has_key(b):
		dict[a][b] = {}
	if not dict[a][b].has_key(c):
		dict[a][b][c] = 0
	dict[a][b][c] += 1

logPrdAssi = {}
logPrdNotAssi = {}

def read_triage_body(header, raw, curline):
	global logPrdAssi 
	global logPrdNotAssi 
	
	bug_id = raw[header['bug_id']]
	login = raw[header['login']]
	field = raw[header['field']]
	when_resolved = resolved_time.get_resolved_time(bug_id)

	# ignore not resolved
	if when_resolved == -1:
		return
	# ignore not valid
	if header.has_key('valid'):
		valid = bool(raw[header['valid']])
		if not valid:
			return
	# get product
	product = ''
	if bug_final_product.has_key(bug_id):
		product = bug_final_product[bug_id]
	# add to num
	if field == 'product':
		add_to_dict(logPrdAssi, login, product, when_resolved)
	else:
		add_to_dict(logPrdNotAssi, login, product, when_resolved)

# read level4_assigning
lib.read_file(sys.argv[2], lib.empty_header, read_triage_body)

# read level4_info
lib.read_file(sys.argv[3], lib.empty_header, read_triage_body)

# read confirm
lib.read_file(sys.argv[1], lib.empty_header, read_triage_body)

# new output
print 'login' + lib.sep + 'product' + lib.sep + 'num' + lib.sep + 'type'
def output_file(logdict, mark):
	for login in logdict:
		for product in logdict[login]:
			str_out = ''
			times = sorted(logdict[login][product].keys())
			count = 0
			for time in times:
				count += logdict[login][product][time]
				str_out += str(count) + lib.fsep + str(time) + lib.tsep
			if str_out.__len__() > 0:
				str_out = login + lib.sep + product + lib.sep + str_out[:-lib.tsep.__len__()] + lib.sep + mark
				print str_out


output_file(logPrdAssi, 'prdAssi')
output_file(logPrdNotAssi, 'prdNotAssi')

