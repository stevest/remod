import re
from math import sqrt
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import sys

import numpy as np
from random import uniform, randrange
from math import cos, sin, pi, sqrt, radians, degrees

def plot_(my_file, my_plot):

	x_points=[]
	y_points=[]
	z_points=[]
	diameter=[]

	for line in my_file:

		regex=re.search(r'pt3dadd\((.*?),(.*?),(.*?),(.*?)\)', line)
		regex1=re.search('(.*?)pt3dclear', line)
		regex2=re.search('objref', line)

		if regex1 or regex2:

			for i in range(len(x_points)-1):
				x=[ x_points[i], x_points[i+1] ]
				y=[ y_points[i], y_points[i+1] ]
				z=[ z_points[i], z_points[i+1] ]
				d=diameter[i]
				parameters=[x, y, z, d]
				my_plot.append(parameters)

			x_points=[]
			y_points=[]
			z_points=[]
			diameter=[]

		elif regex:
			x_points.append(float(regex.group(1)))
			y_points.append(float(regex.group(2)))
			z_points.append(float(regex.group(3)))
			diameter.append(float(regex.group(4)))

	return my_plot


def graph(initial_file, modified_file, action):

	fig = plt.figure()
	ax = Axes3D(fig)
	#ax = fig.gca(projection='3d')

	plot_before=[]
	plot_after=[]

	plot_before=plot_(initial_file, plot_before)
	plot_after=plot_(modified_file, plot_after)

	if action=='shrink' or action=='remove':
		plot_after = [x for x in plot_before if x not in plot_after]
	if action=='extend' or action=='branch':
		plot_after = [x for x in plot_after if x not in plot_before]

	l=[0,1]

	k=0
	for i in plot_before:
		if k in l:
			pass
		else:
			ax.plot(i[0], i[1], i[2], linewidth=i[3], c='b', alpha=1)
			#print i[0][0], i[1][0], i[2][0], i[0][1], i[1][1], i[2][1], i[3]
		k+=1

	k=0
	for i in plot_after:
		if k in l:
			pass
		else:
			ax.plot(i[0], i[1], i[2], linewidth=i[3], c='green', alpha=1)
			#print i[0][0], i[1][0], i[2][0], i[0][1], i[1][1], i[2][1], i[3]

		k+=1

	ax.tick_params(labelsize=8)
	plt.show()
