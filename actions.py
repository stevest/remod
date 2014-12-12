import re
from math import sqrt
from random import randint
import sys

import numpy as np
from random import uniform, randrange
from math import cos, sin, pi, sqrt, radians, degrees

def length_distribution(): #parses the length distribution

	length=[]
	frequency=[]
	for line in open('length_distribution.txt'):
		line=line.rstrip('\n')
		if re.search(r'(\S+)\s-\s(\S+)', line):
			regex=re.search(r'(\S+)\s-\s(\S+)', line)
			length.append(float(regex.group(1)))
			frequency.append(float(regex.group(2)))

	l_length=[]
	l_length.append(0)
	limit_length=0
	for i in range(len(length)):
		l_length.append(int(frequency[i]*1000000+limit_length))
		limit_length=l_length[i]
	return length, l_length

def length_selection(l_length): #returns a randomly chosen length value based on the distribution

	random=randint(0, l_length[-1]);

	for i in range(len(l_length)):
		if random>l_length[i] and random<l_length[i+1]:
			return length[i]
			break

def distance(x1,x2,y1,y2,z1,z2): #returns the euclidean distance between two 3d points

	dist = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
	return dist

def round_to(x, rounder): #returns the nearest number to the multiplied "rounder"

	return round(x/rounder)*rounder

def createP(length, angle, p1, p2, flag): #returns new pt3dadd lines formatted in the typical NEURON way

	r=radians(angle)

	p1=np.matrix([float(p1[0]), float(p1[1]), float(p1[2])])
	p2=np.matrix([float(p2[0]), float(p2[1]), float(p2[2])])

	axis=p2-p1

	axis = axis / np.linalg.norm(axis) # monadiaio vector me tin idia kateuthinsi kai arxi tin arxi ton axonwn

	tmp = np.cross(axis,[0,0,1])
	tmp = tmp/np.linalg.norm(tmp)

	xt = tmp[0,0]
	yt = tmp[0,1]
	zt = tmp[0,2]

	r1 = np.matrix([[cos(r)+(xt**2)*(1-cos(r)), xt*yt*(1-cos(r))-zt*sin(r), xt*zt*(1-cos(r))+yt*sin(r)],
		[yt*xt*(1-cos(r))+zt*sin(r) , cos(r) + (yt**2)*(1-cos(r)), yt*zt*(1-cos(r))-xt*sin(r)],
		[zt*xt*(1-cos(r))-yt*sin(r), zt*yt*(1-cos(r))+xt*sin(r), cos(r)+(zt**2)*(1-cos(r))]], float)

	xa = axis[0,0]
	ya = axis[0,1]
	za = axis[0,2]

	r=randrange(360) 
	r=radians(r) # /!\ in rads /!\

	r2 = np.matrix([[cos(r)+(xa**2)*(1-cos(r)), xa*ya*(1-cos(r))-za*sin(r), xa*za*(1-cos(r))+ya*sin(r)],
		[ya*xa*(1-cos(r))+za*sin(r) , cos(r) + (ya**2)*(1-cos(r)), ya*za*(1-cos(r))-xa*sin(r)],
		[za*xa*(1-cos(r))-ya*sin(r), za*ya*(1-cos(r))+xa*sin(r), cos(r)+(za**2)*(1-cos(r))]], float)

	factor =  (axis.T * length)

	f1 = r1 * factor
	f2 = r2 * f1
	f2 = f2.T
	v1 = f2 + p2

	np1='\tpt3dadd(%.2f, %.2f, %.2f, 0.5)' % (v1[0,0], v1[0,1], v1[0,2])

	np_=[]
	np_.append(np1)

	if flag==2:
		r = r + 3.1415
		r2_ = np.matrix([[cos(r)+(xa**2)*(1-cos(r)), xa*ya*(1-cos(r))-za*sin(r), xa*za*(1-cos(r))+ya*sin(r)],
			[ya*xa*(1-cos(r))+za*sin(r) , cos(r) + (ya**2)*(1-cos(r)), ya*za*(1-cos(r))-xa*sin(r)],
			[za*xa*(1-cos(r))-ya*sin(r), za*ya*(1-cos(r))+xa*sin(r), cos(r)+(za**2)*(1-cos(r))]], float)
		f3 = r2_ * f1
		f3 = f3.T
		v2 = f3 + p2

		new_point=[]
		new_point.append(v2[0,0])
		new_point.append(v2[0,1])
		new_point.append(v2[0,2])

		np2='\tpt3dadd(%.2f, %.2f, %.2f, 0.5)' % (v2[0,0], v2[0,1], v2[0,2])

		np_.append(np2)

	return np_

