#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 17:00:40 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer

with open('data/input.txt', 'r') as f:
    opcodes = [int(x) for x in f.readlines()[0].strip('\n').split(',')]

machine = IntcodeComputer(opcodes, [1])
while machine.active:
    machine.step()
print('Part 1: {}'.format(machine.output))

machine = IntcodeComputer(opcodes, [2])
while machine.active:
    machine.step()
print('Part 2: {}'.format(machine.output))
