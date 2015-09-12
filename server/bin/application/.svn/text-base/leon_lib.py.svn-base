# lib for preprocessing

# define global variables
sep = ';'
tsep = ']~>['
fsep = '|-|'
ffsep = '::'

# genral use info pack
class infopack:
	def __init__(self):
		self.data = 0
		self.when = 0
def func_time(pack):
	return pack.when

# align a date(long) to month-aligned
def month_align(when):
	import math
	return int(math.floor(when/3600/24/12) * 12*24*3600)

# infos may be any list, func_time return time(int) from an element of infos
def binary_search(infos, func_time, aim_time):
	left = 0
	right = infos.__len__()
	
	if right == 0:
		return -1
	if aim_time < func_time(infos[0]):
		return -1

	while left + 1 < right:
		mid = (left + right)/2
		mid_value = func_time(infos[mid])
		if mid_value < aim_time:
			left = mid
		elif mid_value > aim_time:
			right = mid
		else:
			return mid
	return left

# framework of read a file
def read_file(filename, run_header, run_body):
	header = {}
	first = True
	file = open(filename, 'r')
	for curline in file:
		raw = curline[:-1].split(sep)
		if first:
			for title in raw:
				header[title] = header.__len__()
			first = False
			# run header function
			run_header(header, raw, curline)
			continue
		# body
		res = run_body(header, raw, curline)
		if res == -1:
			break
	file.close()
	
# empty function
def empty_header(header, raw, curline):
	pass

def insert_infopack(dict, login, data, when):
	if not dict.has_key(login):
		dict[login] = []
	newpack = infopack()
	newpack.data = data
	newpack.when = when
	dict[login].append(newpack)

# specified tools

# new read product convertion
class product_convertion:
	def __init__(self):
		self.fork_set = {}
		self.rename_list = {}

	def read_product_convertion(self, file):
		self.fork_set = {}
		self.rename_list = {}
		# open file
		file = open(file, 'r')
		first = True
		header = {}
		for curline in file:
			raw = curline[:-1].split(sep)
			# read header
			if first:
				for title in raw:
					header[title] = header.__len__()
				first = False
				continue
			# read body
			product = raw[header['product']].lower()
			convert_to = raw[header['convert_to']].lower()
			type = raw[header['type']].lower()
			if type == 'rename':
				self.rename_list[product] = convert_to
			elif type == 'fork':
				if not self.fork_set.has_key(product):
					self.fork_set[product] = set()
				self.fork_set[product].add(convert_to)
		file.close()
	
	def is_correct(self, a_from, b_to):
		# do not check for itself
		# check fork
		a = a_from.lower()
		b = b_to.lower()
		if self.fork_set.has_key(a):
			if b in self.fork_set[a]:
				return True
		# check rename
		if self.rename_list.has_key(a) and b == self.rename_list[a]:
			return True
		return False

	def rename(self, product):
		a = product.lower()
		if self.rename_list.has_key(a):
			return self.rename_list[a]
		return a


# bug_resolved time checker
class resolved_time_checker:
	def __init__(self):
		self.bug_resolved_time = {}

	def read(self, leon_level3):
		self.bug_resolved_time = {}
		first = True
		header = {}
		file = open(leon_level3, 'r')
		for curline in file:
			raw = curline[:-1].split(sep)
			if first:
				for title in raw:
					header[title] = header.__len__()
				first = False
				continue
			# body
			bug_id = raw[header['bug_id']]
			statuses = raw[header['status']].split(tsep)
			statuses.reverse()
			for status in statuses:
				raw_status = status.split(fsep)
				name = raw_status[0]
				if name == 'RESOLVED':
					when = int(raw_status[1])
					self.bug_resolved_time[bug_id] = when
					break
		file.close()
	def get_resolved_time(self, bug_id):
		if not self.bug_resolved_time.has_key(bug_id):
			return -1
		else:
			return self.bug_resolved_time[bug_id]
