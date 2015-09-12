#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-02-20
# Function: link assigning performation of a login to llevel4_assigning
# Parameters: 1) llevel4_assigning
#	      2) login_information
#	      3) product_convertion
# Output Stream: linked llevel4_assigning

import sys
import leon_lib as lib

# read product_convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[3])

# read product_information
n_assi = {}
n_cor_assi = {}

def read_body(header, raw, curline):
	login = raw[header['login']]
	# n_assi
	n_assis = raw[header['n_assi']].split(lib.tsep)
	assis = []
	for str_assi in n_assis:
		raw_assi = str_assi.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_assi[0])
		newpack.when = int(raw_assi[1])
		assis.append(newpack)
	n_assi[login] = assis
	# n_cor_assi
	n_assis = raw[header['n_cor_assi']].split(lib.tsep)
	assis = []
	for str_assi in n_assis:
		if str_assi == '':
			break
		raw_assi = str_assi.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_assi[0])
		newpack.when = int(raw_assi[1])
		assis.append(newpack)
	n_cor_assi[login] = assis

lib.read_file(sys.argv[2], lib.empty_header, read_body)

# link to file
def link_header(header, raw, curline ):
	print curline[:-1] + lib.sep + 'nLogAssi' + lib.sep + 'nLogCorAssi'

def link_body(header, raw, curline):
	login = raw[header['login']]
	when = int(raw[header['when']])
	# n_assi
	n_assi_i = 0
	if n_assi.has_key(login):
		index = lib.binary_search(n_assi[login], lib.func_time, when)
		if index >= 0:
			n_assi_i = n_assi[login][index].data
	# n_cor_assi
	n_cor_assi_i = 0
	if n_cor_assi.has_key(login):
		index = lib.binary_search(n_cor_assi[login], lib.func_time, when)
		if index >= 0:
			n_cor_assi_i = n_cor_assi[login][index].data
	# output
	print curline[:-1] + lib.sep + str(n_assi_i) + lib.sep + str(n_cor_assi_i)

lib.read_file(sys.argv[1], link_header, link_body)
