#/bin/python

# script for get information at anytime from [report_time, +infinit)
# input

fsep = '|-|'
tsep = ']~>['

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

def find_info_within_time_range(infos, func_time, begin, end):
	left = binary_search(infos, func_time, begin)
	if func_time(infos[left]) < begin:
		if infos.__len__() > left + 1:
			left += 1
		else:
			return [-1, -1]
	right = binary_search(infos[left:], func_time, end)
	if right == -1:
		return [-1,-1]
	else:
		return [left, right + 1]

class act_pack:
	def __init__(self):
		self.value = ''
		self.login = ''
		self.when = 0

def build_act_packs(str_acts):
	raw = str_acts.split(tsep)
	actpacks = []
	for act in raw:
		act_raw = act.split(fsep)
		actpack = act_pack()
		actpack.value = act_raw[0]
		actpack.login = act_raw[2]
		actpack.when = int(act_raw[1])
		actpacks.append(actpack)
	return actpacks
