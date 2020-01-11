#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 16:26:30 2019

@author: dennis
"""

from navigator import Navigator
import random

def count_upper(s):
    return sum(x.isupper() for x in s)

with open('data/modified_input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]

results = []
#last_order = ['R', 'g', 'G', 'y', 'Y', 'i']
while True:
    nav = Navigator(grid)
    sequence = []
    while not nav.is_completed():
        unlockable_doors = nav.reachable_doors() & set(key.upper() for key in nav.inventory)
        reachables = list(nav.reachable_keys() | unlockable_doors)
        print(reachables)
        
        selected = random.choice(reachables)
#        while ((selected in last_order) and (len(nav.keys) > 3)) or \
#                ((selected.isupper() and selected != 'P') and (not count_upper(sequence))) or \
#                (selected.isupper() and (len(sequence) < 5)):
#            selected = random.choice(reachables)
        sequence.append(selected)
        if selected.isupper():
            nav.move(nav.doors[selected])
            nav.open_door(selected)
        else:
            nav.move(nav.keys[selected])
            nav.loot_key(selected)
    print(nav.distance_traveled)
    results.append((nav.distance_traveled, sequence))
    break
