#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-11
# Function: link correct or not to level4_assigning
# Parameters: 1) level4_assigning
#	      2) product convertion
# Output stream: linked level4_assigning
# Warning: component and product-component are disable

import sys
import leon_lib as lib

# read product chain
convertion = lib.product_convertion()
convertion.read_product_convertion(sys.argv[2])

# read target file
header = {}
first = True

# TODO: move the loop into framework

file = open(sys.argv[1], 'r')
for curline in file:
	raw = curline[:-1].split(lib.sep)
	# header
	if first:
		for title in raw:
			header[title] = header.__len__()
		first = False
		print curline[:-1] + lib.sep + 'correct'
		continue
	# body
	old = raw[header['old']].lower()
	new = raw[header['new']].lower()
	final = raw[header['final']].lower()
	field = raw[header['field']]

	# the logic is, if new == final or new product is finally rename to final, it is correct
	if field == 'product':
		if new == final or convertion.is_correct(new, final):
			correct = True
		else:
			correct = False
		print curline[:-1] + lib.sep + str(correct)
file.close()
