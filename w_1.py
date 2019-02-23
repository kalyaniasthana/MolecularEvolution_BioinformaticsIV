
#I'll try to follow PEP from now on

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
	val = float('Inf')
	for i in range(n):
		for k in range(n):
			dist = (mat[i][j] + mat[j][k] - mat[i][k])/2
			if j != i and j != k: 
				if dist < val:
					val = dist
	return int(val)


'''

n = 32
file = '../Downloads/dataset_10328_12.txt'
d_nodes, d_weights = read_distance_between_leaves(file)
m = distance_between_leaves(n, d_nodes, d_weights)
for line in m:
	print(*line)
'''
'''
n = 21
j = 17
file = '../Downloads/dataset_10329_11.txt'
mat = limb_length_input(file)
print(limb_length(n, j, mat))
'''