def add_point(point1, point2, flag): #returns 1 or 2 new points 

	p1=[]
	if re.search(r'pt3dadd\((.*?),(.*?),(.*?),', point1):
		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', point1)

		p1.append(float(regex.group(1)))
		p1.append(float(regex.group(2)))
		p1.append(float(regex.group(3)))

	p2=[]
	if re.search(r'pt3dadd\((.*?),(.*?),(.*?),', point2):
		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', point2)
	
		p2.append(float(regex.group(1)))
		p2.append(float(regex.group(2)))
		p2.append(float(regex.group(3)))

	length=length_selection(l_length)
	angle=5

	npoint=createP(length, angle, p1, p2, flag)
	
	return npoint, length

def basal_max(basal): #returns the highest index of basal dendrites

	regex=re.search('dend\[(\d+)\]', basal[-1])
	b_max=int(regex.group(1))

	return b_max

def apical_max(apical): #returns the highest index of apical dendrites

	regex=re.search('apic\[(\d+)\]', apical[-1])
	a_max=int(regex.group(1))

	return a_max

def new_dend(dend, b_max, a_max, basal, apical): #it returns two new dendrites for branching

	regex=re.search('(\w+)\[', dend)

	if str(regex.group(1))=='dend':

		b_max=basal_max(basal)
		dend_index_a=b_max+1
		new_dend_a='dend[' + str(dend_index_a) + ']'
		basal.append(new_dend_a)

		dend_index_b=b_max+2
		new_dend_b='dend[' + str(dend_index_b) + ']'
		basal.append(new_dend_b)

	if str(regex.group(1))=='apic':

		a_max=apical_max(apical)
		apical_index_a=a_max+1
		new_dend_a='apic[' + str(apical_index_a) + ']'
		apical.append(new_dend_a)

		apical_index_b=a_max+2
		new_dend_b='apic[' + str(apical_index_b) + ']'
		apical.append(new_dend_b)

	return new_dend_a, new_dend_b


def extend_dendrite(dend, new_dist, point1, point2): #grows the dendrite and returns a list of the new lines

	new_lines=[]
	dist_sum=0

	my_point2=point2

	while dist_sum<new_dist[dend]:
		flag=1
		(npoint, length)=add_point(point1, point2, flag)
		
		new_lines.append(npoint[0])

		point1=point2
		point2=npoint[0]

		dist_sum+=length

	diff=dist_sum-float(new_dist[dend])

	if len(new_lines)==1:
		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', my_point2)
		x2=float(regex.group(1))
		y2=float(regex.group(2))
		z2=float(regex.group(3))
	else:
		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', new_lines[-2])
		x2=float(regex.group(1))
		y2=float(regex.group(2))
		z2=float(regex.group(3))

	regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', new_lines[-1])
	x1=float(regex.group(1))
	y1=float(regex.group(2))
	z1=float(regex.group(3))

	xn=x2-x1
	yn=y2-y1	
	zn=z2-z1

	per=1-(length-diff)/length

	xn=round_to((x1+per*xn),0.01)
	yn=round_to((y1+per*yn),0.01)
	zn=round_to((z1+per*zn),0.01)

	newpoint='\tpt3dadd(%.2f, %.2f, %.2f, 0.5)' % (xn, yn, zn)
	new_lines[-1]=newpoint

	return new_lines

