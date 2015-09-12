#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-12
# Function: link experience to llevel4_assigning
# Parameters: 1) llevel4_assigning
#	      2) login_experience
#	      3) product_convertion
# Output Stream: linked llevel4_assigning
# Detail: linked information includes
# 	      1) ExpPrdAssi
# 	      2) ExpPrdNotAssi
# 	      3) ExpNotPrdAssi
# 	      4) ExpNotPrdNotAssi

import sys
import leon_lib as lib

# read product_convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[3])

# read product_information
logPrdAssi = {}
logPrdNotAssi = {}

def read_body(header, raw, curline):
	login = raw[header['login']]
	product = raw[header['product']]
	type = raw[header['type']]

	raw_nums = raw[header['num']].split(lib.tsep)
	nums = []
	for str_num in raw_nums:
		raw_num = str_num.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_num[0])
		newpack.when = int(raw_num[1])
		nums.append(newpack)
	if type == 'prdAssi':
		if not logPrdAssi.has_key(login):
			logPrdAssi[login] = {}
		logPrdAssi[login][product] = nums
	elif type == 'prdNotAssi':
		if not logPrdNotAssi.has_key(login):
			logPrdNotAssi[login] = {}
		logPrdNotAssi[login][product] = nums

lib.read_file(sys.argv[2], lib.empty_header, read_body)

# link to file
def link_header(header, raw, curline ):
	print curline[:-1] + lib.sep + 'ExpPrdAssi' + lib.sep + 'ExpPrdNotAssi' + lib.sep + 'ExpNotPrdAssi' + lib.sep + 'ExpNotPrdNotAssi'

def link_body(header, raw, curline):
	login = raw[header['login']]
	new = raw[header['new']].lower()
	new = convertion.rename(new)
	when = int(raw[header['when']])

	# expPrdAssi
	expPrdAssi = 0
	if logPrdAssi.has_key(login) and logPrdAssi[login].has_key(new):
		index = lib.binary_search(logPrdAssi[login][new], lib.func_time, when)
		if index >= 0:
			expPrdAssi = logPrdAssi[login][new][index].data
	
	# expPrdNotAssi
	expPrdNotAssi = 0
	if logPrdNotAssi.has_key(login) and logPrdNotAssi[login].has_key(new):
		index = lib.binary_search(logPrdNotAssi[login][new], lib.func_time, when)
		if index >= 0:
			expPrdNotAssi = logPrdNotAssi[login][new][index].data

	# expNotPrdAssi
	expNotPrdAssi = 0
	if logPrdAssi.has_key(login):
		for product in logPrdAssi[login]:
			if product == new:
				continue
			index = lib.binary_search(logPrdAssi[login][product], lib.func_time, when)
			if index >= 0:
				expNotPrdAssi += logPrdAssi[login][product][index].data
	# expNotPrdNotAssi
	expNotPrdNotAssi = 0
	if logPrdNotAssi.has_key(login):
		for product in logPrdNotAssi[login]:
			if product == new:
				continue
			index = lib.binary_search(logPrdNotAssi[login][product], lib.func_time, when)
			if index >= 0:
				expNotPrdNotAssi += logPrdNotAssi[login][product][index].data
	# output
	print curline[:-1] + lib.sep + str(expPrdAssi) + lib.sep + str(expPrdNotAssi) + lib.sep + str(expNotPrdAssi) + lib.sep + str(expNotPrdNotAssi)

lib.read_file(sys.argv[1], link_header, link_body)
