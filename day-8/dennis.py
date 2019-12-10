#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:12:44 2019

@author: dennis
"""

import numpy as np
from skimage import io

WIDTH = 25
HEIGHT = 6
SIZE = WIDTH*HEIGHT

with open('data/input.txt', 'r') as f:
    data = f.readline().strip('\n')

layers = [data[i:i+SIZE] for i in range(0, len(data), SIZE)]
min_zeros = SIZE+1
best_layer = ''
for layer in layers:
    if (zeros := layer.count('0')) < min_zeros:
        min_zeros = zeros
        best_layer = layer

print(best_layer.count('1')*best_layer.count('2'))

image = np.zeros((HEIGHT,WIDTH))
for i in range(SIZE):
    for layer in layers:
        if layer[i] != '2':
            image[i//WIDTH, i%WIDTH] = int(layer[i])
            break
io.imshow(image)
