#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 19:33:28 2019

@author: dennis
"""

import networkx as nx

def resulting_pos(pos, direction):
    dict_ = {1: complex(1, 0), 2: complex(-1, 0), 3: complex(0, -1), 4: complex(0, 1)}
    return pos+dict_[direction]

class Game():

    def __init__(self, computer):
        self.graph = nx.Graph()
        self.position = complex(50, 50)
        self.computers = [computer]
        self.visited = set()

    def explore_block(self, computer):
        unexplored_blocks = []
        for action in range(1, 5):
            new_pos = resulting_pos(self.position, action)
            if new_pos in self.visited:
                continue
            self.visited.add(new_pos)
            result = self.move(computer, action)
            if result:
                unexplored_blocks.append(new_pos)
                self.graph.add_edge(self.position, new_pos)
                if action == 1:
                    _ = self.move(computer, 2)
                elif action == 2:
                    _ = self.move(computer, 1)
                elif action == 3:
                    _ = self.move(computer, 4)
                elif action == 4:
                    _ = self.move(computer, 3)
        return unexplored_blocks

    def step(self):
        for computer in self.computers:
            
                    


    def move(self, computer, action):
        computer.input_queue += [action]
        while not computer.awaiting_input:
            computer.step()
        return computer.output
