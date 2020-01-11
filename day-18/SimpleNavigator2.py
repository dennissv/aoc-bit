#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:20:01 2019

@author: dennis
"""

from string import ascii_lowercase
from string import ascii_uppercase

import networkx as nx

class SimpleNavigator():

    def __init__(self, grid):
        self.grid = grid
        self.to_ignore = ''#'FINOSUZ'
        self.distance_traveled = 0
        self.size = 0
        self._build_positions(grid)
        self._build_graph()
        self._calculate_distances()
        self._build_order()
        self.history = ['@']
        self.inventory = set()
        self.opened_doors = set()
        self.drones = {pos: pos for pos in '1234'}

    def get_neighbours(self, pos):
        y, x = pos
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i)+abs(j) == 1:
                    if self.grid[y+i][x+j] in '.'+ascii_lowercase+ascii_uppercase:
                        neighbours.append((y+i, x+j))
        return neighbours

    def _build_positions(self, grid):
        print('Getting positions...')
        self.positions = dict()
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                if char == '@':
                    self.start = (y, x)
                if char in ascii_lowercase+ascii_uppercase+'@'+'1234':
                    self.positions[char] = (y, x)
                    if char in ascii_lowercase:
                        self.size += 1

    def _build_graph(self):
        print('Building graph...')
        self.g = nx.Graph()
        for i in '1234':
            queue = [self.positions[i]]
            visited = set()
            while queue:
                new_queue = []
                for node in queue:
                    visited.add(node)
                    for neighbour in self.get_neighbours(node):
                        if neighbour not in visited:
                            new_queue.append(neighbour)
                            self.g.add_edge(node, neighbour)
                queue = new_queue

    def _calculate_distances(self):
        print('Calculating distances...')
        self.distances = {char: {} for char in ascii_lowercase+'1234'}
        for item1 in ascii_lowercase+'1234':
            for item2 in ascii_lowercase+'1234':
                if (item1 not in self.positions) or (item2 not in self.positions):
                    continue
                if item1 == item2:
                    continue
                if nx.has_path(self.g, self.positions[item1], self.positions[item2]):
                    self.distances[item1][item2] = nx.astar_path_length(self.g, \
                                  self.positions[item1], self.positions[item2])
       
    def _build_order(self):
        print('Building orders...')
        self.order = dict()
        for target in ascii_lowercase:
            if target not in self.positions:
                    continue
            for i in '1234':
                if nx.has_path(self.g, self.positions[i], self.positions[target]):
                    requirements = set()
                    for node in nx.astar_path(self.g, self.positions[i], self.positions[target]):
                        y, x = node
                        char = self.grid[y][x]
                        if (char in ascii_uppercase) and (char != target):
                            requirements.add(char)
                    self.order[target] = requirements

    def is_done(self):
        if len(self.inventory) < self.size:
            return False
        return True

    def possible_moves(self):
        moves = []
        for target in ascii_lowercase:
            if target not in self.order:
                continue
            requirements = self.order[target]
            if ((requirements & self.opened_doors) == requirements) and (target not in self.history):
                moves.append(target)
        return moves

    def move(self, target):
        self.inventory.add(target)
        self.opened_doors.add(target.upper())
        for t in self.distances[target]:
            if t in '1234':
                self.distance_traveled += self.distances[self.drones[t]][target]
                self.drones[t] = target
        self.history.append(target)

    def reset(self):
        self.history = ['@']
        self.inventory = set()
        self.opened_doors = set()
        self.distance_traveled = 0
