#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 22:17:30 2019

@author: dennis
"""

from copy import deepcopy

from navigator import Navigator
from mcts import mcts

class NavigatorMCTS():
    
    def __init__(self, grid):
        self.nav = Navigator(grid)
    
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
        return newState

    def isTerminal(self):
        ''' Returns whether this state is a terminal state'''
        return self.nav.is_completed()

    def getReward(self):
        ''' Returns the reward for this state. Only needed for terminal states.'''
        return self.nav.distance_traveled

with open('data/modified_input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]


state = NavigatorMCTS(grid)
mcts = mcts(timeLimit=10000)
while not state.isTerminal():
    action = mcts.search(initialState=state)
    state = state.takeAction(action)
    print(action)
print(state.getReward())
