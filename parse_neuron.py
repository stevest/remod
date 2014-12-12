from extract_hoc_morphology import *
from take_action import *
from warn import *
from  neuron_before import *
from  print_statistics import *
from statistics import *
import sys

if (len(sys.argv)==3):
	path=str(sys.argv[1])
	fname=sys.argv[2]
else:
	sys.exit(0)

print path

(hoc_lines, connex, start_con, end_con, parsed_con, dlist, list_a, list_b, connected, basal, apical, b_max, a_max, paths, all_terminal, basal_terminal, apical_terminal, siblings, dbe, dist)=read_file(fname) #extracts important connectivity and morphological data - you can check these data at 'con_morph.txt' file

fdendlist=str(path)+str('dendritic_list.txt')

f = open('%s' % fdendlist, 'wb')
for dend in dlist:
	print >>f, dend
f.close()

f = open('dendritic_lengths.txt', 'w')
for dend in dlist:
	print >>f, str(dend) + ' ' + str(dist[dend])
f.close()

f = open('number_of_dendrites.txt', 'w')
print >>f, 'basal' + ' ' + str(len(basal)) + ' ' + str(len(basal_terminal))
print >>f, 'apical' + ' ' + str(len(apical)) + ' ' + str(len(apical_terminal))
f.close()

bo=branch_order(dlist, paths)
bo_freq=bo_frequency(dlist, bo)
f = open('branch_order_frequency.txt', 'w')
for order in bo_freq:
	print >>f, str(order) + ' ' + str(bo_freq[order])
f.close()

bo_dlen=bo_dlength(dlist, bo, dist)
f = open('bo_average_dlength.txt', 'w')
for order in bo_dlen:
	print >>f, str(order) + ' ' + str(bo_dlen[order])
f.close()

plength=path_length(dlist, paths, dist)
bo_plen=bo_plength(dlist, bo, plength)
f = open('bo_average_plength.txt', 'w')
for order in bo_dlen:
	print >>f, str(order) + ' ' + str(bo_plen[order])
f.close()

#print bo_len

graph(fname)

#statistics(dlist, all_terminal, basal_terminal, apical_terminal, dist)
