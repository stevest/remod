def check_terminal(who, all_terminal):

	not_terminal=[]

	for dend in who:
		if dend not in all_terminal:
			not_terminal.append(dend)

	if len(not_terminal)>0:
		print '\nYou have to remove the following non-terminal dendrites from the modification list:\n'
		for dend in not_terminal:
			print '> ' + str(dend)
		print '\nProgram stopped\n'
		exit(1)
