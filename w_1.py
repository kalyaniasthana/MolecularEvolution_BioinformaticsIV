
#I'll try to follow PEP from now on
from time import time
import networkx as nx
import sys
import copy
import numpy as np
def read_distance_between_leaves(file):
	read = open(file)
	edges = []
	d_nodes = {}
	d_weights = {}
	for line in read:
		l = line.strip()
		l = l.split('->')
		if int(l[0]) not in d_nodes:
			d_nodes[int(l[0])] = []
		if int(l[0]) not in d_weights:
			d_weights[int(l[0])] = []
		n = l[1].split(':')
		d_nodes[int(l[0])].append(int(n[0]))
		d_weights[int(l[0])].append(int(n[1]))
	
	return d_nodes, d_weights

def distance_between_leaves(n, d_nodes, d_weights):
	#floyd warshal algorithm
	m = 0
	for node in d_nodes:
		m+=1

	mat = []
	for i in range(m):
		l = []
		for j in range(m):
			l.append(float('Inf'))
		mat.append(l)

	for node in d_nodes:
		for edge in d_nodes[node]:
			index = d_nodes[node].index(edge)
			mat[node][edge] = d_weights[node][index]

	for i in range(m):
		mat[i][i] = 0

	for k in range(m):
		for i in range(m):
			for j in range(m):
				mat[i][j] = min(mat[i][j], mat[i][k] + mat[k][j])

	new_mat = []
	for i in range(n):
		l = []
		for j in range(n):
			l.append(0)
		new_mat.append(l)

	for i in range(n):
		for j in range(n):
			new_mat[i][j] = mat[i][j]

	return new_mat

def limb_length_input(file):
	read = open(file)
	mat = []
	for line in read:
		l = line.strip()
		l = l.split(' ')
		l = list(map(int, l))
		mat.append(l)
	return mat

def limb_length(n, j, mat):
	#start = time()
	val = float('Inf')
	for i in range(n):
		if i != j:
			for k in range(n):
				if k != j:
					dist = (mat[i][j] + mat[j][k] - mat[i][k])/2
					if dist < val:
						val = dist
	#end = time()
	#print(end - start)
	return int(val)

def additive_phylogeny(mat, counter):
	n = len(mat)
	if counter == 2:
		G = nx.Graph()
		G.add_weighted_edges_from([(0, 1, mat[0][1])])
		return G
	ll = limb_length(n, counter - 1, mat)
	for j in range(0, counter - 1):
		mat[j][counter - 1] -= ll
		mat[counter - 1][j] = mat[j][counter - 1]
	i, k = 0, 0
	for p in range(0, n):
		for q in range(0, n):
			if mat[p][q] == mat[p][counter - 1] + mat[counter - 1][q]:
				i = p
				k = q
				break
	counter -= 1
	x = mat[i][counter]
	G = additive_phylogeny(mat, counter)
	#v ← the (potentially new) node in T at distance x from i on the path between i and k
	#add leaf n back to T by creating a limb (v, n) of length limbLength
	'''
	 the attachment point for leaf j must be located at distance 𝐷𝑏𝑎𝑙𝑑𝑖,𝑗 from leaf i on the path
	 connecting i and k in the trimmed tree. This attachment point may occur at an existing node,
	 in which case we connect j to this node. On the other hand, the attachment point for j may occur
	 along an edge, in which case we place a new node at the attachment point and connect j to it.
	 '''
	
def upgma(mat, n):
	global distances
	distances = np.array(mat)

	#print(distances)
	new_node = copy.deepcopy(n)
	clusters = {}
	for i in range(0, n):
		clusters[i] = [i]
	G = nx.Graph()
	G.add_nodes_from([i for i in range(0, n)], age = 0)
	new_distances = copy.deepcopy(distances)
	while len(clusters) > 1:
		def distance_between_clusters(i, j):
			if i in clusters and j in clusters:
				d = sum([distances[x, y] for x in clusters[i] for y in clusters[j]])/(len(clusters[i])*len(clusters[j]))
				return d
			return 0
		#print(clusters)
		def find_closest_clusters():
			min_element = np.min(new_distances[np.nonzero(new_distances)])
			#print(min_element)
			index = np.where(new_distances == min_element)[0]
			i = index[0]
			j = index[1]
			return (i, j)

		i, j = find_closest_clusters()
		G.add_node(new_node, age = 0)
		G.add_edge(new_node, i, age = 0)
		G.add_edge(new_node, j, age = 0)
		#print(i, j)
		clusters[new_node] = clusters[i] + clusters[j]
		G.nodes[new_node]['age'] = distances[i, j]/2

		del clusters[i]
		del clusters[j]

		new_row = [distance_between_clusters(i, new_node) for i in range(len(distances))] 
		#print(new_row)
		distances = np.concatenate((distances, [new_row]))
		new_distances = np.concatenate((new_distances, [new_row]))

		m = []
		for dist in new_row:
			m.append([dist])
		m.append([float(0)])
		distances = np.append(distances, m, axis = 1)
		new_distances = np.append(new_distances, m, axis = 1)
		new_distances[i] = [0 for i in range(len(new_distances))]
		new_distances[j] = [0 for i in range(len(new_distances))]
		new_distances[:, i] = [0 for i in range(len(new_distances))]
		new_distances[:, j] = [0 for i in range(len(new_distances))]
		#print(distances)
		new_node += 1

	#return G.nodes.data()
	for u, v, a in G.edges(data=True):
		G[u][v]['age'] = abs(G.nodes[v]['age'] - G.nodes[u]['age'])
		#print(u, v, a)

	return G.edges.data()

def upgma_print(g_edges):
	l = []
	for u, v, a in g_edges:
		string = str(u) + '->' +str(v) + ':' + str('{0:.3f}'.format(a['age']))
		l.append(string)
		string = str(v) + '->' +str(u) + ':' + str('{0:.3f}'.format(a['age']))
		l.append(string)
	return l

	

'''
n = 32
file = '../Downloads/dataset_10328_12.txt'
d_nodes, d_weights = read_distance_between_leaves(file)
m = distance_between_leaves(n, d_nodes, d_weights)
for line in m:
	print(*line)
'''
'''
n = 4
j = 0
file = 'limbs.txt'
mat = limb_length_input(file)
print(limb_length(n, j, mat))
'''

'''
file = 'additive.txt'
mat = limb_length_input(file)
counter = len(mat)
G = additive_phylogeny(mat, counter)
'''
file = 'upgma.txt'
mat = limb_length_input(file)
n = 22
g_edges = upgma(mat, n)
l = upgma_print(g_edges)
l.sort()
for i in l:
	print(i)

