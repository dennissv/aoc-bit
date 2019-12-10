#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:28:22 2019

@author: dennis
"""

import numpy as np

def rad_to_deg(a):
    return a*(180/np.pi)

def diff_to_deg(dx, dy):
    with np.errstate(divide='ignore'):
        if (dx >= 0) and (dy >= 0):
            angle = 90-rad_to_deg(np.arctan(dy/dx))
        elif (dx >= 0) and (dy <= 0):
            angle = 90+rad_to_deg(np.arctan(abs(dy/dx)))
        elif (dx <= 0) and (dy <= 0):
            angle = 270-rad_to_deg(np.arctan(abs(dy/dx)))
        elif (dx <= 0) and (dy >= 0):
            angle = 270+rad_to_deg(np.arctan(abs(dy/dx)))
    return angle

grid = []
with open('data/input.txt', 'r') as f:
    grid = [[int(x == '#') for x in line.strip('\n')] for line in f.readlines()]
grid = np.array(grid)

asteroids = np.where(grid == 1)
asteroids = [(asteroids[0][i], asteroids[1][i]) for i in range(asteroids[0].size)]

all_angles =  []
for op_pos in asteroids:
    angles = set()
    for a_pos in asteroids:
        if op_pos == a_pos:
            continue
        angles.add(diff_to_deg(op_pos[1]-a_pos[1], op_pos[0]-a_pos[0]))
    all_angles.append((len(angles), op_pos))
all_angles.sort()
print('Part 1: {}'.format(all_angles[-1][0]))

p = all_angles[-1][-1]
a_l = [(diff_to_deg(a_pos[1]-p[1], p[0]-a_pos[0]), abs(a_pos[1]-p[1])+abs(p[0]-a_pos[0]), a_pos)
       for a_pos in asteroids if a_pos != p]
a_l.sort()

destroyd = []
while a_l:
    ld = -1
    to_remove = []
    for x in a_l:
        if x[0] != ld:
            destroyd.append(x[2])
            ld = x[0]
            to_remove.append(x)
    for x in to_remove:
        a_l.remove(x)

target = destroyd[199]
print('Part 2: {}'.format(target[1]*100+target[0]))
