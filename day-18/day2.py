#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:03:41 2019

@author: dennis
"""

import random
import time
from tqdm import tqdm

from SimpleNavigator import SimpleNavigator

with open('data/input.txt', 'r') as f:
    grid = [row.strip('\n') for row in f.readlines()]
nav = SimpleNavigator(grid)

solution = 'pkatbecxsuvowdlfjqzhmnrgyi'

#results = []
#while True:
#    while not nav.is_done():
#        nav.move(random.choice(nav.possible_moves()))
#    results.append((nav.distance_traveled, nav.history[1:]))
#    nav.reset()
#    if not len(results)%10000:
#        print('Simulated {} results'.format(len(results)))

#queue = ['@pkatbecxsuvow']
##seq_end = 'suvowdmhxlfjqnrgyi'
#seq_end = ''
#depth = 0
#end_results = []
#while queue:
#    start = time.time()
#    new_queue = []
#    for node in queue:
#        if len(node)+len(seq_end) == 27:
#            node += [x for x in seq_end]
#        for action in node[1:]:
#            if (action not in nav.possible_moves()) or (action in nav.history):
#                action = random.choice(nav.possible_moves())
#            nav.move(action)
#        if nav.is_done():
#            end_results.append((nav.distance_traveled, nav.history[1:]))
#            nav.reset()
#            continue
#        for possibility in nav.possible_moves():
#            new_queue.append(nav.history+[possibility])
#        nav.reset()
#    queue = new_queue
#    depth += 1
#    end = time.time()
#    print('Depth {} after {}s'.format(depth, end-start))
#end_results.sort()
#for i in range(5):
#    print(''.join(end_results[i][1]), end_results[i][0])
