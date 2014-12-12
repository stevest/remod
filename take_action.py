from actions import *
from print_file import *

def execute_action(who, action, amount, hm_choice, dist, dbe, start_con, end_con, parsed_con, hoc_lines, b_max, a_max, basal, apical, fname):

	if action == 'shrink':
		newfile=shrink(who, amount, hm_choice, dist, dbe, start_con, end_con, parsed_con, hoc_lines)
	if action == 'remove':
		newfile=remove(who, dbe, start_con, end_con, parsed_con, hoc_lines)
	if action == 'extend':
		newfile=extend(who, amount, hm_choice, dist, dbe, hoc_lines)
	if action == 'branch':
		newfile=branch(who, b_max, a_max, basal, apical, hm_choice, amount, dist, dbe, hoc_lines, end_con)

	print_newfile(fname, newfile) #prints the lines of the modified tree to a '*_new.hoc' file

	return newfile

