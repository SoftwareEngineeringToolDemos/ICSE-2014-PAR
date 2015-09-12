#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-20
# Function: link peer information to llevel4_assigning
# Parameters: 1) llevel4_assigning
#	      2) contacter file
# Output Stream: linked llevel4_assigning

import sys
import leon_lib as lib

# read contact info
# dictionary login -> [list of <peer_num,when> tuples]
con_num = {}
# dictionary login -> [list of <peer_max_exp,when> tuples]
con_exp = {}
def read_contact_info(header, raw, curline):
	global con_num, con_exp
	login = raw[header['login']]
	
	# number
	raw_nums = raw[header['contacter_num']].split(lib.tsep)
	num_packs = []
	for raw_num in raw_nums:
		if raw_num == '':
			continue
		raw_pack = raw_num.split(lib.fsep)
		num = int(raw_pack[0])
		time = int(raw_pack[1])
		newpack = lib.infopack()
		newpack.data = num
		newpack.when = time
		num_packs.append(newpack)
	con_num[login] = num_packs

	# exp
	raw_exps = raw[header['max_contecter_exp']].split(lib.tsep)
	exp_packs = []
	for raw_exp in raw_exps:
		if raw_exp == '':
			continue
		raw_pack = raw_exp.split(lib.fsep)
		exp = int(raw_pack[0])
		time = int(raw_pack[1])
		newpack = lib.infopack()
		newpack.data = exp
		newpack.when = time
		exp_packs.append(newpack)
	con_exp[login] = exp_packs
lib.read_file(sys.argv[2], lib.empty_header, read_contact_info)

# link to target file
def link_header(header, raw, curline):
	print curline[:-1] + lib.sep + 'cnt_num' + lib.sep + 'cnt_max_exp'
	
def link_body(header, raw, curline):
	global con_num, con_exp, con_dev

	login = raw[header['login']]
	when = int(raw[header['when']])

	# num
	num = 0
	if con_num.has_key(login):
		num_index = lib.binary_search(con_num[login], lib.func_time, when)
		if num_index >= 0:
			num = con_num[login][num_index].data
	# exp
	exp = 0
	if con_exp.has_key(login):
		exp_index = lib.binary_search(con_exp[login], lib.func_time, when)
		if exp_index >= 0:
			exp = con_exp[login][exp_index].data
	
	print curline[:-1] + lib.sep + str(num) + lib.sep + str(exp)
lib.read_file(sys.argv[1], link_header, link_body)

