#!/usr/bin/env python
import re
from math import sqrt
from random import randint
import matplotlib.pyplot as plt
import sys

import numpy as np
from random import uniform, randrange
from math import cos, sin, pi, sqrt, radians, degrees

from actions import *

def read_lines(fname): #saves in a list the lines of the .hoc file

	hoc_lines=[]
	for line in open(fname):
		hoc_lines.append(line.rstrip('\n'))

	del_index=[]
	i=0
	while i<len(hoc_lines):
		regex1=re.search('\/\*', hoc_lines[i])
		if regex1:
			del_index.append(i)
			i+=1
			regex2=re.search('\*\/', hoc_lines[i])
			while bool(regex2)==False:
				del_index.append(i)
				i+=1
				regex2=re.search('\*\/', hoc_lines[i])
			del_index.append(i)
		i+=1
	k=0
	for item in del_index:
		del(hoc_lines[item-k])
		k+=1

	hoc_lines=hoc_lines[:]

	return hoc_lines

def read_con(hoc_lines): #saves the connectivity lines as it's defined in the initial .hoc file
	i,k=0,0
	connex=[]
	for line in hoc_lines:
 		if re.search(r'axon', line):
			pass
		else:
			if re.search(r'connect', line) and k==0:
				start_con=i
			if re.search(r'connect', line):
				connex.append(line)
				k=1
			if re.search(r'\}', line) and k==1:
				end_con=i
				break
			i+=1

	return connex, start_con, end_con

def connectivity(connex): #parses the connectivity
	parsed_con=[]
	for line in connex:
		line = re.sub(r'(\w+)(\(\d\))', r'\1[0]\2', line.rstrip())
		line=line.lstrip()

		if re.search(r'for i = (\d+), (\d+) connect (\w+)\[i\]\((\d)\), (\w+)\[i-1\]\((\d)\)', line):
			con=re.search(r'for i = (\d+), (\d+) connect (\w+)\[i\]\((\d)\), (\w+)\[i-1\]\((\d)\)', line)
			i_start=int(con.group(1))
			i_end=int(con.group(2))
			seg_a=str(con.group(3))
			pol_a=int(con.group(4))
			seg_b=str(con.group(5))
			pol_b=int(con.group(6))

			for i in range(i_start,i_end+1):
				string = 'connect %s[%d](%d), %s[%d](%d)'%(seg_a, i, pol_a ,seg_b, i-1, pol_b)
				parsed_con.append(string)


		elif re.search(r'for i = (\d+), (\d+) connect (\w+)\[i\]\((\d)\), (\w+)\[(\d+)\]\((\d)\)', line):
			con=re.search(r'for i = (\d+), (\d+) connect (\w+)\[i\]\((\d)\), (\w+)\[(\d+)\]\((\d)\)', line)
			i_start=int(con.group(1))
			i_end=int(con.group(2))
			seg_a=str(con.group(3))
			pol_a=int(con.group(4))
			seg_b=str(con.group(5))
			id_b=int(con.group(6))
			pol_b=int(con.group(7))

			for i in range(i_start,i_end+1):
				string = 'connect %s[%d](%d), %s[%d](%d)'%(seg_a, i, pol_a ,seg_b, id_b, pol_b)
				parsed_con.append(string)
		else:
			parsed_con.append(line)

	return parsed_con

def dendrites_list(parsed_con): #returns a list of all dendrites

	list_a=[]
	list_b=[]
	connected=[]
	for i in parsed_con: 
		words=i.split()
		word_a=re.sub(r'\(\d\),', r'', words[1].rstrip())
		word_b=re.sub(r'\(\d\)', r'', words[2].rstrip())
		list_a.append(word_a)
		list_b.append(word_b)
		connected.append(str(word_a)+str(word_b))

	dlist=list_a[:]
	for i in list_b:
		if i in dlist:
			pass
		else:
			dlist.insert(0,i)

	basal=[]
	apical=[]

	for dend in dlist:
		if re.search('dend', dend):
			basal.append(dend)
		if re.search('apic', dend):
			apical.append(dend)

	return dlist, list_a, list_b, connected, basal, apical

def pathway(list_a, list_b): #returns the pathway to root of all dendrites
	paths={}
	for a in list_a:
		word=a
		path=[]
		path.append(word)
		k=len(list_a)-1
		while k>-1:
			if list_a[k] == word:
				path.append(list_b[k])
				word=list_b[k]
			else:
				k=k-1
		paths[a]=str(' '.join(path))
	return paths

