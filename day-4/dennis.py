#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 13:09:26 2019

@author: dennis
"""

part_one = 0
part_two = 0
for i in range(234208, 765869+1):
    if (li := [int(x) for x in str(i)]) == sorted(li):
        counter = {li.count(x) for x in set(li)}
        part_one += bool({2, 3, 4, 5, 6} & counter)
        part_two += 2 in counter

print('Part 1: {}'.format(part_one))
print('Part 2: {}'.format(part_two))
