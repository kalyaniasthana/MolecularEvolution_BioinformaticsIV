import networkx as nx
import sys
import copy
import numpy as np
from collections import Counter

AA = np.array(['G','A','S','P','V','T','C','I','L','N','D','Q','K','E','M','H','F','R','Y','W','X','Z'])
AW = np.array([ 57,71,87,97,99,101,103,113,113,114,115,128,128,129,131,137,147,156,163,186,4,5])


def graph_spectrum_input(file):
	masses = [0]
	read = open(file)
	for line in read:
		l = line.split(' ')
		l = list(map(int, l))
		masses += l

	return masses

def graph_spectrum(masses):

	graph = []
	d = {}

	n = len(masses)
	for i in range(0, n):
		mass = masses[i]
		for j in range(i+1, n):
			find = masses[j] - mass
			if find in AW:
				index = np.where(AW==find)
				acid = AA[index]
				graph.append(str(mass) + '->' + str(masses[j]) + ':' + str(acid[0]))
				if mass not in d:
					d[mass] = []
				d[mass].append(masses[j])
	return graph, d

def ideal_spectrum(peptide):
	peptide = list(peptide)
	prefix_mass, suffix_mass = 0, 0

	spectrum = [0]
	for i in range(len(peptide)):
		prefix = peptide[i]
		suffix = peptide[-i - 1]
		prefix_mass += AW[np.where(AA == prefix)][0]
		suffix_mass += AW[np.where(AA == suffix)][0]
		spectrum.append(prefix_mass)
		spectrum.append(suffix_mass)
	spectrum = list(set(spectrum))
	spectrum.sort()
	return spectrum


def all_paths(start, end, d, visited, nodes, path, paths):
	visited[np.where(nodes == start)] = True
	path.append(start)
	if start == end:
		#print(path)
		paths.append(copy.deepcopy(path))
		path.pop()
		visited[np.where(nodes == start)] = False
		return
	else:
		for i in d[start]:
			if visited[np.where(nodes == i)] == False:
				all_paths(i, end, d, visited, nodes, path, paths)
	path.pop()
	visited[np.where(nodes == start)] = False

def decoding_ideal_spectrum(spectrum):
	
	graph, d = graph_spectrum(spectrum)
	nodes = []

	for key in d:
		nodes.append(key)
		for item in d[key]:
			nodes.append(item)

	nodes = np.array(list(set(nodes)))

	visited = np.array([False for i in range(len(nodes))])
	start = np.min(nodes)
	end = np.max(nodes)
	path = []
	paths = []
	all_paths(start, end, d, visited, nodes, path, paths)
	for path in paths:
		peptide = ''
		x = len(path)
		for i in range(1, x):
			mass = path[i] - path[i-1]
			peptide += str(AA[np.where(AW == mass)][0])
		#print(ideal_spectrum(peptide), 'ideal')
		#print(spectrum, 'find')
		if Counter(ideal_spectrum(peptide)) == Counter(spectrum):
			return peptide

def peptide_vector(peptide):
	peptide = list(peptide)
	prefix_mass = 0

	spectrum = []
	for i in range(len(peptide)):
		prefix = peptide[i]
		prefix_mass += AW[np.where(AA == prefix)][0]
		spectrum.append(prefix_mass)

	spectrum = list(set(spectrum))
	spectrum.sort()
	last = spectrum[len(spectrum) - 1]
	
	vector = [0 for i in range(last)]
	for i in spectrum:
		vector[i-1] = 1
	return vector

peptide = 'EQAVMRFWGGLQSFPTTADHA'
v = peptide_vector(peptide)
for i in v:
	print(i, end = ' ')
print('\n')

'''
file = 'decoding.txt'
spectrum = graph_spectrum_input(file)
print(decoding_ideal_spectrum(spectrum))
'''