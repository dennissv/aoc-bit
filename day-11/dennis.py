#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 12:44:17 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer
import numpy as np

class Hullpainter():
    
    def __init__(self):
        self.grid = np.zeros((1000, 1000), np.uint8)
        self.position = (500, 500)
        self.direction = 0 # 0 = Up, 1 = Right, 2 = Down, 3 = Left
        self.direction_dict = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        self.coordinates_painted = set()
        self._paint(1)
    
    def step(self, paint_instruction, direction_instruction):
        self._paint(paint_instruction)
        self._change_direction(direction_instruction)
        self._move()
        
    def _change_direction(self, instruction):
        if instruction == 1:
            self.direction += 1
        elif instruction == 0:
            self.direction -= 1
        self.direction %= 4
    
    def _move(self):
        self.position = (self.position[0]+self.direction_dict[self.direction][0],
                         self.position[1]+self.direction_dict[self.direction][1])
    
    def _paint(self, instruction):
        self.grid[self.position[0], self.position[1]] = instruction
        self.coordinates_painted.add(self.position)
    
    def get_color(self):
        return self.grid[self.position[0], self.position[1]]


with open('data/input.txt', 'r') as f:
    instructions = [int(x) for x in f.readline().strip('\n').split(',')]

ic = IntcodeComputer(instructions, [0])
painter = Hullpainter()
while ic.active:
    if ic.awaiting_input:
        painter.step(ic.get_output(), ic.get_output())
        ic.input_queue.append(painter.get_color())
    ic.step()

print('Part 1: {}'.format(len(painter.coordinates_painted)))


ic = IntcodeComputer(instructions, [1])
painter = Hullpainter()
while ic.active:
    if ic.awaiting_input:
        painter.step(ic.get_output(), ic.get_output())
        ic.input_queue.append(painter.get_color())
    ic.step()
out = painter.grid[499:507, 500:541]
out = '\n'.join([''.join(['#' if x == 1 else '.' for x in row]) for row in out])
print('Part 2: ')
print(out)