def terminal(dlist, paths, basal, apical): #returns a list of the terminal dendrites

	all_terminal=[]
	for dendrite in dlist:

		regex=re.search('soma', dendrite)

		if regex:
			pass

		else:
			value=0
			for i in paths:
				words=paths[i].split()
				for k in range(len(words)):
					if dendrite==words[k]:
						if k>value:
							value=k
			if value==0:
				all_terminal.append(dendrite)

	basal_terminal=[]
	basal_terminal = [x for x in all_terminal if x in basal]

	apical_terminal=[]
	apical_terminal = [x for x in all_terminal if x in apical]

	return all_terminal, basal_terminal, apical_terminal

def siblings(dlist, all_terminal, list_a, list_b): #returns a list of lists of dendrites that share common root
	sister_branches=[]
	for dendrite in dlist:
		if dendrite not in all_terminal:
			sibling=[]
			for k in range(len(list_b)):
				if list_b[k]==dendrite:
					sibling.append(list_a[k])
			sister_branches.append(sibling)
	return sister_branches

def cp_dlist(dlist): #returns a list of dendrites to work with

	xlist=dlist[:]
	#for i in range(len(xlist)):
	#	xlist[i] = re.sub(r'\[0\]', r'', xlist[i].rstrip())
	return xlist

def dend_be(hoc_lines, dlist): #returns the index of the lines of beggining and ending of every dendrite on the .hoc file
	
	xlist=cp_dlist(dlist)
	dbe=dict()
	for i in range(len(hoc_lines)):
		if re.search(r'pt3dclear', hoc_lines[i]):
			for dend in xlist:
				xdend=re.sub('\[0\]', '', dend)
				if re.search(r'%s' % re.escape(xdend), hoc_lines[i]):
					be=[]
					be.append(i+1)
					i+=1
					while bool(re.search(r'pt3dclear', hoc_lines[i])) == False:
						if (re.search(r'pt3dadd', hoc_lines[i])):
							last=i							
							pass
						i+=1
						if re.search(r'objref', hoc_lines[i]):
							break
					be.append(last)
					xlist.remove(dend)
					dbe[dend]=be
					break
	return dbe

def distance(x1,x2,y1,y2,z1,z2): #returns the euclidean distance between two 3d points

	dist = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
	return dist

def dend_length(hoc_lines, dlist, dbe): #returns a list of dendrites' lengths

	#xlist=cp_dlist(dlist)
	dist=dict()
	for dend in dlist:
		dist_sum=[]
		b=dbe[dend][0]
		e=dbe[dend][1]+1
		for i in range(b,e):
			if re.search(r'pt3dadd\((.*?),(.*?),(.*?),', hoc_lines[i]):
				regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', hoc_lines[i])
				if i != b:
					xp=x
					yp=y
					zp=z 
				
				x=float(regex.group(1))
				y=float(regex.group(2))
				z=float(regex.group(3))

				if i != b:
					dist_sum.append(distance(x,xp,y,yp,z,zp))
		sum_dist=sum(dist_sum)
		dist[dend]=sum_dist

	return dist

def read_file(fname):

	hoc_lines=read_lines(fname)
	(connex, start_con, end_con)=read_con(hoc_lines)
	parsed_con=connectivity(connex)
	(dlist, list_a, list_b, connected, basal, apical)=dendrites_list(parsed_con)
	b_max=basal_max(basal)
	a_max=apical_max(apical)
	paths=pathway(list_a, list_b)
	all_terminal, basal_terminal, apical_terminal=terminal(dlist, paths, basal, apical)
	sister_branches=siblings(dlist, all_terminal, list_a, list_b)
	dbe=dend_be(hoc_lines, dlist)
	dist=dend_length(hoc_lines, dlist, dbe)

	f = open('con_morph.txt', 'w')
	
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
	print >>f, 'Connectivity list:\n'
	for con in parsed_con:
		print >>f, con
	print >>f

	print >>f, '----------------------------------------\n'
	print >>f, 'List of dendritic lengths:\n'
	for dend in dlist:
		print >>f, str(dend) + ' = ' + str(dist[dend])
	print >>f

	f.close()

	return hoc_lines, connex, start_con, end_con, parsed_con, dlist, list_a, list_b, connected, basal, apical, b_max, a_max, paths, all_terminal, basal_terminal, apical_terminal, siblings, dbe, dist
