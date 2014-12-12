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

	np1=[v1[0,0], v1[0,1], v1[0,2]]

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

		np2=[v2[0,0], v2[0,1], v2[0,2]]

		np_.append(np2)

	return np_

def add_point(point1, point2, flag): #returns 1 or 2 new points 

	p1=[point1[2], point1[3], point1[4]]
	p2=[point2[2], point2[3], point2[4]]

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

def new_dend(max_index): #it returns two new dendrites for branching

	new_dend_a=max_index+1
	new_dend_b=max_index+2
	
	max_index=new_dend_b
	
	return new_dend_a, new_dend_b, max_index


def extend_dendrite(dend, new_dist, point1, point2, max_index, flag): #grows the dendrite and returns a list of the new lines

	new_lines=[]
	dist_sum=0

	my_point2=point2

	seg_index=max_index

	while dist_sum<new_dist[dend]:

		(npoint, length)=add_point(point1, point2, flag)
		
		p=[seg_index+1, point2[1], npoint[0][0], npoint[0][1], npoint[0][2], point2[5], point2[0]]
		new_lines.append(p)

		seg_index+=1

		point1=point2
		point2=p

		dist_sum+=length

	diff=dist_sum-float(new_dist[dend])

	if len(new_lines)==1:
		x2=my_point2[2]
		y2=my_point2[3]
		z2=my_point2[4]
	else:
		x2=new_lines[-2][2]
		y2=new_lines[-2][3]
		z2=new_lines[-2][4]

	x1=new_lines[-1][2]
	y1=new_lines[-1][3]
	z1=new_lines[-1][4]

	xn=x2-x1
	yn=y2-y1	
	zn=z2-z1

	per=1-(length-diff)/length

	xn=round_to((x1+per*xn),0.01)
	yn=round_to((y1+per*yn),0.01)
	zn=round_to((z1+per*zn),0.01)

	newpoint=[point2[0], point2[1], xn, yn, zn, point2[5], point2[6]]
	new_lines[-1]=newpoint

	max_index=seg_index-1

	return max_index, new_lines


def how_much(new_dist, dend, amount, hm_choice, dist):

	if hm_choice=='percent':
		new_dist[dend]=dist[dend]*amount/100

	if hm_choice=='micrometers':
		new_dist[dend]=amount

	return new_dist[dend]

def shrink(who, action, amount, hm_choice, dend_add3d, dist): #returns the new lines of the .hoc file with the selected dendrites shrinked

	if hm_choice=='percent':
		amount=100-amount

	new_lines=[]

	new_dist=dict()

	for dend in who:

		dist_sum=0

		new_dist[dend]=how_much(new_dist, dend, amount, hm_choice, dist)

		mylist=[]

		for i in range(len(dend_add3d[dend])-1):

			current_point=dend_add3d[dend][i]
			next_point=dend_add3d[dend][i+1]

			xp=current_point[2]
			yp=current_point[3]
			zp=current_point[4]
			dp=current_point[5]

			point=[current_point[0], current_point[1], xp, yp, zp, dp, current_point[6]]
			mylist.append(point)

			x=next_point[2]
			y=next_point[3]
			z=next_point[4]
			d=next_point[5]

			dist_sum+=distance(x,xp,y,yp,z,zp)

			if dist_sum>new_dist[dend]:

				diff=dist_sum-float(new_dist[dend])

				xn=x-xp
				yn=y-yp	
				zn=z-zp

				per=1-diff/distance(x,xp,y,yp,z,zp)

				xn='%.2f' % (round_to((xp+per*xn),0.01))
				yn='%.2f' % (round_to((yp+per*yn),0.01))
				zn='%.2f' % (round_to((zp+per*zn),0.01))

				# 1202 3 -43.5 27 19 0.15 1201
				mylist[-1]=[current_point[0], current_point[1], xn, yn, zn, dp, current_point[6]]
				
				dend_add3d[dend]=mylist	

				break

	mylist=[]

	for i in dend_add3d:
		for k in dend_add3d[i]:
			if k not in mylist:
				mylist.append(k)
	mylist.sort(key=lambda x: x[0])

	newfile=[]
	for k in mylist:
		newfile.append(' %d %d %.2f %.2f %.2f %.2f %d' % (k[0], k[1], k[2], k[3], k[4], k[5], k[6]))

	return newfile

