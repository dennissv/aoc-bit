#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 15:32:33 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode

opcodes = read_opcode('data/input.txt')

computer = IntcodeComputer(opcodes.copy())
while computer.active:
   if computer.awaiting_input:
       computer.print_out()
       command = input()
       computer.write(command)
   computer.step()
computer.print_out()

'''
#- food ration
- mutex
- asterisk
- space law space brochure

a = [10, 10, 10, 61, 61, 32, 80, 114, 101, 115, 115, 117, 114, 101, 45, 83, 101, 110, 115, 105, 116, 105, 118, 101, 32, 70, 108, 111, 111, 114, 32, 61, 61, 10, 65, 110, 97, 108, 121, 122, 105, 110, 103, 46, 46, 46, 10, 10, 68, 111, 111, 114, 115, 32, 104, 101, 114, 101, 32, 108, 101, 97, 100, 58, 10, 45, 32, 119, 101, 115, 116, 10, 10, 65, 32, 108, 111, 117, 100, 44, 32, 114, 111, 98, 111, 116, 105, 99, 32, 118, 111, 105, 99, 101, 32, 115, 97, 121, 115, 32, 34, 65, 110, 97, 108, 121, 115, 105, 115, 32, 99, 111, 109, 112, 108, 101, 116, 101, 33, 32, 89, 111, 117, 32, 109, 97, 121, 32, 112, 114, 111, 99, 101, 101, 100, 46, 34, 32, 97, 110, 100, 32, 121, 111, 117, 32, 101, 110, 116, 101, 114, 32, 116, 104, 101, 32, 99, 111, 99, 107, 112, 105, 116, 46, 10, 83, 97, 110, 116, 97, 32, 110, 111, 116, 105, 99, 101, 115, 32, 121, 111, 117, 114, 32, 115, 109, 97, 108, 108, 32, 100, 114, 111, 105, 100, 44, 32, 108, 111, 111, 107, 115, 32, 112, 117, 122, 122, 108, 101, 100, 32, 102, 111, 114, 32, 97, 32, 109, 111, 109, 101, 110, 116, 44, 32, 114, 101, 97, 108, 105, 122, 101, 115, 32, 119, 104, 97, 116, 32, 104, 97, 115, 32, 104, 97, 112, 112, 101, 110, 101, 100, 44, 32, 97, 110, 100, 32, 114, 97, 100, 105, 111, 115, 32, 121, 111, 117, 114, 32, 115, 104, 105, 112, 32, 100, 105, 114, 101, 99, 116, 108, 121, 46, 10, 34, 79, 104, 44, 32, 104, 101, 108, 108, 111, 33, 32, 89, 111, 117, 32, 115, 104, 111, 117, 108, 100, 32, 98, 101, 32, 97, 98, 108, 101, 32, 116, 111, 32, 103, 101, 116, 32, 105, 110, 32, 98, 121, 32, 116, 121, 112, 105, 110, 103, 32, 53, 51, 54, 57, 48, 52, 55, 51, 54, 32, 111, 110, 32, 116, 104, 101, 32, 107, 101, 121, 112, 97, 100, 32, 97, 116, 32, 116, 104, 101, 32, 109, 97, 105, 110, 32, 97, 105, 114, 108, 111, 99, 107, 46, 34, 10]
'''