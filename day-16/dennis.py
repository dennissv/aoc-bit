#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 00:13:00 2019

@author: dennis
"""

import numpy as np
from tqdm import tqdm

def get_pattern(n, length):
    pattern = []
    while len(pattern) < length+1:
        pattern += [0]*n+[1]*n+[0]*n+[-1]*n
    pattern = pattern[1:length+1]
    return np.int8(pattern)

def last_digit(n):
    return int(str(n)[-1])

def part1(signal):
    patterns = np.int8([get_pattern(n, len(signal)) for n in range(1, len(signal)+1)])
    for _ in range(100):
        signal = np.int8([last_digit(np.sum(x)) for x in signal*patterns])
    return ''.join(str(x) for x in signal[:8])

def part2(signal):
    for _ in tqdm(range(100)):
        sum_ = 0
        for i in range(1, len(signal)+1):
            sum_ += signal[-i]
            signal[-i] = last_digit(sum_)
    return ''.join(str(x) for x in signal[:8])

with open('data/input.txt', 'r') as f:
    BASE_SIGNAL = [int(x) for x in f.readline().strip('\n')]
OFFSET = int(''.join(str(x) for x in BASE_SIGNAL[:7]))

ANS1 = part1(BASE_SIGNAL)
PART2_SIGNAL = (BASE_SIGNAL*10000)[OFFSET:]
ANS2 = part2(PART2_SIGNAL)

print()
print('Part 1:', ANS1)
print('Part 2:', ANS2)
