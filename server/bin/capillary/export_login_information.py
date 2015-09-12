#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-02-12
# Function: generate login performance record
# Parameters: 1) llevel4_assigning
#	      2) product_convertion
# Output Stream: login performance

import sys
import leon_lib as lib

# read product_convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[2])

# read level5
n_assi = {}
n_cor_assi = {}

def read_body(header, raw, curline):
	# if the deal is valied when get resolved
	valid_t = int(raw[header['valid_t']])
	bug_id = raw[header['bug_id']]
	field = raw[header['field']]
	
	# ignore not valid and not resolved
	if field != 'product' or valid_t < 0:
		return
	
	login = raw[header['login']]
	new = convertion.rename(raw[header['new']].lower())
	final = convertion.rename(raw[header['final']].lower())

	# n_assi
	if not n_assi.has_key(login):
		n_assi[login] = {}
	if not n_assi[login].has_key(valid_t):
		n_assi[login][valid_t] = 0
	n_assi[login][valid_t] += 1
	# n_cor_assi
	if new == final or convertion.is_correct(new, final):
		if not n_cor_assi.has_key(login):
			n_cor_assi[login] = {}
		if not n_cor_assi[login].has_key(valid_t):
			n_cor_assi[login][valid_t] = 0
		n_cor_assi[login][valid_t] += 1

lib.read_file(sys.argv[1], lib.empty_header, read_body)

# output
print 'login' + lib.sep + 'n_assi' + lib.sep + 'n_cor_assi'
for login in n_assi:
	# n_assi
	str_assi = ''
	timelist = sorted(n_assi[login].keys())
	count = 0
	for time in timelist:
		count += n_assi[login][time]
		str_assi += str(count) + lib.fsep + str(time) + lib.tsep
	if str_assi.__len__() > 0:
		str_assi = str_assi[:-lib.tsep.__len__()]
	# n_cor_assi
	str_cor_assi = ''
	if n_cor_assi.has_key(login):
		timelist = sorted(n_cor_assi[login].keys())
		count = 0
		for time in timelist:
			count += n_cor_assi[login][time]
			str_cor_assi += str(count) + lib.fsep + str(time) + lib.tsep
		if str_cor_assi.__len__() > 0:
			str_cor_assi = str_cor_assi[:-lib.tsep.__len__()]
	# output
	print login + lib.sep + str_assi + lib.sep + str_cor_assi

