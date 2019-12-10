#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:20:30 2019

@author: dennis
"""

from itertools import permutations
from IntcodeComputer import IntcodeComputer

with open('data/input.txt', 'r') as f:
    opcodes =[int(x) for x in f.readline().strip('\n').split(',')]

best_result = 0
for comb in permutations(range(5), 5):
    result = 0
    machines = []
    for i in range(5):
        machine = IntcodeComputer(opcodes.copy(), (comb[i], result))
        machines.append(machine)
        while machine.active:
            machine.step()
        result = machine.output
    if result > best_result:
        best_result = result
print('Part 1: {}'.format(best_result))

best_result = 0
step_count = 0
for comb in permutations(range(5, 10), 5):
    result = 0
    machines = []
    for i in range(5):
        machine = IntcodeComputer(opcodes.copy(), (comb[i], result))
        machines.append(machine)
        while not machine.awaiting_input:
            machine.step()
        result = machine.get_output()
        step_count += 1
    i = 0
    machines[0].input_queue.append(result)
    while machines[4].active:
        machine = machines[i]
        machine.step()
        while not machine.awaiting_input:
            machine.step()
            if machine.output_queue:
                machines[(i+1)%5].input_queue.append(machine.get_output())
            if not machine.active:
                break
        i += 1
        i %= 5
        step_count += 1
    end_result = machines[4].output
    if end_result > best_result:
        best_result = end_result
print('Part 2: {}'.format(best_result))
