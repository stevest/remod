from extract_swc_morphology import *
from take_action_swc import *
from warn import *
from graph import *
import sys

if (len(sys.argv)==3):
	path=str(sys.argv[1])
	fname=sys.argv[2]
else:
	sys.exit(0)

print path
print fname

(swc_lines, points, comment_lines, parents, bpoints, soma_index, max_index, dlist, dend_points, dend_names, exceptions, basal, apical, dend_add3d, path, all_terminal, basal_terminal, apical_terminal, dist)=read_file(fname) #extracts important connectivity and morphological data

choices=[]
for line in open('choices_swc.txt'):
	line.rstrip('\n')
	choices.append(line)

regex_who=re.search('(.*)', choices[0])

who=regex_who.group(1)
if who=='all_terminal':
	who=all_terminal
if who=='apical_terminal':
	who=apical_terminal
if who=='basal_terminal':
	who=basal_terminal
if who=='random_all':
	who=random_all
if who=='random_apical':
	who=random_apical
if who=='random_basal':
	who=random_basal
if who=='manual':
	who=apical_terminal

regex_action=re.search('(.*)', choices[1])
action=regex_action.group(1)

regex_hm_choice=re.search('(.*)', choices[2])
hm_choice=regex_hm_choice.group(1)

regex_amount=re.search('(.*)', choices[3])
amount=int(regex_amount.group(1))

#print who, action, amount, hm_choice

#check_terminal(who, all_terminal) #checks if selected dendrites are terminal

newfile=execute_action(who, action, amount, hm_choice, dend_add3d, dist, max_index) #executes the selected action and print the modified tree to a '*_new.hoc' file
newfile=comment_lines + newfile

for i in newfile:
	print i

#graph(hoc_lines, newfile, action) #plots the original and modified tree (overlaying one another)'''