def remove(who, action, dend_add3d): #returns the new lines of the .hoc file with the selected dendrites shrinked

	new_lines=[]

	for dend in who:
		dend_add3d[dend]=[]

	mylist=[]

	for i in dend_add3d:
		for k in dend_add3d[i]:
			if k not in mylist:
				mylist.append(k)
	mylist.sort(key=lambda x: x[0])

	newfile=[]
	for k in mylist:
		newfile.append(' %d %d %.2f %.2f %.2f %.2f %d' % (k[0], k[1], k[2], k[3], k[4], k[5], k[6]))

	return newfile


def extend(who, action, amount, hm_choice, dend_add3d, dist, max_index): #returns the new lines of the .hoc file with the selected dendrites extended

	new_dist=dict() #saves the legth [value] of the new dendrite to its name [key]
	add_these_lines=dict() #saves the list of lines [value] of the newly grown dendrite to its name [key]

	for dend in who:
		
		new_dist[dend]=how_much(new_dist, dend, amount, hm_choice, dist)

		point1=dend_add3d[dend][-1]
		point2=dend_add3d[dend][-2]

		(max_index, add_these_lines[dend])=extend_dendrite(dend, new_dist, point1, point2, max_index, 1)

		dend_add3d[dend]=dend_add3d[dend]+add_these_lines[dend]

	mylist=[]
	for i in dend_add3d:
		for k in dend_add3d[i]:
			mylist.append(k)
	mylist.sort(key=lambda x: x[0])

	newfile=[]
	for k in mylist:
		m=' %d %d %.2f %.2f %.2f %.2f %d' % (k[0], k[1], k[2], k[3], k[4], k[5], k[6])
		newfile.append(m)

	return newfile

def branch(who, action, amount, hm_choice, dend_add3d, dist, max_index): #returns the new lines of the .hoc file with the selected dendrites extended

	new_dist=dict() #saves the legth [value] of the new dendrite to its name [key]
	add_these_lines=dict() #saves the list of lines [value] of the newly grown dendrite to its name [key]

	for dend in who:

		(new_dend_a, new_dend_b, max_index)=new_dend(max_index)

		point1=dend_add3d[dend][-1]
		point2=dend_add3d[dend][-2]

		print 'before sprout'
		print point1
		print point2
		print

		(new_point, length)=add_point(point1, point2, 2)

		new_point_a=[new_dend_a, point2[1], new_point[0][0], new_point[0][1], new_point[0][2], point2[5], point2[0]]
		new_point_b=[new_dend_b, point2[1], new_point[1][0], new_point[1][1], new_point[1][2], point2[5], point2[0]]

		print 'sprouts'
		print new_point_a
		print new_point_b
		print

		#new_dend_a

		new_dist[new_dend_a]=how_much(new_dist, dend, amount, hm_choice, dist)

		point1=new_point_a
		point2=dend_add3d[dend][-1]

		print 'sprout 1'
		print point1
		print point2
		print

		(max_index, add_these_lines[new_dend_a])=extend_dendrite(dend, new_dist, point1, point2, max_index, 1)
		dend_add3d[new_dend_a]=dend_add3d[dend]+add_these_lines[new_dend_a]		

		#new_dend_b

		new_dist[new_dend_b]=how_much(new_dist, dend, amount, hm_choice, dist)

		point1=new_point_b
		point2=dend_add3d[dend][-1]

		print 'sprout 1'
		print point1
		print point2
		print

		(max_index, add_these_lines[new_dend_b])=extend_dendrite(dend, new_dist, point1, point2, max_index, 1)
		dend_add3d[new_dend_b]=dend_add3d[dend]+add_these_lines[new_dend_b]


		mylist=[]
		for i in dend_add3d:
			for k in dend_add3d[i]:
				mylist.append(k)
		mylist.sort(key=lambda x: x[0])

		newfile=[]
		for k in mylist:
			m=' %d %d %.2f %.2f %.2f %.2f %d' % (k[0], k[1], k[2], k[3], k[4], k[5], k[6])
			newfile.append(m)

	return newfile

(length, l_length)=length_distribution()
