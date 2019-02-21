
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
        node = path[-1]
        if node == end:
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

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

def distance(n, d_nodes, d_weights, paths):
	#print(d_nodes)
	#print(d_weights)
	mat = []
	for i in range(n):
		l = []
		for j in range(n):
			l.append(0)
		mat.append(l)

	for path in paths:
		#print(path)
		d = 0
		pairs = adjacent_pairs(path)
		for tup in pairs:
			start = tup[0]
			end = tup[1]
			try:
				index = d_nodes[start].index(end)
				d += d_weights[start][index]
			except:
				index = d_nodes[end].index(start)
				d += d_weights[end][index]
		mat[path[0]][path[-1]] = mat[path[-1]][path[0]] = d
	return mat

def distance_between_leaves(n, d_nodes, d_weights):
	l = []
	for i in range(n):
		l.append(i)
	pairs = pairs_in_list(l)
	paths = []
	for tup in pairs:
		paths.append(bfs(d_nodes, tup[0], tup[1]))
	mat = distance(n, d_nodes, d_weights, paths)
	return mat

n = 4
file = 'weights.txt'
d_nodes, d_weights = read_distance_between_leaves(file)
mat = distance_between_leaves(n, d_nodes, d_weights)
for l in mat:
	print(*l)