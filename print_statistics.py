def statistics(dlist, all_terminal, basal_terminal, apical_terminal, dist):

	f = open('statistics.txt', 'w')

	print >>f, '----------------------------------------\n'
	print >>f, 'List of all dendrites:\n'
	for dend in dlist:
		print >>f, dend
	print >>f

	print >>f, '----------------------------------------\n'
	print >>f, 'List of terminal dendrites:\n'
	for dend in all_terminal:
		print >>f, dend
	print >>f

	print >>f, '----------------------------------------\n'
	print >>f, 'List of basal terminal dendrites:\n'
	for dend in basal_terminal:
		print >>f, dend
	print >>f

	print >>f, '----------------------------------------\n'
	print >>f, 'List of apical terminal dendrites:\n'
	for dend in apical_terminal:
		print >>f, dend
	print >>f

	print >>f, '----------------------------------------\n'
	print >>f, 'List of dendritic lengths:\n'
	for dend in dlist:
		print >>f, str(dend) + ' = ' + str(dist[dend])
	print >>f

	f.close()
