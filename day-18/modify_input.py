#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 20:22:26 2019

@author: dennis
"""

from string import ascii_lowercase
from string import ascii_uppercase

import networkx as nx

from navigator import Navigator

with open('data/input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]

nav = Navigator(grid)
all_nodes = set([(y, x) for y in range(1, 80) for x in range(1, 80)])
used = set()
tot_dist = 0
for source in ascii_lowercase+ascii_uppercase:
    for target in ascii_lowercase+ascii_uppercase:
        if source == target:
            continue
        if source.islower():
            source_pos = nav.keys[source]
        else:
            if source not in nav.doors:
                continue
            source_pos = nav.doors[source]
        if target.islower():
            target_pos = nav.keys[target]
        else:
            if target not in nav.doors:
                continue
            target_pos = nav.doors[target]
        path = nx.astar_path(nav.graph, (source_pos.y, source_pos.x), (target_pos.y, target_pos.x))
        tot_dist += len(path)
        for node in path:
            used.add(node)

grid = [[char for char in row] for row in grid]
for node in all_nodes:
    if node not in used:
        grid[node[0]][node[1]] = '#'
grid = [''.join(row) for row in grid]

nav = Navigator(grid)
all_nodes = set([(y, x) for y in range(1, 80) for x in range(1, 80)])
used = set()
tot_dist2 = 0
for source in ascii_lowercase+ascii_uppercase:
    for target in ascii_lowercase+ascii_uppercase:
        if source == target:
            continue
        if source.islower():
            source_pos = nav.keys[source]
        else:
            if source not in nav.doors:
                continue
            source_pos = nav.doors[source]
        if target.islower():
            target_pos = nav.keys[target]
        else:
            if target not in nav.doors:
                continue
            target_pos = nav.doors[target]
        path = nx.astar_path(nav.graph, (source_pos.y, source_pos.x), (target_pos.y, target_pos.x))
        tot_dist2 += len(path)
        for node in path:
            used.add(node)

assert tot_dist == tot_dist2

#useless = []
#for char in ascii_uppercase:
#    if len(nav._valid_neighbours((nav.doors[char].y, nav.doors[char].x))) == 1:
#        useless.append(char)

with open('data/modified_input.txt', 'w') as f:
    for row in grid:
        f.write(row+'\n')
