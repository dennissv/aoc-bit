#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 10:51:51 2019

@author: dennis
"""

with open('data/input.txt', 'r') as f:
    data = [int(line) for line in f.readlines()]

print("Part 1: {}".format(sum([int(fuel/3)-2 for fuel in data])))

def tot_fuel(fuel):
    curr_fuel = int(fuel/3)-2
    if curr_fuel > 0:
        return curr_fuel + tot_fuel(curr_fuel)
    return 0

print("Part 2: {}".format(sum([tot_fuel(fuel) for fuel in data])))
