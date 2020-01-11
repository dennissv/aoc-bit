#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 15:32:33 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode

opcodes = read_opcode('data/input.txt')

grid = [['.' for i in range(50)] for j in range(50)]
results = []
for i in range(50):
    for j in range(50):
        computer = IntcodeComputer(opcodes.copy(), [i, j])
        while computer.active:
            computer.step()
        results.append((computer.output, (i, j)))
        if computer.output:
            grid[i][j] = '#'

results.sort(reverse=True)
print('Part 1:', sum(x[0] for x in results))

def fits(positions):
    first = positions[0]
    last = positions[99]
    if (first[1]-100) >= last[0]:
        return True
    return False

y = 1500
x = 1200
result = 1
last_hundred = []
while True:
    first = True
    while True:
        computer = IntcodeComputer(opcodes.copy(), [x, y])
        while computer.active:
            computer.step()
        result = computer.output
        if first and result:
            first = False
            start = x
        elif not first and not result:
            end = x
            break
        x += 1
    last_hundred.append((start, end))
    last_hundred = last_hundred[-100:]
    y += 1
    x = start
    if len(last_hundred) < 100:
        continue
    if fits(last_hundred):
        break

print('Part 2:', ((last_hundred[0][1]-100)*10000+y-100))
