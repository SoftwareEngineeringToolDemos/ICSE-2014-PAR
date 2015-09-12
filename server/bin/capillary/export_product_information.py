#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-02-10
# Function: gerate product triage statistics
# Parameters: 1) llevel4_*
#	      2) product_convertion
#	      3) llevel4 type 0 assigning 1 info
#	      4) option: product field name
# Output Stream: product_information

import sys
import leon_lib as lib

# decide field set
llevel4_type = int(sys.argv[3])
if llevel4_type == 0:
	field_set = set(['product'])
elif llevel4_type == 1:
	field_set = set(['version', 'severity', 'priority', 'os'])
elif llevel4_type == 2:
	field_set = set(['confirm'])

# product field name
product_field_name = 'new'
if sys.argv.__len__() > 4:
	product_field_name = sys.argv[4]

# initialize rename
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[2])

# product error rate
# field -> product -> when -> number of correct triage
n_cor_tri = {}
# field -> product -> when -> number of triage
n_tri = {}

for field in field_set:
	n_cor_tri[field] = {}
	n_tri[field] = {}

def read_body(header, raw, curline):
	global n_cor_tri
	global n_tri

	field = raw[header['field']]
	# we record the info when it is valid
	valid_t = int(raw[header['valid_t']])
	bug_id = raw[header['bug_id']]

	# only count valid product and resolved deals
	if not field in field_set or valid_t < 0: 
		return

	product = convertion.rename(raw[header[product_field_name]].lower())
	is_correct = (raw[header['correct']] == 'True')

	# n_tri
	if not n_tri[field].has_key(product):
		n_tri[field][product] = {}
	if not n_tri[field][product].has_key(valid_t):
		n_tri[field][product][valid_t] = 0
	n_tri[field][product][valid_t] += 1

	# n_cor_tri
	if is_correct:
		if not n_cor_tri[field].has_key(product):
			n_cor_tri[field][product] = {}
		if not n_cor_tri[field][product].has_key(valid_t):
			n_cor_tri[field][product][valid_t] = 0
		n_cor_tri[field][product][valid_t] += 1

lib.read_file(sys.argv[1], lib.empty_header, read_body)

# output
print 'product' + lib.sep + 'field' + lib.sep + 'n_tri' + lib.sep + 'n_cor_tri'
for field in n_tri:
	for product in n_tri[field]:
		# n_tri
		timelist = sorted(n_tri[field][product].keys())
		str_n_tri = ''
		count = 0
		for time in timelist:
			count += n_tri[field][product][time]
			str_n_tri += str(count) + lib.fsep + str(time) + lib.tsep
		if str_n_tri.__len__() > 0:
			str_n_tri = str_n_tri[:-lib.tsep.__len__()]
		# n_cor_tri
		str_n_cor_tri = ''
		if not n_cor_tri[field].has_key(product):
			continue
		timelist = sorted(n_cor_tri[field][product].keys())
		count = 0
		for time in timelist:
			count += n_cor_tri[field][product][time]
			str_n_cor_tri += str(count) + lib.fsep + str(time) + lib.tsep
		if str_n_cor_tri.__len__() > 0:
			str_n_cor_tri = str_n_cor_tri[:-lib.tsep.__len__()]
		# output all
		print product + lib.sep + field + lib.sep + str_n_tri + lib.sep + str_n_cor_tri

