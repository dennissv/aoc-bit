#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:49:05 2019

@author: dennis
"""

import pygame
pygame.init()
TEXT_COLOR = pygame.Color('#cccccc')
BACKGROUND_COLOR = pygame.Color('#0f0f23')
GRAPH_COLOR = pygame.Color('#00cc00')
BODY_COLOR = pygame.Color('#ffff66')
OBJECT_COLORS = (BACKGROUND_COLOR, pygame.Color('#ffff66'), pygame.Color('#00cc00'), pygame.Color('#cccccc'), (255,0,0))

class Object():
    
    def __init__(self, item):
        self.x = item[0]
        self.y = item[1]
        self.score = -1
        if (self.x, self.y) == (-1, 0):
            self.score = item[2]
            self.id = 5
        else:
            self.id = item[2]

class Game():
    
    def __init__(self, record_flag=False):
        self.record_flag = record_flag
        self._init_draw()
        self.objects = []
        self.blocks = 0
        self.action = 0
        self.ball_x = 0
        self.paddle_x = 0
        self.steps = 0
        
    def _init_draw(self):
        self.SCREEN_WIDTH = 720
        self.SCREEN_HEIGHT = 470
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.font.init()
        self.myfont = pygame.font.Font("Source_Code_Pro/SourceCodePro-Regular.ttf", 20)
        if self.record_flag:
            self.images = []

            
    def _parse_objects(self, output):
        items = [(output[i], output[i+1], output[i+2]) for i in range(0, len(output), 3)]
        self.objects = [Object(item) for item in items]
        
    def draw(self, output):
        self._parse_objects(output)
        self.blocks = 0
        self.screen.fill(BACKGROUND_COLOR)
        for object_ in self.objects:
            if object_.score != -1:
                self.score = object_.score
            else:
                if object_.id == 2:
                    self.blocks += 1
                pygame.draw.rect(self.screen, OBJECT_COLORS[object_.id], (object_.x*20, object_.y*20, 20, 20), 0)
            if object_.id == 3:
                self.paddle_x = object_.x
            elif object_.id == 4:
                self.ball_x = object_.x
        textsurface = self.myfont.render('Step {}'.format(self.steps), False, TEXT_COLOR)
        self.screen.blit(textsurface,(180, 430))
        textsurface = self.myfont.render('Score {}'.format(self.score), False, TEXT_COLOR)
        self.screen.blit(textsurface,(420, 430))
        pygame.display.update()
        self.steps += 1
        if self.record_flag:
            pygame.image.save(self.screen, "recording/{}.png".format(str(self.steps).zfill(5)))
            if self.score == 11040:
                for c in range(180):
                    pygame.image.save(self.screen, "recording/{}_{}.png".format(str(self.steps).zfill(5), str(c).zfill(3)))
    
    def compute_move(self):
        if self.ball_x < self.paddle_x:
            return -1
        elif self.ball_x == self.paddle_x:
            return 0
        elif self.ball_x > self.paddle_x:
            return 1
    
    def get_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_a:
                         return -1
                     elif event.key == pygame.K_s:
                         return 0
                     elif event.key == pygame.K_d:
                         return 1
