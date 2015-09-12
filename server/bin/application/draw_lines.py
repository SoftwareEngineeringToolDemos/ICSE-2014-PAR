#!/usr/bin/python

import sys
import leon_lib as lib

sep = ','

def read_head(header, raw, curline):
	pass

def get_num_time(raw):
	tmp = raw.split(lib.fsep)
	return [int(tmp[0]), int(tmp[1])]


def read_body(header, raw, curline):
	product = raw[header['product']]

	nTri = raw[header['n_tri']].split(lib.tsep)
	nCorTri = raw[header['n_cor_tri']].split(lib.tsep)

	nCorTriIndex = 0
	[nCorTriNum, nCorTriTime] = get_num_time(nCorTri[nCorTriIndex])
	nCorCur = 0

	rest = 'product'
	res = product
	for tri in nTri:
		[nTriNum, nTriTime] = get_num_time(tri)
		if nTriTime >= nCorTriTime:
			nCorCur = nCorTriNum
			nCorTriIndex += 1
			if nCorTriIndex < nCorTri.__len__():
				[nCorTriNum, nCorTriTime] = get_num_time(nCorTri[nCorTriIndex])
		rest += sep + str(nTriTime)
		res += sep + str(nCorCur*1.0/nTriNum)
	print rest
	print res

lib.read_file(sys.argv[1], read_head, read_body)
