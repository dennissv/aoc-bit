#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:03:41 2019

@author: dennis
"""

import time
from string import ascii_lowercase
from string import ascii_uppercase

from tqdm import tqdm
import pygame
import networkx as nx

from SimpleNavigator import SimpleNavigator

with open('data/input.txt', 'r') as f:
    grid = [row.strip('\n') for row in f.readlines()]
nav = SimpleNavigator(grid)

solution = 'pkatbxecsuvowdlzfqjmhnrgyi'

pygame.init()

TEXT_COLOR = pygame.Color('#cccccc')
BACKGROUND_COLOR = pygame.Color('#0f0f23')
GRAPH_COLOR = pygame.Color('#00cc00')
BODY_COLOR = pygame.Color('#ffff66')
OBJECT_COLORS = {'floor': BACKGROUND_COLOR,
                 'player': pygame.Color('#ffff66'),
                 'wall': pygame.Color('#00cc00'),
                 'end': pygame.Color('#cccccc')}
SCREEN_WIDTH = 810
SCREEN_HEIGHT = 870
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()
myfont = pygame.font.Font("Source_Code_Pro/SourceCodePro-Regular.ttf", 10)
inventoryfont = pygame.font.Font("Source_Code_Pro/SourceCodePro-Regular.ttf", 22)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def init_draw():
    screen.fill(OBJECT_COLORS['floor'])
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == '#':
                pygame.draw.rect(screen, OBJECT_COLORS['wall'], (x*10, y*10, 10, 10), 0)
            elif char == '.':
                pygame.draw.rect(screen, OBJECT_COLORS['floor'], (x*10, y*10, 10, 10), 0)
            elif char in ascii_lowercase:
                textsurface = myfont.render(char, False, OBJECT_COLORS['player'])
                screen.blit(textsurface, (x*10+2, y*10-2))
            elif char in ascii_uppercase:
                pygame.draw.rect(screen, (139, 0, 0, 255), (x*10, y*10, 10, 10), 0)
                textsurface = myfont.render(char, False, OBJECT_COLORS['player'])
                screen.blit(textsurface, (x*10+2, y*10-2))
    textsurface = inventoryfont.render('Keys: {}'.format(''.join(nav.history[1:])), False, OBJECT_COLORS['player'])
    screen.blit(textsurface, (200, 810))
    pygame.display.update()

grid = [[char for char in row] for row in grid]
init_draw()

steps = 0
for action in solution:
    path = nx.astar_path(nav.g, nav.positions[nav.history[-1]], nav.positions[action])
    for block in path:
        y, x = block
        pygame.draw.rect(screen, (192, 255, 62, 255), (x*10, y*10, 10, 10), 0)
        pygame.draw.rect(screen, OBJECT_COLORS['floor'], (385, 840, 200, 30), 0)
        textsurface = inventoryfont.render('Steps: {}'.format(steps), False, OBJECT_COLORS['player'])
        screen.blit(textsurface, (320, 840))
        pygame.display.update()
        time.sleep(.01)
        steps += 1
    nav.move(action)
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char.lower() in nav.inventory:
                grid[i][j] = '.'
    steps -= 1
    time.sleep(.1)
    init_draw()
pygame.draw.rect(screen, OBJECT_COLORS['floor'], (385, 840, 200, 30), 0)
textsurface = inventoryfont.render('Steps: {}'.format(steps), False, OBJECT_COLORS['player'])
screen.blit(textsurface, (320, 840))
pygame.display.update()

#steps = 0
#path = nx.astar_path(g2, (0, start[0], start[1]), (0, end[0], end[1]))
#for i, edge in enumerate(path[0:-1:2]):
#    screen.fill((0, 0, 0))
#    init_draw()
#    recursion_level, y1, x1 = edge
#    _, y2, x2 = path[i*2+1]
#    textsurface = myfont.render('Recursion level {}'.format(recursion_level), False, OBJECT_COLORS['player'])
#    screen.blit(textsurface, (330, 400))
#    for pixel in nx.astar_path(g3, (y1, x1), (y2, x2))[1:-1]:
#        pygame.draw.rect(screen, OBJECT_COLORS['player'], (pixel[1]*8, pixel[0]*8, 8, 8), 0)
#        pygame.display.update()
##        time.sleep(.02)
##        pygame.image.save(screen, "recording/{}.png".format(str(steps).zfill(5)))
#        steps += 1

