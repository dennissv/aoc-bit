#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 19:33:16 2019

@author: dennis
"""

from IntcodeComputer import read_opcode
from IntcodeComputer import IntcodeComputer

opcodes = read_opcode('data/input.txt')
computer = IntcodeComputer(opcodes.copy())
while computer.active:
    if computer.awaiting_input:
        break
    computer.step()
