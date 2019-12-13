#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:00:22 2019

@author: dennis

Build video with:
    ffmpeg -framerate 60 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p orbits.mp4
"""

from physics import Body, OrbitalSystem
import numpy as np
import re

planet_names = ('io', 'ganymede', 'europa', 'callisto')
bodies = []
with open('data/input.txt', 'r') as f:
    for i, line in enumerate(f.readlines()):
        x, y, z = [int(x) for x in re.findall(r'-?\d+', line)]
        bodies.append(Body(x, y, z, planet_names[i]))

system = OrbitalSystem(bodies, draw_flag=True, record_flag=True)
#while not system.solved:
while system.steps < 1001:
    system.step()

print('Part 1:', system.energies[1000+2])
#print('Part 2:', np.lcm(np.lcm(system.solutions['x'], system.solutions['y']), system.solutions['z']))
