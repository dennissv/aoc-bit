#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 15:32:33 2019

@author: dennis
"""

from collections import deque
from dataclasses import dataclass

from IntcodeComputer import IntcodeComputer
from IntcodeComputer import read_opcode

opcodes = read_opcode('data/input.txt')

network = []
for id_ in range(50):
    network.append(IntcodeComputer(opcodes.copy(), [id_], id_=id_))

result = 0
while not result:
    for computer in network:
        computer.step()
        if (out := computer.output_queue):
            if len(out) >= 3:
                id_ = computer.get_output()
                x = computer.get_output()
                y = computer.get_output()
                if id_ == 255:
                    result = y
                    break
                network[id_].input_queue.append(x)
                network[id_].input_queue.append(y)

print('Part 1:', result)


@dataclass
class Packet:
    x: int
    y: int

class NAT():
    
    def __init__(self, network):
        self.packet = Packet(0, 0)
        self.last_sent = Packet(None, None)
        self.network = network
        self.steps = 0
        self.sent_twice = False
        self.wait = 10
    
    def update(self, x, y):
        self.packet = Packet(x, y)
        print('updated', self.packet)
    
    def send(self):
        self.network[0].input_queue = deque([self.packet.x, self.packet.y])
        if self.last_sent.y == self.packet.y:
            self.sent_twice = True
        self.last_sent = Packet(self.packet.x, self.packet.y)
    
    def is_idle(self):
        if self.wait > 0:
            return False
        all_waiting = True
        continous = True
        for computer in self.network:
            if not computer.idle:
                all_waiting = False
            if computer.recieve_tries < 10:
                continous = False
        
        if continous and all_waiting:
            print('was idle', self.steps)
            self.wait = 10
            return True
        return False
    
    def step(self):
        for computer in self.network:
            computer.step()
            if (out := computer.output_queue):
                if len(out) >= 3:
                    id_ = computer.get_output()
                    x = computer.get_output()
                    y = computer.get_output()
                    if id_ == 255:
                        self.update(x, y)
                    else:
                        self.network[id_].input_queue.append(x)
                        self.network[id_].input_queue.append(y)
        self.wait -= 1
        self.steps += 1

nat = NAT([IntcodeComputer(opcodes.copy(), [id_], id_=id_) for id_ in range(50)])
while not nat.sent_twice:
    nat.step()
    if nat.is_idle():
        nat.send()
print(nat.packet.y)
