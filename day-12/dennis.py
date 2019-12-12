#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:00:22 2019

@author: dennis

Build video with:
    ffmpeg -framerate 60 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p orbits.mp4
"""

from physics import Body, OrbitalSystem

colors = ('io', 'ganymede', 'europa', 'callisto')
with open('data/input.txt', 'r') as f:
    bodies = []
    to_strip = '<x=,yz>'
    for i, line in enumerate(f.readlines()):
        ns = ''
        for char in line.strip('\n'):
            if char not in to_strip:
                ns += char
        x, y, z = [int(x) for x in ns.split(' ')]
        bodies.append(Body(x, y, z, colors[i]))

system = OrbitalSystem(bodies, draw_flag=True, record_flag=True)
while system.steps < 1001:
    system.step()
print(system.energies[1001])
