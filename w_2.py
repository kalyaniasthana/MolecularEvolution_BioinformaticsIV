import networkx as nx
import sys
import copy
import numpy as np


def input_parsimony(file, n):
	read = open(file)
	descendant = {}
	successor = {}
	x = 0

	dna = []
	for i in range(n, 2*n - 1):
		descendant[i] = []

	for line in read:
		l = line.strip()
		l = l.split('->')
		if x < n:
			descendant[int(l[0])].append(x)
			successor[x] = int(l[0])
			dna.append(l[1])
			x += 1
		else:
			descendant[int(l[0])].append(int(l[1]))
			successor[int(l[1])] = int(l[0])

	return descendant, successor, dna

def hamming_distance(string_1, string_2):
	d = 0
	for i in range(len(string_1)):
		if string_1[i] != string_2[i]:
			d += 1
	return d


def small_parsimony(descendant, successor, dna, n):

	m = 2*n - 1 #total number of node
	l = len(dna[0]) #length of sequences
	symbols = {'A' : 0, 'C': 1, 'G': 2, 'T': 3} #bases
	reverse_symbols = {0: 'A', 1: 'C', 2: 'G', 3: 'T' }
	x = []
	# d1- node number, d2 - dna string, d3 -bases
	for i in range(4):
		x.append(float('Inf'))

	y = []
	for i in range(l):
		y.append(x)

	z = []
	for i in range(m):
		z.append(y)

	#number of 2D arrays = number of nodes in tree, z
	#number of rows in a 2D array = length of dna strings, y
	#number of columns = 4 because there are four bases, x

	nodes = np.array(z) 

	tags = [0 for i in range(m)]

	for i in range(n, m):
		dna.append('')

	#for leaf nodes
	for i in range(n):
		tags[i] = 1
		x = list(dna[i])
		for j in range(l):
			symbol = x[j]
			nodes[i, j, symbols[symbol]] = 0

	for i in range(m):
		# node i
		if tags[i] == 0:
			son_i, daughter_i = descendant[i][0], descendant[i][1]
			#print(son_i, daughter_i, i)
			tags[i] = 1
			# dna string
			for j in range(l):
				for k in range(4):

					alpha = np.ones(4)
					alpha[k] = 0
					#x = np.argmin(nodes[son_i, j])
					#print(x)
					#sys.exit()
					#y = np.argmin(nodes[daughter_i, j])
					nodes[i, j, k] = min(nodes[son_i, j, :] + alpha) + min(nodes[daughter_i, j, :] + alpha)

	#backtrack to get symbols
	root_dna = ''
	for j in range(l):
		candidate_root = np.argmin(nodes[m-1, j])
		root_dna += reverse_symbols[candidate_root]

	dna[m-1] = root_dna

	#backtracking left, #parsimony score calculation left

	for i in range(m-2, -1 , -1):
		if i < n:
			break
		suc = successor[i]
		dna_ = ''
		for j in range(l):
			current_node_scores = nodes[i, j, :]
			parent_symbol = dna[suc][j]
			#print(parent_symbol)
			#sys.exit()
			parent_symbol_number = symbols[parent_symbol]
			alpha = np.ones(4)
			alpha[parent_symbol_number] = 0
			minimum_number = np.argmin(current_node_scores + alpha)
			dna_ += reverse_symbols[minimum_number]
		dna[i] = dna_


	p = []
	string = ''
	score = 0
	for node in successor:
		
		dist = hamming_distance(dna[node], dna[successor[node]])
		string = dna[node] + '->' + dna[successor[node]] + ':' + str(dist)
		p.append(string)
		string = dna[successor[node]] + '->' + dna[node] + ':' + str(dist)
		p.append(string)
		score += dist

	return p, score


def small_parsimony_unrooted_input(file, n):
	read = open(file)
	descendant = {}
	successor = {}
	x = 0
	m = 2*n - 1
	dna = []
	for i in range(n, 2*n - 1):
		descendant[i] = []

	for line in read:
		l = line.strip()
		l = l.split('->')

		try:
			int(l[0])
			if x < n:
				descendant[int(l[0])].append(x)
				successor[x] = int(l[0])
				dna.append(l[1])
				x += 1
			elif (int(l[0]) == m - 3 and int(l[1]) == m - 2) or (int(l[1]) == m - 3 and int(l[0]) == m-2):
				descendant[m-1].append(int(l[0]))
				successor[int(l[0])] = m-1
			else:
				descendant[int(l[0])].append(int(l[1]))
				successor[int(l[1])] = int(l[0])

		except:
			#print(x, 'except')
			pass

	return descendant, successor, dna

