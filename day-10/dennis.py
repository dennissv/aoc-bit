#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:28:22 2019

@author: dennis
"""

import numpy as np

def diff_to_deg(d1, d2):
    return (2*np.pi+np.arctan2(d1[1]-d2[1], d2[0]-d1[0]))%(2*np.pi)

grid = []
with open('data/input.txt', 'r') as f:
    grid = np.array([[int(x == '#') for x in line.strip('\n')] for line in f.readlines()])
asteroids = np.argwhere(grid == 1).tolist()

all_angles = [{diff_to_deg(asteroids[i], asteroids[j]) for j in range(len(asteroids))}
              for i in range(len(asteroids))]
reached = [(len(x), asteroids[i]) for i, x in enumerate(all_angles)]
reached.sort()
print('Part 1: {}'.format(reached[-1][0]))


p = reached[-1][-1]
asteroid_list = [(diff_to_deg(a_pos, p), abs(a_pos[1]-p[1])+abs(p[0]-a_pos[0]), a_pos)
       for a_pos in asteroids if a_pos != p]
asteroid_list.sort()

destroyd = []
while asteroid_list:
    destroyed_this_cycle = set()
    to_remove = []
    for asteroid in asteroid_list:
        if asteroid[0] not in destroyed_this_cycle:
            destroyd.append(asteroid[2])
            destroyed_this_cycle.add(asteroid[0])
            to_remove.append(asteroid)
    for asteroid in to_remove:
        asteroid_list.remove(asteroid)
target = destroyd[199]
print('Part 2: {}'.format(target[1]*100+target[0]))
