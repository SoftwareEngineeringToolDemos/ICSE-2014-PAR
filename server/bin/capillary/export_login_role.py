#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2012-10-15
# Function: combine and generate role file
# Parameters: 1) developer namelist
#	      2) non-self-triager list
#	      3) (maintainer)bugmaster namelist
#	      4) activity_level2
#	      5) use 0-email or 1-login only
# Strategy: 
#  maintainer | developer | non-self-triager | role
#       0     |     0     |        0         | reporter
#	0     |     0     |        1         | triager
#       0     |     1     |        *         | developer
#       1     |     *     |        *         | maintainer

import sys
import leon_lib as lib

INFINIT = 999999999999

class actor:
	def __init__(self):
		self.dev_since = INFINIT
		self.nonself_since = INFINIT
		self.is_maint = False

actors = {}
alias = {}
use_email = (sys.argv[5] == '0')

# read reporter(self_triager) namelist
def read_reporter_body(header, raw, curline):
	global actors
	global alias
	global use_email
	who = raw[header['who']]
	when = int(raw[header['when']])

	if use_email:
		name = who.split('@')[0]
		if not alias.has_key(name):
			alias[name] = {}
		alias[name][who] = 1

	if not actors.has_key(who):
		actors[who] = actor()
	actors[who].nonself_since = when

lib.read_file(sys.argv[2], lib.empty_header, read_reporter_body)

# read maintainer namelist
def read_maint_body(header, raw, curline):
	global actors
	global alias
	global use_email
	who = raw[header['who']]

	if use_email:
		name = who.split('@')[0]
		if not alias.has_key(name):
			alias[name] = {}
		alias[name][who] = 1

	if not actors.has_key(who):
		actors[who] = actor()
	actors[who].is_maint = True
lib.read_file(sys.argv[3], lib.empty_header, read_maint_body)

# triage actor
def read_actor_body(header, raw, curline):
	global actors
	global use_email

	login = raw[header['who']]
	if use_email:
		name = login.split('@')[0]
		if not alias.has_key(name):
			alias[name] = {}
		alias[name][login] = 1

	if not actors.has_key(login):
		actors[login] = actor()
lib.read_file(sys.argv[4], lib.empty_header, read_actor_body)

# developer namelist
def read_dev_body(header, raw, curline):
	global actors
	global use_email

	name = raw[header['who']]
	raw_time = int(raw[header['when']])

	if use_email:
		if alias.has_key(name):
			for login in alias[name]:
				actors[login].dev_since = raw_time
	else:
		if actors.has_key(name):
			actors[name].dev_since = raw_time
lib.read_file(sys.argv[1], lib.empty_header, read_dev_body)

# conclusion
print 'who' + lib.sep + 'role'
for login in actors:
	actor = actors[login]
	conclusion = login

	if actor.is_maint == True:
		conclusion += lib.sep + 'maint' + lib.fsep + '0'
	else:
		# assume she was reporter at the very beginning
		conclusion += lib.sep + 'self' + lib.fsep + '0'
		if actor.nonself_since < actor.dev_since:
			conclusion += lib.tsep + 'triager' + lib.fsep + str(actor.nonself_since)
		if actor.dev_since < INFINIT:
			conclusion += lib.tsep + 'dev' + lib.fsep + str(actor.dev_since)
	print conclusion
