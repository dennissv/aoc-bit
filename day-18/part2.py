#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 16:15:59 2019

@author: dennis
"""

import random
import time

from SimpleNavigator2 import SimpleNavigator

with open('data/part2_mod.txt', 'r') as f:
    grid = [row.strip('\n') for row in f.readlines()]
nav = SimpleNavigator(grid)

solution = 'pkaztbfxecsuvowdmhlqjnrgyi'

for action in solution:
    nav.move(action)
print(nav.distance_traveled)

#results = []
#while True:
#    while not nav.is_done():
#        nav.move(random.choice(nav.possible_moves()))
#    results.append((nav.distance_traveled, nav.history[1:]))
#    nav.reset()
#    if not len(results)%10000:
#        print('Simulated {} results'.format(len(results)))
'pkatbecxsuvowdlfjqzhmnrgyi'

#queue = ['@pkaztbfxecsuvowdmhlqjnrgyi']
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