import re
from math import sqrt
from random import randint
import matplotlib.pyplot as plt
import sys

import numpy as np
from random import uniform, randrange
from math import cos, sin, pi, sqrt, radians, degrees

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def path_length(dlist, paths, dist):
	plength=dict()
	for dend in dlist:
		if re.search('soma', dend):
			pass
		else:
			d=0
			path_list=paths[dend].split()
			for i in path_list:
				d+=dist[i]
			plength[dend]=d
	return plength

def branch_order(dlist, paths):
	bo=dict()
	for dend in dlist:
		if re.search('soma', dend):
			pass
		else:
			var=0
			path_list=paths[dend].split()
			for i in path_list:
				var+=1
			bo[dend]=var-1
	return bo

def bo_frequency(dlist, bo):

	orders=[]
	for dend in dlist:
		if re.search('soma', dend):
			pass
		else:
			orders.append(bo[dend])

	bo_min=1 # min(orders)
	bo_max=max(orders)


	bo_freq={}

	for i in range(bo_min, bo_max+1):
		k=0
		for order in orders:
			if order==i:
				k+=1
		bo_freq[i]=k

	return bo_freq

def bo_dlength(dlist, bo, dist):

	orders=[]

	for dend in dlist:
		if re.search('soma', dend):
			pass
		else:
			orders.append(bo[dend])

	bo_min=1 # min(orders)
	bo_max=max(orders)


	bo_dlen={}
	for i in range(bo_min, bo_max+1):

		k=0
		add_length=0

		for dend in dlist:
			if re.search('soma', dend):
				pass
			else:
				if i==bo[dend]:
					k+=1
					add_length+=dist[dend]
					#print str(dend) + ' ' + str(bo[dend]) + ' ' + str(dist[dend])

		if k!=0:
			bo_dlen[i]=add_length/k

	return bo_dlen

def bo_plength(dlist, bo, plength):

	orders=[]

	for dend in dlist:
		if re.search('soma', dend):
			pass
		else:
			orders.append(bo[dend])

	bo_min=1 # min(orders)
	bo_max=max(orders)


	bo_plen={}
	for i in range(bo_min, bo_max+1):

		k=0
		add_length=0

		for dend in dlist:
			if re.search('soma', dend):
				pass
			else:
				if i==bo[dend]:
					k+=1
					add_length+=plength[dend]
					#print str(dend) + ' ' + str(bo[dend]) + ' ' + str(dist[dend])

		if k!=0:
			bo_plen[i]=add_length/k

	return bo_plen


'''plength=path_length()
bo=branch_order()
bo_freq=bo_frequency()

for dend in dlist:
	if re.search('soma', dend):
		pass
	else:
		print paths[dend]
		print plength[dend]
		print bo[dend]'''