def small_parsimony_unrooted(descendant, successor, dna, n):

	m = 2*n - 1 #total number of node
	l = len(dna[0]) #length of sequences
	symbols = {'A' : 0, 'C': 1, 'G': 2, 'T': 3} #bases
	reverse_symbols = {0: 'A', 1: 'C', 2: 'G', 3: 'T' }
	x = []
	# d1- node number, d2 - dna string, d3 -bases
	for i in range(4):
		x.append(float('Inf'))

	y = []
	for i in range(l):
		y.append(x)

	z = []
	for i in range(m):
		z.append(y)

	#number of 2D arrays = number of nodes in tree, z
	#number of rows in a 2D array = length of dna strings, y
	#number of columns = 4 because there are four bases, x

	nodes = np.array(z) 

	tags = [0 for i in range(m)]

	for i in range(n, m):
		dna.append('')

	#for leaf nodes
	for i in range(n):
		tags[i] = 1
		x = list(dna[i])
		for j in range(l):
			symbol = x[j]
			nodes[i, j, symbols[symbol]] = 0

	for i in range(m):
		# node i
		if tags[i] == 0:
			son_i, daughter_i = descendant[i][0], descendant[i][1]
			#print(son_i, daughter_i, i)
			tags[i] = 1
			# dna string
			for j in range(l):
				for k in range(4):

					alpha = np.ones(4)
					alpha[k] = 0
					#x = np.argmin(nodes[son_i, j])
					#print(x)
					#sys.exit()
					#y = np.argmin(nodes[daughter_i, j])
					nodes[i, j, k] = min(nodes[son_i, j, :] + alpha) + min(nodes[daughter_i, j, :] + alpha)

	#backtrack to get symbols
	root_dna = ''
	for j in range(l):
		candidate_root = np.argmin(nodes[m-1, j])
		root_dna += reverse_symbols[candidate_root]

	dna[m-1] = root_dna

	#backtracking left, #parsimony score calculation left

	for i in range(m-2, -1 , -1):
		if i < n:
			break
		suc = successor[i]
		dna_ = ''
		for j in range(l):
			current_node_scores = nodes[i, j, :]
			parent_symbol = dna[suc][j]
			#print(parent_symbol)
			#sys.exit()
			parent_symbol_number = symbols[parent_symbol]
			alpha = np.ones(4)
			alpha[parent_symbol_number] = 0
			minimum_number = np.argmin(current_node_scores + alpha)
			dna_ += reverse_symbols[minimum_number]
		dna[i] = dna_


	p = []
	string = ''
	score = 0
	dna.pop() #remove artficial root dna
	descendant[m-2].append(m-3)
	descendant[m-3].append(m-2)
	del descendant[m-1]
	del successor[m-2]
	successor[m-3] = m-2
	#print(descendant)
	#print(successor)
	#print(len(dna))
	#sys.exit()
	for node in successor:

		dist = hamming_distance(dna[node], dna[successor[node]])
		string = dna[node] + '->' + dna[successor[node]] + ':' + str(dist)
		p.append(string)
		string = dna[successor[node]] + '->' + dna[node] + ':' + str(dist)
		p.append(string)

		score += dist

	return p, score


def nearest_neighbors_input(file):
	read = open(file)
	d = {}
	for line in read:
		l = line.strip()
		l = l.split('->')
		if int(l[0]) not in d:
			d[int(l[0])] = []
		d[int(l[0])].append(int(l[1]))
	return d

def nearest_neighbors_interchange(d, a, b):

	d_1 = copy.deepcopy(d)
	d_2 = copy.deepcopy(d)

	#interchange x and y
	d_1[a].remove(b)
	d_1[b].remove(a)

	#w = d_1[a][0]
	x = d_1[a][1]

	y = d_1[b][0]
	#z = d_1[b][1]
	d_1[a].remove(x)
	d_1[x].remove(a)
	d_1[x].append(b)
	d_1[a].append(y)
	d_1[b].remove(y)
	d_1[y].remove(b)
	d_1[y].append(a)
	d_1[b].append(x)



	d_1[a].append(b)
	d_1[b].append(a)

	#interchange x and z

	d_2[a].remove(b)
	d_2[b].remove(a)

	#w = d_1[a][0]
	x = d_2[a][1]

	#y = d_1[b][0]
	z = d_2[b][1]

	d_2[a].remove(x)
	d_2[x].remove(a)
	d_2[x].append(b)
	d_2[a].append(z)
	d_2[b].remove(z)
	d_2[z].remove(b)
	d_2[z].append(a)
	d_2[b].append(x)

	d_2[a].append(b)
	d_2[b].append(a)

	tuples_1 = []
	tuples_2 = []
	for node in d_1:
		for item in d_1[node]:
			tuples_1.append((node, item))
	for node in d_2:
		for item in d_2[node]:
			tuples_2.append((node, item))

	l_1, l_2 = [], []
	for tup in tuples_1:
		l_1.append(str(tup[0]) + '->' + str(tup[1]))
	for tup in tuples_2:
		l_2.append(str(tup[0]) + '->' + str(tup[1]))

	return l_1, l_2










	
'''
n = 128
file = 'parsimony.txt'
descendant, successor, dna = input_parsimony(file, n)
p, score = small_parsimony(descendant, successor, dna, n)
print(score)
for i in p:
	print(i)
'''
'''
n = 32
file = 'parsimony.txt'
descendant, successor, dna = small_parsimony_unrooted_input(file, n)
p, score = small_parsimony_unrooted(descendant, successor, dna, n)
print(score)
for i in p:
	print(i)
'''
'''
a = 34
b = 60
file = 'nearest_neighbors.txt'
d = nearest_neighbors_input(file)
l_1, l_2 = nearest_neighbors_interchange(d, a, b)
for edge in l_1:
	print(edge)
print('\n')
for edge in l_2:
	print(edge)
'''


