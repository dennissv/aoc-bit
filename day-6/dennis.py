#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:51:05 2019

@author: dennis
"""

import networkx as nx

G = nx.Graph()
graph = dict()
with open('data/input.txt', 'r') as f:
    for line in f.readlines():
        orbits = line.strip('\n').split(')')
        G.add_edge(orbits[1], orbits[0])
        graph[orbits[1]] = orbits[0]

def find_sub_orbits(g, c):
    if c in g:
        return 1+find_sub_orbits(g, g[c])
    return 0

print('Part 1: {}'.format(sum(find_sub_orbits(graph, key) for key in graph)))
print('Part 1: {}'.format(nx.shortest_path_length(G, graph['YOU'], graph['SAN'])))
