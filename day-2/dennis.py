#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 10:51:51 2019

@author: dennis
"""

def run(opcodes):
    for i in range(0, len(opcodes), 4):
        command = opcodes[i]
        if command == 1:
            opcodes[opcodes[i+3]] = opcodes[opcodes[i+1]]+opcodes[opcodes[i+2]]
        elif command == 2:
            opcodes[opcodes[i+3]] = opcodes[opcodes[i+1]]*opcodes[opcodes[i+2]]
        elif command == 99:
            return opcodes[0]

with open('data/input.txt', 'r') as f:
    opcodes =[int(x) for x in f.readline().strip('\n').split(',')]

opcodes_part1 = opcodes.copy()
opcodes_part1[1] = 12
opcodes_part1[2] = 2
print("Part 1: {}".format(run(opcodes_part1)))

for i in range(120):
    for j in range(120):
        opcodes_part2 = opcodes.copy()
        opcodes_part2[1] = i
        opcodes_part2[2] = j
        if  run(opcodes_part2) == 19690720:
            print("Part 2: {}".format((i*100)+j))
