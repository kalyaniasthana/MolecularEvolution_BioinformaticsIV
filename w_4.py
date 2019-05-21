import networkx as nx
import sys
import copy
import numpy as np

AA = np.array(['G','A','S','P','V','T','C','I','L','N','D','Q','K','E','M','H','F','R','Y','W'])
AW = np.array([ 57,71,87,97,99,101,103,113,113,114,115,128,128,129,131,137,147,156,163,186])


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

	n = len(masses)
	for i in range(0, n):
		mass = masses[i]
		for j in range(i+1, n):
			find = masses[j] - mass
			if find in AW:
				index = np.where(AW==find)
				acid = AA[index]
				graph.append(str(mass) + '->' + str(masses[j]) + ':' + str(acid[0]))
	return graph

file = 'graph_spectrum.txt'
masses = graph_spectrum_input(file)
graph = graph_spectrum(masses)
for i in graph:
	print(i)
