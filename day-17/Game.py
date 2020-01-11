#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:49:05 2019

@author: dennis
"""

import pygame
from dataclasses import dataclass
import time
import networkx as nx

pygame.init()
TEXT_COLOR = pygame.Color('#cccccc')
BACKGROUND_COLOR = pygame.Color('#0f0f23')
GRAPH_COLOR = pygame.Color('#00cc00')
BODY_COLOR = pygame.Color('#ffff66')
OBJECT_COLORS = {'empty': BACKGROUND_COLOR,
                 'player': pygame.Color('#ffff66'),
                 'wall': pygame.Color('#00cc00'),
                 'end': pygame.Color('#cccccc')}

@dataclass
class Object:
    x: int
    y: int
    type_: str

                                  
class Game():
    
    def __init__(self, record_flag=False):
        self.record_flag = record_flag
        self.player = Object(50, 50, 'player')
        self.objects = []
        self.steps = 0
        self.done = False
        self.answer = None
        self.solution = None
        self.walls = set()
        self.oxygen = set()
        self.visited = {(self.player.x, self.player.y)}
        self._init_draw()
        self._init_graph()

    def _init_graph(self):
        self.graph = nx.Graph()
        self.graph.add_edges_from([((self.player.x, self.player.y), (self.player.x+1, self.player.y)),
                                   ((self.player.x, self.player.y), (self.player.x-1, self.player.y)),
                                   ((self.player.x, self.player.y), (self.player.x, self.player.y+1)),
                                   ((self.player.x, self.player.y), (self.player.x, self.player.y-1))])
        self.to_test = [(50, 51), (50, 49), (51, 50), (49, 50)]

    def _init_draw(self):
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.font.init()
        self.myfont = pygame.font.Font("Source_Code_Pro/SourceCodePro-Regular.ttf", 20)
        if self.record_flag:
            self.images = []

    def get_move(self, pos1, pos2):
        if pos2[0] == pos1[0]:
            if pos2[1] == (pos1[1]+1):
                return 2
            elif pos2[1] == (pos1[1]-1):
                return 1
        elif pos2[1] == pos1[1]:
            if pos2[0] == (pos1[0]-1):
                return 3
            elif pos2[0] == (pos1[0]+1):
                return 4

    def get_path(self, position):
        return nx.astar_path(self.graph, (self.player.x, self.player.y), position)

    def move(self, action, result):
        curr_pos = (self.player.x, self.player.y)
        self.visited.add(curr_pos)
        if result == 0:
            if action == 1:
                c = (self.player.x, self.player.y-1)
                self.objects.append(Object(self.player.x, self.player.y-1, 'wall'))
            elif action == 2:
                c = (self.player.x, self.player.y+1)
                self.objects.append(Object(self.player.x, self.player.y+1, 'wall'))
            elif action == 3:
                c = (self.player.x-1, self.player.y)
                self.objects.append(Object(self.player.x-1, self.player.y, 'wall'))
            elif action == 4:
                c = (self.player.x+1, self.player.y)
                self.objects.append(Object(self.player.x+1, self.player.y, 'wall'))
            self.walls.add(c)

        elif result == 1:
            self.objects.append(Object(self.player.x, self.player.y, 'empty'))
            if action == 1:
                self.player.y -= 1
            elif action == 2:
                self.player.y += 1
            elif action == 3:
                self.player.x -= 1
            elif action == 4:
                self.player.x += 1
            c = (self.player.x, self.player.y)
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x == y) or (x and y):
                        continue
                    pos = (self.player.x+x, self.player.y+y)
                    if pos not in self.visited:
                        self.to_test.append(pos)
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x == y) or (x and y):
                        continue
                    pos = (self.player.x+x, self.player.y+y)
                    if pos not in self.walls:
                        self.graph.add_edge((self.player.x, self.player.y), pos)

        elif result == 2:
            self.objects.append(Object(self.player.x, self.player.y, 'empty'))
            if action == 1:
                self.player.y -= 1
            elif action == 2:
                self.player.y += 1
            elif action == 3:
                self.player.x -= 1
            elif action == 4:
                self.player.x += 1
            self.visited.add((self.player.x, self.player.y-1))
            self.done = True
            c = (self.player.x, self.player.y)
            self.answer = c

        self.visited.add(c)
        if c in self.to_test:
            self.to_test.remove(c)

    def oxygen_fill(self):
        self.oxygen = {self.answer}
        rooms = len([x for x in self.graph.nodes if x not in self.walls])
        steps = 0
        while len(self.oxygen) < rooms:
            to_add = []
            for pos in self.oxygen:
                for x in self.graph.edges(pos):
                    for y in x:
                        if (y not in self.walls) and (y != pos):
                            to_add.append(y)
            for add in to_add:
                self.oxygen.add(add)
            steps += 1
        return steps

    def draw(self):
        self.screen.fill((0, 0, 0))
        for object_ in self.objects:
            pygame.draw.rect(self.screen, OBJECT_COLORS[object_.type_], (object_.x*10, object_.y*10, 10, 10), 0)
        pygame.draw.rect(self.screen, OBJECT_COLORS['player'], (self.player.x*10, self.player.y*10, 10, 10), 0)
        pygame.display.update()
        self.steps += 1
        if self.record_flag:
            pygame.image.save(self.screen, "recording/{}.png".format(str(self.steps).zfill(5)))
            if self.done:
                for c in range(180):
                    pygame.image.save(self.screen, "recording/{}_{}.png".format(str(self.steps).zfill(5), str(c).zfill(3)))

    def draw_solution(self):
        self.solution = nx.astar_path(self.graph, (50, 50), self.answer)
        for pos in self.solution:
            pygame.draw.rect(self.screen, (255, 0, 0), (pos[0]*10, pos[1]*10, 10, 10), 0)
            pygame.display.update()
            time.sleep(.1)

    def get_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        return 1
                    elif event.key == pygame.K_s:
                        return 2
                    elif event.key == pygame.K_a:
                        return 3
                    elif event.key == pygame.K_d:
                        return 4
            time.sleep(.001)
