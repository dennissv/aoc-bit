#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 03:38:56 2019

@author: dennis
"""

from itertools import permutations

from tqdm import tqdm

from navigator import Navigator

with open('data/modified_input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]

def steps(instructions):
    nav = Navigator(grid)
    for instruction in instructions:
        unlockable_doors = nav.reachable_doors() & set(key.upper() for key in nav.inventory)
        reachables = list(nav.reachable_keys() | unlockable_doors)
        if instruction not in reachables:
            return 100000
        
        if instruction.isupper():
            nav.move(nav.doors[instruction])
            nav.open_door(instruction)
        else:
            nav.move(nav.keys[instruction])
            nav.loot_key(instruction)
    
    return nav.distance_traveled

variatons = 'k Ka B ce suEvCowd Wmhx At'.split(' ')
combs = list(permutations(variatons, len(variatons)))
start = 'zpPb'
end = 'XVlTfjLqQJMHDnrRgGyYi'

results = []
for comb in tqdm(combs):
    seq = start+''.join(comb)+end
    results.append((steps(seq), seq))

results.sort()
