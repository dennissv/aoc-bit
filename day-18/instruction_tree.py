#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 22:17:30 2019

@author: dennis
"""

from copy import deepcopy
import time

from navigator import Navigator

class NavigatorSearch():
    
    def __init__(self, grid):
        self.nav = Navigator(grid)
        self.sequence = ''
    
    def getPossibleActions(self):
        ''' Returns an iterable of all actions which can be taken from this state'''
        unlockable_doors = self.nav.reachable_doors() & set(key.upper() for key in self.nav.inventory)
        return list(self.nav.reachable_keys() | unlockable_doors)

    def takeAction(self, action):
        ''' Returns the state which results from taking action action'''
        newState = deepcopy(self)
        if action.isupper():
            newState.nav.move(newState.nav.doors[action])
            newState.nav.open_door(action)
        else:
            newState.nav.move(newState.nav.keys[action])
            newState.nav.loot_key(action)
        newState.sequence += action
        return newState

    def isTerminal(self):
        ''' Returns whether this state is a terminal state'''
        return self.nav.is_completed()

    def getReward(self):
        ''' Returns the reward for this state. Only needed for terminal states.'''
        return self.nav.distance_traveled

def count_upper(s):
    return sum(x.isupper() for x in s)

with open('data/modified_input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]

base = NavigatorSearch(grid)
for action in 'zuspPbkBKecaECowdvWmhxAtXVlTfjLqQJMHDnrRgGyYi':
    base = base.takeAction(action)
print(base.getReward())

#tree = [NavigatorSearch(grid)]
#phase = 1
#results = []
#while tree:
#    start = time.time()
#    new_tree = []
#    for nav in tree:
#        if count_upper(nav.sequence):
#            continue
#        if phase == 5:
#            results.append((nav.getReward()+nav.nav.distance(nav.nav.doors['P']), nav.sequence))
#        actions = nav.getPossibleActions()
#        for action in actions:
#            new_tree.append(nav.takeAction(action))
#    tree = new_tree
#    end = time.time()
#    print(phase, end-start)
#    phase += 1
#    if phase == 6:
#        break
#results.sort()
#print(results[0][0], results[0][1])
