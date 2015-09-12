#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-11-16
# Function: link login experience to link file
# Parameters: 1) llevel4_assigning
#	      2) login role
#	      3) name of who field
#	      4) name of when field
#	      5) prefix of output field
# Output stream: linked llevel4_assigning

import sys
import level3_lib as lib3
import leon_lib as lib

# 1) read login_role
# dictionary login -> [list of roles]
rolepacks = {}
def read_role_body(header, raw, curline):
	login = raw[header['who']]
	raw_role = raw[header['role']].split(lib.tsep)
	roles = []
	for str_role in raw_role:
		if str_role == '':
			break
		raw_role = str_role.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = raw_role[0]
		newpack.when = int(raw_role[1])
		roles.append(newpack)
	rolepacks[login] = roles
lib.read_file(sys.argv[2], lib.empty_header, read_role_body)

# 2) link to level4_assigning
def link_header(header, raw, curline):
	print curline[:-1] + lib.sep + sys.argv[5] + '_role' 

def link_body(header, raw, curline):
	login = raw[header[sys.argv[3]]]
	when = int(raw[header[sys.argv[4]]])

	# no one should remain 'unknow'
	role = 'unknow'
	if rolepacks.has_key(login):
		index = lib.binary_search(rolepacks[login], lib.func_time, when)
		if index >= 0:
			role = rolepacks[login][index].data	
	print curline[:-1] + lib.sep + str(role)

lib.read_file(sys.argv[1], link_header, link_body)
