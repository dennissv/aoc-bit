#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:20:30 2019

@author: dennis
"""

with open('data/input.txt', 'r') as f:
    opcodes =[int(x) for x in f.readline().strip('\n').split(',')]
    
class Machine():
    
    def __init__(self, opcodes):
        self.opcodes = opcodes
        self.ci = 0
        self.active = True
    
    def step(self):
        two_digit_opcode, parameters = self._parse_instruction(self.opcodes[self.ci])
        self._run_instruction(two_digit_opcode, parameters)
        
    def _run_instruction(self, code, parameters):
        if code in (1, 2, 5, 6, 7, 8):
            if parameters[0] == 0:
                first_value = self.opcodes[self.opcodes[self.ci+1]]
            elif parameters[0] == 1:
                first_value = self.opcodes[self.ci+1]
            if parameters[1] == 0:
                second_value = self.opcodes[self.opcodes[self.ci+2]]
            elif parameters[1] == 1:
                second_value = self.opcodes[self.ci+2]
            if parameters[2] == 0:
                if code == 1:
                    self.opcodes[self.opcodes[self.ci+3]] = first_value + second_value
                    self.ci += 4
                elif code == 2:
                    self.opcodes[self.opcodes[self.ci+3]] = first_value * second_value
                    self.ci += 4
            elif parameters[2] == 1:
                if code == 1:
                    self.opcodes[self.ci+3] = first_value + second_value
                    self.ci += 4
                elif code == 2:
                    self.opcodes[self.ci+3] = first_value * second_value
                    self.ci += 4
            
        elif code == 3:
            input_ = int(input('Input value: '))
            self.opcodes[self.opcodes[self.ci+1]] = input_
            self.ci += 2
            
        elif code == 4:
            print(self.opcodes[self.opcodes[self.ci+1]])
            self.ci += 2
            
        if code == 5:
            if first_value:
                self.ci = second_value
            else:
                self.ci += 3
                
        elif code == 6:
            if not first_value:
                self.ci = second_value
            else:
                self.ci += 3
                
        elif code == 7:
            if first_value < second_value:
                if parameters[2] == 0:
                    self.opcodes[self.opcodes[self.ci+3]] = 1
                elif parameters[2] == 1:
                    self.opcodes[self.ci+3] = 1
            else:
                if parameters[2] == 0:
                    self.opcodes[self.opcodes[self.ci+3]] = 0
                elif parameters[2] == 1:
                    self.opcodes[self.ci+3] = 0
            self.ci += 4
            
        elif code == 8:
            if first_value == second_value:
                if parameters[2] == 0:
                    self.opcodes[self.opcodes[self.ci+3]] = 1
                elif parameters[2] == 1:
                    self.opcodes[self.ci+3] = 1
            else:
                if parameters[2] == 0:
                    self.opcodes[self.opcodes[self.ci+3]] = 0
                elif parameters[2] == 1:
                    self.opcodes[self.ci+3] = 0
            self.ci += 4
            
        elif code == 99:
            self.active = False
    
    def _parse_instruction(self, opcode):
        opcode = str(opcode).zfill(5)
        two_digit_opcode = int(opcode[-2:])
        parameters = [int(opcode[2]), int(opcode[1]), int(opcode[0])]
        return two_digit_opcode, parameters

machine1 = Machine(opcodes.copy())
while machine1.active:
    machine1.step()
