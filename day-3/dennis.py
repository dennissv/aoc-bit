#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:14:47 2019

@author: dennis
"""

def walk(instructions):
    position = complex(0, 0)
    path = set()
    step_dict = dict()
    steps = 0
    for instruction in instructions:
        for _ in range(int(instruction[1:])):
            position += {'U': complex(0, 1), 'D': complex(0, -1), \
                         'R': complex(1, 0), 'L': complex(-1, 0)}[instruction[0]]
            path.add(position)
            steps += 1
            if position not in step_dict:
                step_dict[position] = steps
    return path, step_dict

with open('data/input.txt', 'r') as f:
    first_path, step_dict1 = walk(f.readline().strip('\n').split(','))
    second_path, step_dict2 = walk(f.readline().strip('\n').split(','))

print('Part 1: {}'.format(int(min(abs(p.real)+abs(p.imag) for p in first_path & second_path))))
print('Part 2: {}'.format(int(min(step_dict1[p]+step_dict2[p] for p in first_path & second_path))))