def grow_dendrite(dend, root, length_r, new_dist, point1, point2): #grows the dendrite and returns a list of the new lines

	new_lines=[]
	string='  ' + str(dend) + ' {pt3dclear()'
	new_lines.append(string)
	new_lines.append(root)
	dist_sum=length_r

	my_point2=point2
	my_length=length_r

	while dist_sum<new_dist[dend]:
		flag=1
		(npoint, length)=add_point(point1, point2, flag)
		
		new_lines.append(npoint[0])

		point1=point2
		point2=npoint[0]

		dist_sum+=length

	diff=dist_sum-float(new_dist[dend])

	#must fix the bug

	if len(new_lines)==2:
		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', my_point2)
		x2=float(regex.group(1))
		y2=float(regex.group(2))
		z2=float(regex.group(3))
	else:
		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', new_lines[-2])
		x2=float(regex.group(1))
		y2=float(regex.group(2))
		z2=float(regex.group(3))

	regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),', new_lines[-1])
	x1=float(regex.group(1))
	y1=float(regex.group(2))
	z1=float(regex.group(3))

	xn=x2-x1
	yn=y2-y1	
	zn=z2-z1

	if len(new_lines)==2:
		per=1-(my_length-diff)/my_length

	else:
		per=1-(length-diff)/length

	xn=round_to((x1+per*xn),0.01)
	yn=round_to((y1+per*yn),0.01)
	zn=round_to((z1+per*zn),0.01)

	newpoint='\tpt3dadd(%.2f, %.2f, %.2f, 0.5)' % (xn, yn, zn)
	new_lines[-1]=newpoint

	string='  }'
	new_lines.append(string)
	return new_lines

def how_much(new_dist, dend, amount, hm_choice, dist):

	if hm_choice=='percent':
		new_dist[dend]=dist[dend]*amount/100


	if hm_choice=='micrometers':
		new_dist[dend]=amount

	return new_dist[dend]

def shrink(who, amount, hm_choice, dist, dbe, start_con, end_con, parsed_con, hoc_lines): #returns the new lines of the .hoc file with the selected dendrites shrinked

	if hm_choice=='percent':
		amount=100-amount

	new_lines=[]

	new_dist=dict()

	no_print=[]
	for dend in who:

		new_dist[dend]=how_much(new_dist, dend, amount, hm_choice, dist)

		dist_sum=0
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
					dist_sum+=distance(x,xp,y,yp,z,zp)

				if dist_sum>new_dist[dend]:
					diff=dist_sum-float(new_dist[dend])

					xn=x-xp
					yn=y-yp	
					zn=z-zp

					per=1-diff/distance(x,xp,y,yp,z,zp)

					xn=round_to((xp+per*xn),0.01)
					yn=round_to((yp+per*yn),0.01)
					zn=round_to((zp+per*zn),0.01)

					hoc_lines[i]='\tpt3dadd(%.2f, %.2f, %.2f, 0.5)' % (xn, yn, zn)

					suspend=i+1
					break

		for i in range(suspend,e):
			no_print.append(i)

	newfile=[]
	i=0
	while i < len(hoc_lines):
		if i>start_con and i<end_con:
			for line in parsed_con:
				regex=re.search(r'connect (\w+\[\d+\])', line)
				d=str(regex.group(1))
				if d in who:
					pass
				else:
					newfile.append('  ' + line)
			i=end_con-1
		if i not in no_print:
			newfile.append(hoc_lines[i])

		i+=1

	#print ('\n').join(newfile)
	return newfile

def remove(who, dbe, start_con, end_con, parsed_con, hoc_lines): #returns the new lines of the .hoc file with the selected dendrites removed

	no_print=[]

	for dend in who:
		dist_sum=0
		b=dbe[dend][0]-1
		e=dbe[dend][1]+2
		for i in range(b,e):
			no_print.append(i)


	newfile=[]
	i=0
	while i < len(hoc_lines):
		if i>start_con and i<end_con:
			for line in parsed_con:
				regex=re.search(r'connect (\w+\[\d+\])', line)
				d=str(regex.group(1))
				if d in who:
					pass
				else:
					newfile.append('  ' + line)
			i=end_con-1
		if i not in no_print:
			newfile.append(hoc_lines[i])
		i+=1
	return newfile

