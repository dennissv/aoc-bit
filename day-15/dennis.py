#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 22:32:33 2019

@author: dennis
"""

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode
import Game
import networkx as nx

opcodes = read_opcode('data/input.txt')
computer = IntcodeComputer(opcodes.copy(), [])
game = Game.Game()

def move_long(moves):
    for move in moves:
        while not computer.awaiting_input:
            computer.step()
        computer.input_queue.append(move)
        while not computer.output_queue:
            computer.step()
        game.move(move, computer.output_queue.pop())
#        game.draw()
        
def dist_to_node(pos):
    return len(game.get_path(pos))

old_pos = (1, 1)
co = 0
#while not game.done:
while game.to_test:
    if computer.awaiting_input:
        for i in range(1, len(game.to_test)):
            next_node = game.to_test[-i]
            if next_node not in game.visited:
                continue
        game.visited.add(next_node)
        if (next_node == (game.player.x, game.player.y)) or (next_node in game.visited):
            if next_node in game.to_test:
                game.to_test.remove(next_node)
        path = game.get_path(next_node)
        moves = [game.get_move(path[i], path[i+1]) for i in range(len(path)-1)]
        old_pos = (game.player.x, game.player.y)
        move_long(moves)
        co += 1
    computer.step()

game.graph.remove_edge((50,50), (50,51))
game.graph.remove_edge((50,50), (50,49))
game.graph.remove_edge((50,50), (51,50))
#game.draw_solution()
print(nx.astar_path_length(game.graph, (50, 50), (game.answer[0], game.answer[1])))
