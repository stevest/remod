def print_newfile(fname, newfile):

	new_name=fname.replace('.hoc','') + '_new.hoc'

	f = open(new_name, 'w')
	print >>f, ('\n').join(newfile)
	f.close()
