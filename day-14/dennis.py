#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:21:54 2019

@author: dennis
"""

import re
import math
from dataclasses import dataclass


@dataclass
class Chemical:
    name: str
    quantity: int


def ore_required(fuel):
    targets = [Chemical('FUEL', fuel)]
    ore_used = 0
    inventory = {chemical: 0 for chemical in reactions}
    while targets:
        todo_list = []
        for target in targets:
            if target.name == 'ORE':
                ore_used += target.quantity
                continue
            saved = min(inventory[target.name], target.quantity)
            inventory[target.name] -= saved
            target.quantity -= saved
            batches = math.ceil(target.quantity/reaction_sums[target.name])
            produced = batches*reaction_sums[target.name]
            inventory[target.name] += produced - target.quantity
            todo = reactions[target.name]
            for reactant in todo:
                todo_list.append(Chemical(reactant.name, reactant.quantity*batches))
        targets = todo_list.copy()
    return ore_used

def is_solution(fuel):
    if (ore_required(fuel) < max_ore) and (ore_required(fuel+1) > max_ore):
        return True
    return False

reactions = dict()
reaction_sums = dict()
with open('data/input.txt', 'r') as f:
    for line in f.readlines():
        reg = re.findall(r'\d+\s[A-Z]+', line)
        target = reg[-1].split(' ')
        reaction_sums[target[-1]] = int(target[0])
        reactions[target[-1]] = [Chemical(x.split()[1], int(x.split()[0])) for x in reg[:-1]]

print('Part 1: ', ore_required(1))

# Binary search to solve part 2
max_ore = 1000000000000
exponent = 1
while ore_required(10**exponent) < max_ore:
    exponent += 1
interval = [10**(exponent-1), 10**exponent]
n_fuel = (interval[0]+interval[1])//2
while not is_solution(n_fuel):
    if ore_required(n_fuel) > max_ore:
        interval[1] = n_fuel
    else:
        interval[0] = n_fuel
    n_fuel = (interval[0]+interval[1])//2
print('Part 2: ', n_fuel)
