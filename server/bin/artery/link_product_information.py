#!/usr/bin/python

# Author: Xie Jialinag
# Date: 2013-02-22
# Function: link assigning performance on product to llevel4_assigning
# Parameters: 1) llevel4_assinging
#	      2) product_information
#	      3) product_convertion
#	      4) option: product field name
# Output Stream: linked llevel4_assigning

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
	n_tri[field][product] = tris
	# n_cor_tri
	n_tris = raw[header['n_cor_tri']].split(lib.tsep)
	tris = []
	for str_tri in n_tris:
		raw_tri = str_tri.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_tri[0])
		newpack.when = int(raw_tri[1])
		tris.append(newpack)
	if not n_cor_tri.has_key(field):
		n_cor_tri[field] = {}
	n_cor_tri[field][product] = tris

lib.read_file(sys.argv[2], lib.empty_header, read_body)

# link to file
def link_header(header, raw, curline ):
	print curline[:-1] + lib.sep + 'nPrdTri' + lib.sep + 'nPrdCorTri' + lib.sep + 'nAllTri' + lib.sep + 'nAllCorTri'

def link_body(header, raw, curline):
	new = raw[header[field_name]].lower()
	new = convertion.rename(new)
	when = int(raw[header['when']])
	field = raw[header['field']]
	# n_tri
	n_tri_i = 0
	if n_tri.has_key(field) and n_tri[field].has_key(new):
		index = lib.binary_search(n_tri[field][new], lib.func_time, when)
		if index >= 0:
			n_tri_i = n_tri[field][new][index].data
	# n_cor_tri
	n_cor_tri_i = 0
	if n_cor_tri.has_key(field) and n_cor_tri[field].has_key(new):
		index = lib.binary_search(n_cor_tri[field][new], lib.func_time, when)
		if index >= 0:
			n_cor_tri_i = n_cor_tri[field][new][index].data
	
	# for overall products
	n_all_tri_i = 0
	if n_tri.has_key(field):
		for prd in n_tri[field]:
			index = lib.binary_search(n_tri[field][prd], lib.func_time, when)
			if index >= 0:
				n_all_tri_i += n_tri[field][prd][index].data
	n_all_cor_tri_i = 0
	if n_cor_tri.has_key(field):
		for prd in n_cor_tri[field]:
			index = lib.binary_search(n_cor_tri[field][prd], lib.func_time, when)
			if index >= 0:
				n_all_cor_tri_i += n_cor_tri[field][prd][index].data
	
	# output
	print curline[:-1] + lib.sep + str(n_tri_i) + lib.sep + str(n_cor_tri_i) + lib.sep + str(n_all_tri_i) + lib.sep + str(n_all_cor_tri_i)

lib.read_file(sys.argv[1], link_header, link_body)
