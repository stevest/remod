import re
from math import sqrt
from random import randint
import sys

import numpy as np
from random import uniform, randrange
from math import cos, sin, pi, sqrt, radians, degrees

def plot_(fname, plot_before):

	x_points=[]
	y_points=[]
	z_points=[]
	diameter=[]

	enter=0

	for line in open(fname):

		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),(.*?)\)', line)
		regex1=re.search('(.*?)pt3dclear', line)
		regex2=re.search('objref', line)
		regex3=re.search('soma(.*?)pt3dclear', line)

		if enter==1:

			center=re.search(r'pt3dadd\((.*?),(.*?),(.*?),(.*?)\)', line)

			x_center=regex.group(1)
			y_center=regex.group(2)
			z_center=regex.group(3)

			enter=0

		if regex3:

			enter=1

		if regex1 or regex2:

			for i in range(len(x_points)-1):
				x=[ x_points[i], x_points[i+1] ]
				y=[ y_points[i], y_points[i+1] ]
				z=[ z_points[i], z_points[i+1] ]
				d=diameter[i]
				parameters=[x, y, z, d]
				plot_before.append(parameters)

			x_points=[]
			y_points=[]
			z_points=[]
			diameter=[]

		elif regex:
			x_points.append(float(regex.group(1)))
			y_points.append(float(regex.group(2)))
			z_points.append(float(regex.group(3)))
			diameter.append(float(regex.group(4)))

	return plot_before, x_center, y_center, z_center


def graph(fname):

	plot_before=[]

	plot_before, x_center, y_center, z_center=plot_(fname, plot_before)

	l=[0,1]
	k=0

	f = open('neuron_before.txt', 'w')
	for i in plot_before:
		if k in l:
			pass
		else:
			print >>f, i[0][0], i[1][0], i[2][0], i[0][1], i[1][1], i[2][1], i[3]
		k+=1
	f.close()

	f = open('neuron_center.txt', 'w')
	print >>f, x_center, y_center, z_center
	f.close()
