import re
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from math import cos, sin, pi, sqrt, radians, degrees

fname="c11563.CNG.swc" #file name

def swc_line(fname):

	swc_lines=[]
	for line in open(fname):
		swc_lines.append(line.rstrip('\n'))

	return swc_lines

def point(swc_lines):

	points={}

	point_lines=[]

	for line in swc_lines:
	
		comment=re.search(r'#', line)
		p=re.search(r'(\d+) (\d+) (.*?) (.*?) (.*?) (.*?) (-?\d+)', line)

		if comment:
			continue

		elif p:

			i=int(p.group(1))
			l=int(p.group(2))
			x=float(p.group(3))
			y=float(p.group(4))
			z=float(p.group(5))
			d=float(p.group(6))
			c=int(p.group(7))

			mylist=[i, l, x, y, z, d, c]
			points[i]=mylist
			point_lines.append(line)

	return points, point_lines

def comments(swc_lines, point_lines):

	comment_lines=[]

	for line in swc_lines:
		if line not in point_lines:
			comment_lines.append(line)

	return comment_lines

def index(points):

	mylist=[]
	for i in points:
		mylist.append(points[i][0])
	max_index=max(mylist)
	return max_index		

def branching_points(points):

	bpoints={}
	parents=[]

	for i in points:
		c=points[i][0]
		children=[]
		count=0
		for k in points:
			if points[k][6]==c:
				children.append(k)
				count+=1
		if count>1:
			if c not in parents:
				parents.append(c)
				bpoints[c]=children

	m=len(points)
	c=points[m][0]
	while c>0:
		for k in points:
			if c==points[k][0]:
				c=points[k][6]
				break
	soma_index=k
	return parents, bpoints, soma_index

def d_list(parents, bpoints, soma_index):

	dlist=[]
	dlist.append(soma_index)
	for n in parents:
		for k in bpoints[n]:
			dlist.append(k)

	return dlist

def dend_point(parents, bpoints, dlist, points):

	dend_points={}

	for i in dlist:
		next=i
		dendrite=[]
		dendrite.append(i)
		for k in points:
			if k>1:
				if next==points[k][6]:
					next=points[k][0]
					dendrite.append(next)
			if next in parents and next>i:
				break
		dend_points[i]=dendrite

	return dend_points

def dend_name(dlist, points):

	exceptions=[]
	dend_names={}

	basal=[]
	apical=[]

	undef_index=0
	soma_index=0
	axon_index=0
	basal_index=0
	apic_index=0

	for i in dlist:
		if points[i][1]==0:
			dend_names[i]='undef' + '[' + str(undef_index) + ']'
			undef_index+=1
		elif points[i][1]==1:
			dend_names[i]='soma' + '[' + str(soma_index) + ']'
			soma_index+=1
		elif points[i][1]==2:
			dend_names[i]='axon' + '[' + str(axon_index) + ']'
			axon_index+=1
		elif points[i][1]==3:
			dend_names[i]='dend' + '[' + str(basal_index) + ']'
			basal.append(i)
			basal_index+=1
		elif points[i][1]==4:
			dend_names[i]='apic' + '[' + str(apic_index) + ']'
			apical.append(i)
			apic_index+=1
		else:	
			exceptions.append(i)

	return dend_names, exceptions, basal, apical

def dend_add3d_points(dlist, dend_points, points):

	dend_add3d={}

	for i in dlist:
		pts=[]
		for k in dend_points[i]:
			mylist=[points[k][0], points[k][1], points[k][2], points[k][3], points[k][4], points[k][5], points[k][6]]
			pts.append(mylist)
		dend_add3d[i]=pts
	return dend_add3d

def pathways(dlist, points): #returns the pathway to root of all dendrites

	path={}

	for i in dlist:
		word=i
		pathway=[]
		pathway.append(word)
		k=len(points)
		while k>0:
			if points[k][0] == word:
				word=points[k][6]
				if word!=-1:
					pathway.append(word)
			else:
				pass
			k=k-1
		path[i]=pathway
	return path

def terminal(dlist, path, basal, apical): #returns a list of the terminal dendrites

	all_terminal=[]
	for i in dlist:
		if i!=1:
			value=0
			for n in dlist:
				for k in path[n]:
					if i==k:
						value+=1
			if value==1:
				all_terminal.append(i)

	basal_terminal=[]
	basal_terminal = [x for x in all_terminal if x in basal]

	apical_terminal=[]
	apical_terminal = [x for x in all_terminal if x in apical]

	return all_terminal, basal_terminal, apical_terminal

def distance(x1,x2,y1,y2,z1,z2): #returns the euclidean distance between two 3d points

	dist = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
	return dist

def dend_length(dend_add3d, dlist): #returns a list of dendrites' lengths

	dist={}
	for i in dlist:
		dist_sum=[]
		for k in range(len(dend_add3d[i])-1):
			current=dend_add3d[i][k]
			next=dend_add3d[i][k+1]
			dist_sum.append(distance(next[0], current[0], next[1],current[1], next[2],current[2]))
		sum_dist=sum(dist_sum)
		dist[i]=sum_dist

	return dist

def read_file(fname):

	swc_lines=swc_line(fname)
	points, point_lines=point(swc_lines)
	comment_lines=comments(swc_lines, point_lines)
	parents,bpoints,soma_index=branching_points(points)
	dlist=d_list(parents, bpoints, soma_index)
	dend_points=dend_point(parents, bpoints, dlist, points)
	dend_names, exceptions, basal, apical=dend_name(dlist, points)
	dend_add3d=dend_add3d_points(dlist, dend_points, points)
	path=pathways(dlist, points)
	all_terminal, basal_terminal, apical_terminal=terminal(dlist, path, basal, apical)
	dist=dend_length(dend_add3d, dlist)
	max_index=index(points)

	return (swc_lines, points, comment_lines, parents, bpoints, soma_index, max_index, dlist, dend_points, dend_names, exceptions, basal, apical, dend_add3d, path, all_terminal, basal_terminal, apical_terminal, dist)



#points, parents, bpoints, soma_index, dend_points, dend_names, exceptions, dend_add3d, path

#hoc_lines - swc_lines
#dlist - dlist
#basal - basal
#apical - apical
#all_terminal - all_terminal
#basal_terminal - basal_terminal
#apical_terminal - apical_terminal
#dist - dist
#paths - path


'''for i in index:
	if point[i][5]!=-1:
		c=point[i][5]
		x=[ point[i][0], point[c][0] ]
		y=[ point[i][1], point[c][1] ]
		z=[ point[i][2], point[c][2] ]
		d=point[i][3]
		parameters=[x, y, z, d]
		plot_neuron.append(parameters)

fig = plt.figure()
ax = fig.gca(projection='3d')

l=[0,1]
k=0

for i in plot_neuron:
	if k in l:
		pass
	else:
		ax.plot(i[0], i[1], i[2], linewidth=i[3], c='b', alpha=1)
	k+=1

ax.tick_params(labelsize=6)
plt.show()'''

#hoc_lines
#3d_points
