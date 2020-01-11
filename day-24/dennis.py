#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 12:59:03 2019

@author: dennis
"""

from copy import deepcopy

def adjacent_count(y, x):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == j) or ((abs(i)+abs(j)) > 1) or not (0 <= y+i <= 4) or not (0 <= x+j <= 4):
                continue
            count += (grid[y+i][x+j] == '#')
    return count

def biodiversity(grid):
    rating = 0
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == '#':
                rating += 2**(j+i*5)
    return rating

def print_grid():
    for row in grid:
        print(''.join(row))

with open('data/input.txt', 'r') as f:
    grid = [[char for char in row.strip()] for row in f.readlines()]

seen = set()
while True:
    new_grid = [['' for _ in range(5)] for _ in range(5)]
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            count = adjacent_count(i, j)
            if (char == '#') and (adjacent_count(i, j) != 1):
                new_grid[i][j] = '.'
            elif (char == '.') and (adjacent_count(i, j) in range(1, 3)):
                new_grid[i][j] = '#'
            else:
                new_grid[i][j] = char
    grid = new_grid.copy()
    rating = biodiversity(grid)
    if rating in seen:
        break
    seen.add(rating)

print('Part 1:', rating)


def recursive_count(y, x, level):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == j) or ((abs(i)+abs(j)) > 1):
                continue
            elif (y+i < 0):
                count += recursive_grid[level-1][1][2] == '#'
            elif (y+i > 4):
                count += recursive_grid[level-1][3][2] == '#'
            elif (x+j < 0):
                count += recursive_grid[level-1][2][1] == '#'
            elif (x+j > 4):
                count += recursive_grid[level-1][2][3] == '#'
            elif (y+i) == (x+j) == 2:
                if (y == 2) and (x == 1):
                    count += sum(recursive_grid[level+1][row][0] == '#' for row in range(5))
                elif (y == 2) and (x == 3):
                    count += sum(recursive_grid[level+1][row][4] == '#' for row in range(5))
                elif (y == 1) and (x == 2):
                    count += sum(recursive_grid[level+1][0][column] == '#' for column in range(5))
                elif (y == 3) and (x == 2):
                    count += sum(recursive_grid[level+1][4][column] == '#' for column in range(5))
            else:
                count += (recursive_grid[level][y+i][x+j] == '#')
    return count

with open('data/input.txt', 'r') as f:
    grid = [[char for char in row.strip()] for row in f.readlines()]
grid[2][2] = '?'

empty_grid = [['.' for _ in range(5)] for _ in range(5)]
empty_grid[2][2] = '?'

recursive_grid = {i: empty_grid.copy() for i in range(-101, 102)}
recursive_grid[0] = grid.copy()

for generation in range(200):
    new_recursive_grid = {i: empty_grid.copy() for i in range(-101, 102)}
    for level in range(-(generation//2)-1, (generation//2)+2):
        new_grid = [['.' for _ in range(5)] for _ in range(5)]
        for i, row in enumerate(recursive_grid[level]):
            for j, char in enumerate(row):
                if (i == j == 2):
                    continue
                count = recursive_count(i, j, level)
                if (char == '#') and (count != 1):
                    new_grid[i][j] = '.'
                elif (char == '.') and (count in range(1, 3)):
                    new_grid[i][j] = '#'
                else:
                    new_grid[i][j] = char
        new_recursive_grid[level] = new_grid.copy()
    recursive_grid = deepcopy(new_recursive_grid)

bugs = 0
for grid in recursive_grid.values():
    bugs += sum(sum(char == '#' for char in row) for row in grid)

print('Part 2:', bugs)
