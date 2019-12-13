#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:18:33 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode
from Game import Game

opcodes = read_opcode('data/input.txt')
computer = IntcodeComputer(opcodes.copy(), [])
computer.memory[0] = 2
game = Game()
while computer.active:
    if computer.awaiting_input:
        game.draw(computer.output_queue)
        input_ = game.compute_move()
        computer.input_queue.append(input_)
    computer.step()
game.draw(computer.output_queue)
