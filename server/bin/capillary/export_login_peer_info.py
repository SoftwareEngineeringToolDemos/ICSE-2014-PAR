#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-12-20
# Function: generate peer information
# Parameters: 1) lcmt_level2
#	      2) login_general_experience
# Output Stream: peer_information
# Strategy:
# step 1: build the dictionary of login -> when -> peers he met at when
# step 2: build the dictionary of login -> [list of <exp,when> tuples]
# step 3: for each login, scan by sort of time, calculating 1) a set of peers 2) max exp in 1)


import sys
import leon_lib as lib

# step 1: read lcmt_level2 to build login -> when -> set of peers
# for each bug, e.g.
# login;time
# loginA;1
# loginB;3
# loginC;4
#
# loginA has no peer
# loginB has peer loginA at time 3
# loginC has peers loginA and loginB at time 4
#
# so we keep a cur_set, for each new login, it peer set at the time may be cur_set - {login}

class contacters:
	def __init__(self):
		self.logins = set()

# dictionary login -> when -> set of peers login met at when
logins = {}
# set of the peers list by far
cur_set = set()
cur_bug_id = ''

def read_lcmt_level2_body(header, raw, curline):
	global logins
	global cur_set
	global cur_bug_id
	# body
	bug_id = raw[header['bug_id']]
	# new bug
	if bug_id != cur_bug_id:
		cur_bug_id = bug_id
		cur_set = set()

	login = raw[header['who']]
	when = int(raw[header['when']])
	month_aligned_when = lib.month_align(when)
	cur_set.add(login)

	if not logins.has_key(login):
		logins[login] = {}
	if not logins[login].has_key(month_aligned_when):
		logins[login][month_aligned_when] = contacters()
	logins[login][month_aligned_when].logins = cur_set.union(logins[login][month_aligned_when].logins)

lib.read_file(sys.argv[1], lib.empty_header, read_lcmt_level2_body)

# step 2) read login general experience
# dictionary login -> [list of <exp,when> tuples]
login_exp = {}
def read_body(header, raw, curline):
	who = raw[header['who']]
	exps = raw[header['exp']].split(lib.tsep)
	explist = []
	for str_exp in exps:
		if str_exp == '':
			break
		raw_exp = str_exp.split(lib.fsep)
		newpack = lib.infopack()
		newpack.data = int(raw_exp[0])
		newpack.when = int(raw_exp[1])
		explist.append(newpack)
	login_exp[who] = explist
lib.read_file(sys.argv[2], lib.empty_header, read_body)

# step 3) for each login, scan by time
# header
print 'login' + lib.sep + 'contacter_num' + lib.sep + 'max_contecter_exp'
for login in logins:
	out_count = ''
	out_exp = ''
	out_role = ''
	# set of peers it gets by far
	cur_set = set()
	cur_size = 0
	dates = sorted(logins[login].keys())
	max_exp = 0
	sign = False

	for date in dates:
		# it met new peers
		cur_set = cur_set.union(logins[login][date].logins)
		cur_max_exp = 0
		
		# for each peer, find max experience
		for contactor in logins[login][date].logins:
			if login == contactor:
				# do not calculate itself
				continue
			if login_exp.has_key(contactor):
				index = lib.binary_search(login_exp[contactor], lib.func_time, date)
				if index >= 0:
					cur_exp = login_exp[contactor][index].data
					if cur_exp > cur_max_exp:
						cur_max_exp = cur_exp
		# check whether the max experince has been updated
		if cur_max_exp > max_exp:
			max_exp = cur_max_exp
			out_exp += str(max_exp) + lib.fsep + str(date) + lib.tsep
				
		if login in cur_set:
			# remove it self
			cur_set.remove(login)
		# check whether contact new people
		if cur_set.__len__() != cur_size:
			cur_size = cur_set.__len__()
			out_count += str(cur_size) + lib.fsep + str(date) + lib.tsep
	# finish scan a login, output
	out = login + lib.sep
	if out_count.__len__() > 0:
		out += out_count[:-lib.tsep.__len__()]
	out += lib.sep
	if out_exp.__len__() > 0:
		out += out_exp[:-lib.tsep.__len__()]
	if out_count.__len__() > 0 or out_exp.__len__() > 0 or out_role.__len__() > 0:
		print out
