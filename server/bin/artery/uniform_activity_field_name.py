#!/usr/bin/python

# Author: Xie Jialiang
# Date: 2013-05-02
# Function: Uniform field name into standard
# Parameters: 1) activity level2
# Output stream: uniformed activity level2

import sys
import leon_lib as lib

# setting the dictionary of uniform
uniform_dic = {'assigned_to':'Assignee',
		'cc':'CC',
		'component':'Component',
		'op_sys':'OS',
		'priority':'Priority',
		'product':'Product',
		'resolution':'Resolution',
		'bug_severity':'Severity',
		'bug_status':'Status',
		'target_milestone':'Target Milestone',
		'version':'Version',
		'blocked':'Blocks',
		'dependson':'Depends on',
		'hardware':'Hardware',
		'flag':'Flags',
		'target_milestone':'Target Milestone'}



def read_head(header, raw, curline):
	print curline[:-1]

def read_body(header, raw, curline):
	bug_id = raw[header['bug_id']]
	who = raw[header['who']]
	when = raw[header['when']]
	what = raw[header['what']]
	old = raw[header['old']]
	new = raw[header['new']]

	if uniform_dic.has_key(what):
		what = uniform_dic[what]
	print bug_id + ';;' + who + ';' + when + ';' + what + ';' + old + ';' + new

lib.read_file(sys.argv[1], read_head, read_body)




