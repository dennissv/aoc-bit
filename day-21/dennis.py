#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 15:32:33 2019

@author: dennis
"""

from itertools import permutations

from tqdm import tqdm

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode

def assembly(li):
    s = '\n'.join(li)+'\n'
    return [ord(x) for x in s]

def read(s):
    return ''.join(chr(x) for x in s)

def create_valid_commands():
    valid_commands = []
    for start in ['NOT', 'OR', 'AND']:
        for r1 in 'ABCDJT':
            for r2 in 'JT':
                if r1 == r2:
                    continue
                valid_commands.append(' '.join((start, r1, r2)))
    return valid_commands

def find_answer():
    for i in range(16):
        for perm in tqdm(permutations(valid_commands, i)):
            instructions = list(perm)+['AND D J', 'WALK']
            computer = IntcodeComputer(opcodes.copy(), assembly(instructions))
            while computer.active:
                computer.step()
            if computer.output > 255:
                return computer.output, instructions
        print(i)

opcodes = read_opcode('data/input.txt')
valid_commands = create_valid_commands()
answer, instructions = find_answer()
print('Part 1:', answer)
print(instructions)

instructions = ['NOT C J', 'NOT B T', 'OR T J', 'NOT A T', 'OR T J', 'AND D J', 
                'NOT E T', 'NOT T T', 'OR H T', 'AND T J', 'RUN']
computer = IntcodeComputer(opcodes.copy(), assembly(instructions))
while computer.active:
    computer.step()
print('Part 2:', computer.output)
