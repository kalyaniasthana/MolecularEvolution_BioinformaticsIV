
#I'll try to follow PEP from now on
'''
class Edge:
	def __init__(self, weight, start, end):
		self.weight = weight
		self.start = start
		self.end = end
'''
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
		#edge = Edge(int(n[1]), int(l[0]), int(n[0]))
		#edges.append(edge)
	return d_nodes, d_weights

def bfs(graph, start, end):   
    queue = []
    queue.append([start])
    while queue:
        path = queue.pop(0)
        #print(path)
        node = path[-1]
        if node == end:
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            if new_path not in queue:
            	queue.append(new_path)

            #print(queue)

'''
def dfs(d_nodes, start, end):
	stack = [start]
	seen = [start]
	path = []
	while len(stack) > 0:
		v = stack.pop()
		path.append(v)
		if v == end:
			return path
		for u in d_nodes[v]:
			if not u in seen:
				seen.append(u)
				stack.append(u)
'''


def pairs_in_list(l):
	pairs = []
	for num in l:
		for num_ in l:
			t_1 = (num, num_)
			t_2 = (num_, num)
			if num != num_:
				if t_1 not in pairs and t_2 not in pairs:
					pairs.append(t_1)
	return pairs

def adjacent_pairs(l):
	pairs = []
	i = 0
	while i < len(l) - 1:
		pairs.append((l[i], l[i+1]))
		i += 1
	return pairs
def dfs(graph, start, end):
    stack, path = [start], []

    while stack:
        vertex = stack.pop()
        if vertex in path:
            continue
        path.append(vertex)
        for neighbor in graph[vertex]:
            stack.append(neighbor)
            if neighbor == end:
            	path.append(neighbor)
            	return path

            	

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







	'''
	for path in paths:
		start = path[0]
		end = path[-1]
		d = 0
		for i in range(0, len(path) - 1):
			try:
				index = d_nodes[path[i]].index(path[i+1])
				d += d_weights[path[i]][index]
			except:
				index = d_nodes[path[i+1]].index(path[i])
				d += d_weights[path[i+1]][index]
		mat[start][end] = d
		mat[end][start] = d
	return mat

	

	paths = []
	for node in d_nodes:
		paths.append(dfs(d_nodes, node))
	m = len(paths[0])
	mat = []
	for i in range(m):
		l = []
		for j in range(m):
			l.append(0)
		mat.append(l)
	distances = []
	for path in paths:
		dist = [0]
		d = 0
		for i in range(len(path) - 1):
			try:
				index = d_nodes[path[i]].index(path[i+1])
				d += d_weights[path[i]][index]
			except:
				try:
					index = d_nodes[path[i+1]].index(path[i])
					d += d_weights[path[i+1]][index]
				except:
					d = 0
			dist.append(d)
		distances.append(dist)
	
	for i in range(m):
		keys = paths[i]
		values = distances[i]
		for j in range(m):
			mat[keys[0]][j] = values[j]
	'''


n = 32
file = '../Downloads/dataset_10328_12.txt'
d_nodes, d_weights = read_distance_between_leaves(file)
#mat = distance_between_leaves(n, d_nodes, d_weights)
#for l in mat:
#	print(*l)
m = distance_between_leaves(n, d_nodes, d_weights)

for line in m:
	print(*line)