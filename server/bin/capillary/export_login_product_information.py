#!/usr/bin/python

# Author: Xie Jialinag
# Date: 2013-02-16
# Function: generate login performance on product
# Parameters: 1) llevel4_*
#	      2) product_convertion
#	      3) llevel4 type 0 assigning 1 info
#	      4) option: product field name
# Ouput Stream: login_product_information
# Strategy: we use delay statistic

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

# read product_convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[2])

# read level5
# dictionary field -> login -> product -> time -> login's assignment on the product at time
n_tri = {}
# dictionary field -> login -> product -> time -> login's correct assignment on the product at time
n_cor_tri = {}

for field in field_set:
	n_tri[field] = {}
	n_cor_tri[field] = {}

def read_body(header, raw, curline):
	bug_id = raw[header['bug_id']]
	# we record the info when it become valid
	valid_t = int(raw[header['valid_t']])
	field = raw[header['field']]
	
	# ignore not valid
	if not field in field_set or valid_t < 0:
		return
	
	login = raw[header['login']]
	product = convertion.rename(raw[header[product_field_name]].lower())
	is_correct = raw[header['correct']] == 'True'

	# n_tri
	if not n_tri[field].has_key(login):
		n_tri[field][login] = {}
	if not n_tri[field][login].has_key(product):
		n_tri[field][login][product] = {}
	if not n_tri[field][login][product].has_key(valid_t):
		n_tri[field][login][product][valid_t] = 0
	n_tri[field][login][product][valid_t] += 1
	# n_cor_tri
	if is_correct:
		if not n_cor_tri[field].has_key(login):
			n_cor_tri[field][login] = {}
		if not n_cor_tri[field][login].has_key(product):
			n_cor_tri[field][login][product] = {}
		if not n_cor_tri[field][login][product].has_key(valid_t):
			n_cor_tri[field][login][product][valid_t] = 0
		n_cor_tri[field][login][product][valid_t] += 1

lib.read_file(sys.argv[1], lib.empty_header, read_body)

# output
print 'login' + lib.sep + 'product' + lib.sep + 'field' + lib.sep + 'n_tri' + lib.sep + 'n_cor_tri'
for field in n_tri:
	for login in n_tri[field]:
		for product in n_tri[field][login]:
			# n_tri
			str_tri = ''
			timelist = sorted(n_tri[field][login][product].keys())
			count = 0
			for time in timelist:
				count += n_tri[field][login][product][time]
				str_tri += str(count) + lib.fsep + str(time) + lib.tsep
			if str_tri.__len__() > 0:
				str_tri = str_tri[:-lib.tsep.__len__()]
			# n_cor_tri
			str_cor_tri = ''
			if n_cor_tri[field].has_key(login) and n_cor_tri[field][login].has_key(product):
				timelist = sorted(n_cor_tri[field][login][product].keys())
				count = 0
				for time in timelist:
					count += n_cor_tri[field][login][product][time]
					str_cor_tri += str(count) + lib.fsep + str(time) + lib.tsep
				if str_cor_tri.__len__() > 0:
					str_cor_tri = str_cor_tri[:-lib.tsep.__len__()]
			# output
			print login + lib.sep + product + lib.sep + field + lib.sep + str_tri + lib.sep + str_cor_tri