def extend(who, amount, hm_choice, dist, dbe, hoc_lines): #returns the new lines of the .hoc file with the selected dendrites extended

	new_dist=dict() #saves the legth [value] of the new dendrite to its name [key]
	add_these_lines=dict() #saves the list of lines [value] of the newly grown dendrite to its name [key]
	new_dends=dict() #saves the list of names [value] of the new dendrites to the root dendrite [key]

	for dend in who:

		new_dist[dend]=how_much(new_dist, dend, amount, hm_choice, dist)

		i=dbe[dend][1]

		n=0
		my_list=[]
		while len(my_list)<2:
			if re.search(r'pt3dadd\((.*?),(.*?),(.*?),', hoc_lines[i-n]):
				my_list.append(hoc_lines[i-n])
			n+=1

		point1=my_list[1]
		point2=my_list[0]

		add_these_lines[dend]=extend_dendrite(dend, new_dist, point1, point2)

	suspend=[]
	for dend in who:
		suspend.append(int(dbe[dend][1]+1))

	newfile=[]
	i=0

	while i < len(hoc_lines):
		regex=re.search('pt3dclear', hoc_lines[i])
		if regex:
			regex=re.search('\s?(\S+)\s+{pt3dclear', hoc_lines[i])
			current_dendrite=regex.group(1)
			if current_dendrite=='soma':
				current_dendrite='soma[0]'
			if current_dendrite=='dend':
				current_dendrite='dend[0]'
			if current_dendrite=='apic':
				current_dendrite='apic[0]'
			for dend in who:
				if dend==current_dendrite:
					#print str(current_dendrite) + str(hoc_lines[i]) + str(i)
					growing_dendrite=dend
		if i in suspend:
			for line in add_these_lines[growing_dendrite]:
				newfile.append(str(line))
		newfile.append(hoc_lines[i])
		i+=1

	return newfile

def branch(who, b_max, a_max, basal, apical, hm_choice, amount, dist, dbe, hoc_lines, end_con): #returns the new lines of the .hoc file with the selected dendrites extended

	new_dist=dict() #saves the legth [value] of the new dendrite to its name [key]
	add_these_lines=dict() #saves the list of lines [value] of the newly grown dendrite to its name [key]
	new_dends=dict() #saves the list of names [value] of the new dendrites to the root dendrite [key]

	new_connections=[]

	for dend in who:

		(new_dend_a, new_dend_b)=new_dend(dend, b_max, a_max, basal, apical)

		#connect dend[12](0), dend[11](1)

		new_con='  connect ' + str(new_dend_a) + '(0), ' + str(dend) + '(1)'
		new_connections.append(new_con)

		new_con='  connect ' + str(new_dend_b) + '(0), ' + str(dend) + '(1)'
		new_connections.append(new_con)

		d=[]
		d.append(new_dend_a)
		d.append(new_dend_b)
		new_dends[dend]=d

		new_dist[new_dend_a]=how_much(new_dist, dend, amount, hm_choice, dist)
		new_dist[new_dend_b]=how_much(new_dist, dend, amount, hm_choice, dist)

		dist_sum=0
		i=dbe[dend][1]

		n=0
		my_list=[]
		while len(my_list)<2:
			if re.search(r'pt3dadd\((.*?),(.*?),(.*?),', hoc_lines[i-n]):
				my_list.append(hoc_lines[i-n])
			n+=1

		point1=my_list[1]
		point2=my_list[0]

		flag=2

		(npoint, length_r)=add_point(point1, point2, flag)

		root1=npoint[0]
		root2=npoint[1]

		root=hoc_lines[i]

		point1=root
		point2=root1

		add_these_lines[new_dend_a]=grow_dendrite(new_dend_a, root, length_r, new_dist, point1, point2)
		

		point1=root
		point2=root2

		add_these_lines[new_dend_b]=grow_dendrite(new_dend_b, root, length_r, new_dist, point1, point2)

	suspend=[]
	for dend in who:
		suspend.append(int(dbe[dend][1])+1)


	newfile=[]
	i=0
	while i < len(hoc_lines):
		regex=re.search('pt3dclear', hoc_lines[i])

		if regex:
			regex=re.search('\s?(\S+)\s+{pt3dclear', hoc_lines[i])
			current_dendrite=regex.group(1)
			if current_dendrite=='soma':
				current_dendrite='soma[0]'
			if current_dendrite=='dend':
				current_dendrite='dend[0]'
			if current_dendrite=='apic':
				current_dendrite='apic[0]'
			for dend in who:
				if dend==current_dendrite:
					branching_dendrite=dend

		newfile.append(hoc_lines[i])

		if i==end_con-2:
			for n in new_connections:
				newfile.append(n)

		if i in suspend:
			for line in add_these_lines[new_dends[branching_dendrite][0]]:
				newfile.append(line)
			for line in add_these_lines[new_dends[branching_dendrite][1]]:
				newfile.append(line)

		i+=1

	return newfile

(length, l_length)=length_distribution()
