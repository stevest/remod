from extract_hoc_morphology import *
from take_action import *
from warn import *
from graph import *
import sys

if (len(sys.argv)==2):
	fname=sys.argv[1]
else:
	sys.exit(0)

(hoc_lines, connex, start_con, end_con, parsed_con, dlist, list_a, list_b, connected, basal, apical, b_max, a_max, paths, all_terminal, basal_terminal, apical_terminal, siblings, dbe, dist)=read_file(fname) #extracts important connectivity and morphological data - you can check these data at 'con_morph.txt' file

choices=[]
for line in open('choices.txt'):
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

print who, action, amount, hm_choice

check_terminal(who, all_terminal) #checks if selected dendrites are terminal

newfile=execute_action(who, action, amount, hm_choice, dist, dbe, start_con, end_con, parsed_con, hoc_lines, b_max, a_max, basal, apical, fname) #executes the selected action and print the modified tree to a '*_new.hoc' file

graph(hoc_lines, newfile, action) #plots the original and modified tree (overlaying one another)
