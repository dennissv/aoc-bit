#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 15:58:37 2019

@author: dennis
"""

from string import ascii_uppercase

import networkx as nx

def neighbour_char(i, j):
    relevant = False
    for y in range(-1, 2):
        for x in range(-1, 2):
            if (abs(y)+abs(x) == 1):
                if grid[i+y][j+x] in ascii_uppercase:
                    pos = (i+y, j+x)
                elif grid[i+y][j+x] == '.':
                    relevant = True
    return pos, relevant

def name(pos1, pos2):
    y1, x1 = pos1
    y2, x2 = pos2
    if (y1 < y2) or (x1 < x2):
        return grid[y1][x1]+grid[y2][x2]
    return grid[y2][x2]+grid[y1][x1]

def find_exit(pos):
    i, j = pos
    for y in range(-1, 2):
        for x in range(-1, 2):
            if (abs(y)+abs(x) == 1):
                if grid[i+y][j+x] == '.':
                    return (i+y, j+x)

def find_neighbours(pos):
    i, j = pos
    neighbours = []
    for y in range(-1, 2):
        for x in range(-1, 2):
            if (abs(y)+abs(x) == 1):
                if (grid[i+y][j+x] in '.'+ascii_uppercase):
                    neighbours.append((i+y, j+x))
    return neighbours

def is_inner(pos):
    if (pos[0] in range(26, 80)) and (pos[1] in range(26, 85)):
        return True
    return False

with open('data/input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]

portals = dict()
for i, row in enumerate(grid[1:-1]):
    for j, char in enumerate(row[1:-1]):
        if char in ascii_uppercase:
            pos, relevant = neighbour_char(i+1, j+1)
            if relevant:
                portals[(i+1, j+1)] = name(pos, (i+1, j+1))

for pos, portal in portals.items():
    if portal == 'AA':
        start = find_exit(pos)
    if portal == 'ZZ':
        end = pos

g = nx.Graph()
for start_pos, start_portal in portals.items():
    visited = {start_pos}
    queue = [find_exit(start_pos)]
    steps = 0
    while queue:
        new_queue = []
        for node in queue:
            visited.add(node)
            if node in portals:
                g.add_edge(start_pos, node, weight=steps-1)
                g.add_edge(node, start_pos, weight=steps-1)
                continue
            for neighbour in find_neighbours(node):
                if neighbour not in visited:
                    new_queue.append(neighbour)
        queue = new_queue
        steps += 1

op_portals = {value: key for key, value in portals.items()}
for pos1, portal1 in portals.items():
    for pos2, portal2 in portals.items():
        if pos1 == pos2:
            continue
        if (portal2 == portal1):
            g.add_edge(pos1, pos2)
            g.add_edge(pos2, pos1)

print(nx.astar_path_length(g, op_portals['AA'], op_portals['ZZ']))


g2 = nx.DiGraph()
recursion_depth = 50
for start_pos, start_portal in portals.items():
    visited = {start_pos}
    queue = [find_exit(start_pos)]
    steps = 0
    while queue:
        new_queue = []
        for node in queue:
            visited.add(node)
            if node in portals:
                for r in range(recursion_depth):
                    g2.add_edge((r, start_pos[0], start_pos[1]), (r, node[0], node[1]), weight=steps-1)
                    g2.add_edge((r, node[0], node[1]), (r, start_pos[0], start_pos[1]), weight=steps-1)
                continue
            for neighbour in find_neighbours(node):
                if neighbour not in visited:
                    new_queue.append(neighbour)
        queue = new_queue
        steps += 1

op_portals = {value: key for key, value in portals.items()}
for pos1, portal1 in portals.items():
    for pos2, portal2 in portals.items():
        if pos1 == pos2:
            continue
        if (portal2 == portal1):
            if is_inner(pos1):
                for r in range(recursion_depth):
                    g2.add_edge((r, pos1[0], pos1[1]), (r+1, pos2[0], pos2[1]))
            else:
                for r in range(1, recursion_depth):
                    g2.add_edge((r, pos1[0], pos1[1]), (r-1, pos2[0], pos2[1]))
start = op_portals['AA']
end = op_portals['ZZ']
print(nx.astar_path_length(g2, (0, start[0], start[1]), (0, end[0], end[1])))



import pygame
import random
import time

g3 = nx.Graph()
for start_pos, start_portal in portals.items():
    visited = {start_pos}
    queue = [find_exit(start_pos)]
    steps = 0
    while queue:
        new_queue = []
        for node in queue:
            visited.add(node)
            if node in portals:
                g.add_edge(start_pos, node)
                g.add_edge(node, start_pos)
                continue
            for neighbour in find_neighbours(node):
                if neighbour not in visited:
                    g3.add_edge(node, neighbour)
                    new_queue.append(neighbour)
        queue = new_queue
        steps += 1

pygame.init()

TEXT_COLOR = pygame.Color('#cccccc')
BACKGROUND_COLOR = pygame.Color('#0f0f23')
GRAPH_COLOR = pygame.Color('#00cc00')
BODY_COLOR = pygame.Color('#ffff66')
OBJECT_COLORS = {'floor': BACKGROUND_COLOR,
                 'player': pygame.Color('#ffff66'),
                 'wall': pygame.Color('#00cc00'),
                 'end': pygame.Color('#cccccc')}
TELEPORTER_COLORS = {char: pygame.Color(random.randint(20, 255), random.randint(50, 255), random.randint(30, 255)) for char in ascii_uppercase}
SCREEN_WIDTH = 872
SCREEN_HEIGHT = 840
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()
myfont = pygame.font.Font("Source_Code_Pro/SourceCodePro-Regular.ttf", 20)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def init_draw():
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == '#':
                pygame.draw.rect(screen, OBJECT_COLORS['wall'], (x*8, y*8, 8, 8), 0)
            elif char == '.':
                pygame.draw.rect(screen, OBJECT_COLORS['floor'], (x*8, y*8, 8, 8), 0)
            elif char in ascii_uppercase:
                pygame.draw.rect(screen, TELEPORTER_COLORS[char], (x*8, y*8, 8, 8), 0)
    pygame.display.update()

init_draw()

steps = 0
path = nx.astar_path(g2, (0, start[0], start[1]), (0, end[0], end[1]))
for i, edge in enumerate(path[0:-1:2]):
    screen.fill((0, 0, 0))
    init_draw()
    recursion_level, y1, x1 = edge
    _, y2, x2 = path[i*2+1]
    textsurface = myfont.render('Recursion level {}'.format(recursion_level), False, OBJECT_COLORS['player'])
    screen.blit(textsurface, (330, 400))
    r_color = pygame.Color(random.randint(20, 255), random.randint(0, 255), random.randint(30, 255))
    for pixel in nx.astar_path(g3, (y1, x1), (y2, x2))[1:-1]:
        pygame.draw.rect(screen, OBJECT_COLORS['player'], (pixel[1]*8, pixel[0]*8, 8, 8), 0)
        pygame.display.update()
#        time.sleep(.02)
#        pygame.image.save(screen, "recording/{}.png".format(str(steps).zfill(5)))
        steps += 1

#for c in range(180):
#    pygame.image.save(screen, "recording/{}_{}.png".format(str(steps).zfill(5), str(c).zfill(3)))
