from actions_swc import *
from print_file import *

def execute_action(who, action, amount, hm_choice, dend_add3d, dist, max_index):

	if action == 'shrink':
		newfile=shrink(who, action, amount, hm_choice, dend_add3d, dist)

	if action == 'remove':
		newfile=remove(who, action, dend_add3d)

	if action == 'extend':
		newfile=extend(who, action, amount, hm_choice, dend_add3d, dist, max_index)

	if action == 'branch':
		newfile=branch(who, action, amount, hm_choice, dend_add3d, dist, max_index)

	return newfile

	'''print_newfile(fname, newfile) #prints the lines of the modified tree to a '*_new.hoc' file'''
