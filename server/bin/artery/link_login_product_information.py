#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-02-20
# Function: link assigning performance for a login on product
# Parameters: 1) llevel4_*
#	      2) login_product_information
#	      3) product_convertion
#             4) option: product field name
# Output Stream: linked llevel4_*

import sys
import leon_lib as lib

# product field name
field_name = 'new'
if sys.argv.__len__() == 5:
	field_name = sys.argv[4]

# read product_convertion
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[3])

# read product_information
n_tri = {}
n_cor_tri = {}

def read_body(header, raw, curline):
	login = raw[header['login']]
	product = raw[header['product']]
	field = raw[header['field']]
	# n_tri
	n_tris = raw[header['n_tri']].split(lib.tsep)
	tris = []
	for str_tri in n_tris:
		raw_tri = str_tri.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_tri[0])
		newpack.when = int(raw_tri[1])
		tris.append(newpack)
	if not n_tri.has_key(field):
		n_tri[field] = {}
	if not n_tri[field].has_key(login):
		n_tri[field][login] = {}
	n_tri[field][login][product] = tris
	# n_cor_tri
	n_tris = raw[header['n_cor_tri']].split(lib.tsep)
	tris = []
	for str_tri in n_tris:
		if str_tri == '':
			break
		raw_tri = str_tri.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_tri[0])
		newpack.when = int(raw_tri[1])
		tris.append(newpack)
	if not n_cor_tri.has_key(field):
		n_cor_tri[field] = {}
	if not n_cor_tri[field].has_key(login):
		n_cor_tri[field][login] = {}
	n_cor_tri[field][login][product] = tris

lib.read_file(sys.argv[2], lib.empty_header, read_body)

# link to file
def link_header(header, raw, curline ):
	print curline[:-1] + lib.sep + 'nLogPrdTri' + lib.sep + 'nLogPrdCorTri'

def link_body(header, raw, curline):
	login = raw[header['login']]
	new = raw[header[field_name]].lower()
	new = convertion.rename(new)
	when = int(raw[header['when']])
	field = raw[header['field']]
	# n_tri
	n_tri_i = 0
	if n_tri.has_key(field) and n_tri[field].has_key(login) and n_tri[field][login].has_key(new):
		index = lib.binary_search(n_tri[field][login][new], lib.func_time, when)
		if index >= 0:
			n_tri_i = n_tri[field][login][new][index].data
	# n_cor_tri
	n_cor_tri_i = 0
	if n_cor_tri.has_key(field) and n_cor_tri[field].has_key(login) and n_cor_tri[field][login].has_key(new):
		index = lib.binary_search(n_cor_tri[field][login][new], lib.func_time, when)
		if index >= 0:
			n_cor_tri_i = n_cor_tri[field][login][new][index].data
	# output
	print curline[:-1] + lib.sep + str(n_tri_i) + lib.sep + str(n_cor_tri_i)

lib.read_file(sys.argv[1], link_header, link_body)
