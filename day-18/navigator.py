#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:20:01 2019

@author: dennis
"""

from dataclasses import dataclass
from string import ascii_lowercase
from string import ascii_uppercase

import networkx as nx

@dataclass
class Position:
    x: int
    y : int

def _pos_from_flat(i):
    return Position(i%81, i//81)

class Navigator():
    
    def __init__(self, grid):
        self.position = Position(y=40, x=40)
        self.grid = [[char for char in row] for row in grid]
        flat = ''.join(grid)
        self.keys = {char: _pos_from_flat(flat.find(char)) for char in ascii_lowercase}
        self.doors = {char: _pos_from_flat(flat.find(char)) for char in ascii_uppercase}
        for char in 'FINOSUZ':
            del self.doors[char]
        self.inventory = set()
        self.distance_traveled = 0
        self._build_graph()

    def _build_graph(self):
        self.graph = nx.Graph()
        to_check = [(self.position.y, self.position.x)]
        self.visited = set()
        while to_check:
            new_check = []
            for node in to_check:
                neighbours, door = self._valid_neighbours(node)
                for neighbour in neighbours:
                    self.graph.add_edge(node, neighbour)
                    if neighbour not in self.visited:
                        new_check.append(neighbour)
                        self.visited.add(neighbour)
                    if door:
                        self.graph.add_edge(door, node)
                
            to_check = new_check
    
    def _update_graph(self):
        neighbours, door = self._valid_neighbours((self.position.y, self.position.x))
        for neighbour in neighbours:
            if neighbour not in self.visited:
                break
        to_check = [neighbour]
        while to_check:
            new_check = []
            for node in to_check:
                neighbours, door = self._valid_neighbours(node)
                for neighbour in neighbours:
                    self.graph.add_edge(node, neighbour)
                    if neighbour not in self.visited:
                        new_check.append(neighbour)
                        self.visited.add(neighbour)
                if door:
                    self.graph.add_edge(door, node)
            to_check = new_check
        

    def _valid_neighbours(self, node):
        valid = []
        door = None
        valid_chars = '.@'+ascii_lowercase
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (i == j) or ((abs(i)+abs(j)) > 1):
                    continue
                if self.grid[node[0]+i][node[1]+j] in valid_chars:
                    valid.append((node[0]+i, node[1]+j))
                elif self.grid[node[0]+i][node[1]+j] in ascii_uppercase:
                    door = (node[0]+i, node[1]+j)
        return valid, door

    def _build_graph_all(self):
        self.graph = nx.Graph()
        to_check = [(self.position.y, self.position.x)]
        visited = set()
        while to_check:
            new_check = []
            for node in to_check:
                neighbours = self._valid_neighbours_all(node)
                for neighbour in neighbours:
                    self.graph.add_edge(node, neighbour)
                    if neighbour not in visited:
                        new_check.append(neighbour)
                        visited.add(neighbour)
            to_check = new_check

    def _valid_neighbours_all(self, node):
        valid = []
        valid_chars = '.@'+ascii_lowercase+ascii_uppercase
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (i == j) or ((abs(i)+abs(j)) > 1):
                    continue
                if self.grid[node[0]+i][node[1]+j] in valid_chars:
                    valid.append((node[0]+i, node[1]+j))
        return valid
            
    def is_reachable(self, node):
        if (node[0], node[1]) in self.graph.nodes:
            if nx.has_path(self.graph, (self.position.y, self.position.x), (node[0], node[1])):
                return True
        return False
    
    def has_path(self, node):
        if (node.y, node.x) in self.graph.nodes:
            if nx.has_path(self.graph, (self.position.y, self.position.x), (node.y, node.x)):
                return True
        return False

    def reachable_keys(self):
        reachable = set()
        for key, pos in self.keys.items():
            if self.has_path(pos):
                reachable.add(key)
        return reachable

    def reachable_doors(self):
        reachable = set()
        for name, door in self.doors.items():
            if self.is_reachable((door.y-1, door.x)):
                reachable.add(name)
                self.graph.add_edge((door.y-1, door.x), (door.y, door.x))
            elif self.is_reachable((door.y+1, door.x)):
                reachable.add(name)
                self.graph.add_edge((door.y+1, door.x), (door.y, door.x))
            elif self.is_reachable((door.y, door.x-1)):
                reachable.add(name)
                self.graph.add_edge((door.y, door.x-1), (door.y, door.x))
            elif self.is_reachable((door.y, door.x+1)):
                reachable.add(name)
                self.graph.add_edge((door.y, door.x+1), (door.y, door.x))
                
        return reachable

    def loot_key(self, key):
        self.inventory.add(key)
        _ = self.keys.pop(key)

    def open_door(self, door):
        door = self.doors.pop(door)
        self.grid[door.y][door.x] = '.'
        self._update_graph()
    
    def is_completed(self):
        if len(self.inventory) == len(ascii_lowercase):
            return True
        return False
    
    def move(self, node):
        self.distance_traveled += self.distance(node)
        self.position.x = node.x
        self.position.y = node.y
    
    def distance(self, node):
        return nx.astar_path_length(self.graph, (self.position.y, self.position.x), (node.y, node.x))
