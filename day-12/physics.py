#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:52:54 2019

@author: dennis
"""

from itertools import combinations

import time
from PIL import Image
import pygame

class Body():
    
    def __init__(self, x, y, z, img=''):
        self.x = x
        self.vx = 0
        self.y = y
        self.vy = 0
        self.z = z
        self.vz = 0
        self.img = img

class OrbitalSystem():
    
    def __init__(self, bodies, draw_flag=False, record_flag=False):
        self.bodies = bodies
        self.draw_flag = draw_flag
        self.record_flag = record_flag
        self.steps = 0
        if draw_flag:
            self._setup_draw()
        self.current_energy = 0
        self.energies = [0, 0, 0]
            
    def step(self):
        self._update_velocity()
        if self.draw_flag:
            self.draw()
        self._update_positions()
        self.current_energy = self.total_energy()
        self.energies.append(self.current_energy)
        self.steps += 1
    
    def _setup_draw(self):
        pygame.init()
        self.SCREEN_SIZE = 1000
        self.SCREEN = pygame.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        for body in self.bodies:
            body.img = pygame.image.load("img/{}.png".format(body.img)).convert_alpha()
        self.TEXT_COLOR = pygame.Color('#cccccc')
        self.BACKGROUND_COLOR = pygame.Color('#0f0f23')
        self.GRAPH_COLOR = pygame.Color('#00cc00')
        self.BODY_COLOR = pygame.Color('#ffff66')
        pygame.font.init()
        self.myfont = pygame.font.Font("Source_Code_Pro/SourceCodePro-Regular.ttf", 20)
        self.graph_surface = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE))
        self.graph_surface.fill(self.BACKGROUND_COLOR)
        if self.record_flag:
            self.images = []
        
    def draw(self):
        if self.steps%1 == 0:
            pygame.draw.line(self.graph_surface, self.GRAPH_COLOR,
                             ((self.steps-1)//1, int(130-(self.energies[-3]/(17500/110)))),
                             ((self.steps)//1, int(130-(self.energies[-1]/(17500/110)))), 2)
        dt = 5
        self.bodies.sort(key=lambda x: x.z)
        for t in range(dt+1):
            self.SCREEN.blit(self.graph_surface, (0,0))
            textsurface = self.myfont.render('Step {}'.format(self.steps), False, self.TEXT_COLOR)
            self.SCREEN.blit(textsurface,(10,10))
            textsurface = self.myfont.render('Energy of system: {}'.format(self.current_energy),
                                             False, self.TEXT_COLOR)
            self.SCREEN.blit(textsurface,(10, 40))
            for body in self.bodies:
                z_scale = max(5, int((body.z+60+t*(body.vz/dt))))
                xy_scale = self.SCREEN_SIZE*.175
                self.SCREEN.blit(pygame.transform.scale(body.img, (z_scale, z_scale)),
                                 (int((body.x+xy_scale-5+t*(body.vx/dt))*((self.SCREEN_SIZE/2)/xy_scale)),
                                  int((body.y+xy_scale-5+t*(body.vy/dt))*((self.SCREEN_SIZE/2)/xy_scale))))
            pygame.display.update()
            if self.record_flag:
                pygame.image.save(self.SCREEN, "recording/{}_{}.png".format(str(self.steps).zfill(5), t))
                if self.steps == 1000 and t == 5:
                    for c in range(180):
                        pygame.image.save(self.SCREEN, "recording/{}_{}_{}.png".format(str(self.steps).zfill(5), t, str(c).zfill(3)))
#                data = pygame.image.tostring(self.SCREEN, 'RGBA')
#                self.images.append(Image.frombytes('RGBA', (500,500), data))
#            time.sleep(.005)

    def _get_state(self):
        return (((b.x, b.y, b.z, b.vx, b.vy, b.vz) for b in self.bodies))
    
    def _update_velocity(self):
        for comb in combinations(self.bodies, 2):
            body1 = comb[0]
            body2 = comb[1]
            if body1.x > body2.x:
                body1.vx -= 1
                body2.vx += 1
            elif body1.x < body2.x:
                body1.vx += 1
                body2.vx -= 1
            if body1.y > body2.y:
                body1.vy -= 1
                body2.vy += 1
            elif body1.y < body2.y:
                body1.vy += 1
                body2.vy -= 1
            if body1.z > body2.z:
                body1.vz -= 1
                body2.vz += 1
            elif body1.z < body2.z:
                body1.vz += 1
                body2.vz -= 1
            
    def _update_positions(self):
        for body in self.bodies:
            body.x += body.vx
            body.y += body.vy
            body.z += body.vz
    
    def _potential_energy(self, body):
        return abs(body.x) + abs(body.y) + abs(body.z)
    
    def _kinetic_energy(self, body):
        return abs(body.vx) + abs(body.vy) + abs(body.vz)
    
    def total_energy(self):
        energy = 0
        for body in self.bodies:
            energy += self._potential_energy(body)*self._kinetic_energy(body)
        return energy
