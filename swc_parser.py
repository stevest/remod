import re
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

my_file="c11563.CNG.swc" #file name
index=[]
point={}

for line in open(my_file):
	
	# 697 4 156.5 -633.5 -96 0.15 696  (.*?) (.*?) (.*?) (.*?) (.*?)
	regex=re.search(r'(\d+) (\d+) (.*?) (.*?) (.*?) (.*?) (-?\d+)', line)

	if regex:
		i=int(regex.group(1))
		l=int(regex.group(2))
		x=float(regex.group(3))
		y=float(regex.group(4))
		z=float(regex.group(5))
		d=float(regex.group(6))
		c=int(regex.group(7))

		mylist=[x, y, z, d, i, c, l]
		point[i]=mylist
		index.append(i)


plot_neuron=[]

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

nbp={}
nodes=[]
for i in index:
	c=point[i][5]
	mylist=[]
	count=-1
	for k in index:
		if c==point[k][5]:
			mylist.append(k)
			count+=1
	if count>0:
		if c not in nodes:
			#print c, mylist
			nodes.append(c)
			nbp[c]=mylist

print nodes

for i in nodes:	
	#print
	#print i
	for n in nbp[i]:
		next=n
		dendrite=[]
		for k in index:
			if next==point[k][5]:
				next=k
				dendrite.append(k)
			if k in nodes and k>n:
				break
		#print '>' +str(n) + str(dendrite)
