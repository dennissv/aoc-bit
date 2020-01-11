#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 22:32:33 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode

import numpy as np
import networkx as nx

def is_intersection(y, x, grid):
    if grid[y][x] and grid[y-1][x] and grid[y+1][x] and grid[y][x-1] and grid[y]:
        return True
    return False

def turn(y, x, grid):
    if grid[y][x] and ((grid[y-1][x] or grid[y+1][x]) and (grid[y][x+1] or grid[y][x-1])) and \
        (not is_intersection(y, x, grid)):
        return True
    return False

def is_end(y, x, grid):
    if grid[y][x] and ((grid[y-1][x]+grid[y+1][x]+grid[y][x-1]+grid[y][x+1]) == 1):
        return True
    return False

def build_grid(chars):
    grid = [[0]*57]
    row = [0]
    letter_dict = {'.': 0, '#': 1, '^': 2, '>': 3, 'v': 4, '<': 5}
    for char in computer.output_queue:
        letter = chr(char)
        if letter == '\n':
            row.append(0)
            grid.append(row)
            row = [0]
        else:
            row.append(letter_dict[letter])
    grid = grid[:-1]
    grid.append([0]*57)
    return grid

def walk(grid, y, x, dy, dx):
    i = 1
    while value := np_grid[y+(i*dy), x+(i*dx)]:
        if value in (6, 7):
            return ((y+(i*dy), x+(i*dx)), i)
        i += 1
    return None

def build_graph(grid):
    g = nx.Graph()
    rows, columns = np.where(np_grid > 5)
    for y, x in zip(rows, columns):
        if node := walk(grid, y, x, 1, 0):
            g.add_edge((y, x), node[0], weight=node[1])
        if node := walk(grid, y, x, -1, 0):
            g.add_edge((y, x), node[0], weight=node[1])
        if node := walk(grid, y, x, 0, 1):
            g.add_edge((y, x), node[0], weight=node[1])
        if node := walk(grid, y, x, 0, -1):
            g.add_edge((y, x), node[0], weight=node[1])
    return g

def get_instruction(current_position, target_position, current_direction):
    # 0 = Up, 1 = Right, 2 = Down, 3 = Left
    curr_y, curr_x = current_position
    t_y, t_x = target_position
    direction_dict = {(-1, 0): 0, (1, 0): 2, (0, 1): 1, (0, -1): 3}
    new_direction = direction_dict[(min(max(-1, (t_y-curr_y)), 1),
                                   min(max(-1, (t_x-curr_x)), 1))]
    dist = str(abs(t_y-curr_y)+abs(t_x-curr_x))
    if (nd := ((current_direction-1)%4)) == new_direction:
        return ['L'+dist], nd
    elif (nd := ((current_direction+1)%4)) == new_direction:
        return ['R'+dist], nd
    elif (current_direction == new_direction):
        return dist, current_direction
    else:
        return ['R', 'R', dist], (new_direction+2)%4

opcodes = read_opcode('data/input.txt')
computer = IntcodeComputer(opcodes.copy(), [])

while computer.active:
    computer.step()

grid = build_grid(computer.output_queue)
sum_ = 0
for y, row in enumerate(grid[1:-1]):
    for x, point in enumerate(row[1:-1]):
        sum_ += (x)*(y)*is_intersection(y+1, x+1, grid)
print('Part 1:', sum_)


def is_solution(encoded, A, B, C):
    coverage = encoded.count(A)*len(A) + encoded.count(B)*len(B) + encoded.count(C)*len(C)
    if coverage == len(encoded):
        return True
    return False

def build_functions(encoded):
    li = []
    for a in range(5):
        A = encoded[:a+1]
        for b in range(1, 6):
            B = encoded[a+1:a+b+1]
            for c in range(1, 6):
                C = encoded[-c:]
                if is_solution(encoded, A, B, C):
                    return {A: 'A', B: 'B', C: 'C'}
    return None, None, None

def build_main_routine(encoded, functions):
    instruction = ''
    main_routine = ''
    for char in encoded:
        instruction += char
        if instruction in functions:
            main_routine += functions[instruction]
            instruction = ''
    return main_routine

def encode(instructions):
    codes = 'ABCDEFGHIKL'
    i = 0
    code_dict = dict()
    for instruction in instructions:
        if instruction not in code_dict:
            code_dict[instruction] = codes[i]
            i += 1
    encoded = [code_dict[instruction] for instruction in instructions]
    return ''.join(encoded), code_dict

def decode_main_routine(encoded):
    decoded = []
    for code in encoded:
        decoded.append(ord(code))
        decoded.append(ord(','))
    return decoded[:-1]+[10]

def decode_functions(functions, code_dict):
    code_dict = {v: k for k, v in code_dict.items()}
    decoded_functions = []
    for function in functions:
        for encoded_instruction in function:
            instruction = code_dict[encoded_instruction]
            decoded_functions.append(ord(instruction[0]))
            decoded_functions.append(ord(','))
            for number in instruction[1:]:
                decoded_functions.append(ord(number))
            decoded_functions.append(ord(','))
        decoded_functions = decoded_functions[:-1]+[10]
    return decoded_functions

np_grid = np.int8(grid)
for y, row in enumerate(grid[1:-1]):
    for x, point in enumerate(row[1:-1]):
        if turn(y+1, x+1, grid):
            np_grid[y+1, x+1] = 6
        if is_end(y+1, x+1, grid):
            np_grid[y+1, x+1] = 6
g = build_graph(np_grid)
p = list(nx.eulerian_path(g, source=(17, 27)))[::-1]
p = [(x[1], x[0]) for x in p]

instructions = []
direction = 0
for x in p:
    instruction, direction = get_instruction(x[0], x[1], direction)
    if type(instruction) == str:
        instructions[-1] = instructions[-1][0]+str(int(instructions[-1][1:])+int(instruction))
    else:
        instructions += instruction

encoded, code_dict = encode(instructions)
encoded_functions = build_functions(encoded)
main_routine = build_main_routine(encoded, encoded_functions)
machine_instructions = decode_main_routine(main_routine)
functions = decode_functions(encoded_functions, code_dict)
end = [110, 10]

part2_opcodes = opcodes.copy()
part2_opcodes[0] = 2

computer = IntcodeComputer(part2_opcodes, machine_instructions+functions+end)

steps = 0
while computer.active:
    if computer.awaiting_input:
        break
    computer.step()
    steps += 1
print('Part 2:', computer.output)
