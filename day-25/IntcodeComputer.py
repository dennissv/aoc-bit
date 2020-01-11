#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 00:40:47 2019

@author: dennis
"""

from collections import deque

def read_opcode(fname):
    with open(fname, 'r') as f:
        return [int(x) for x in f.readline().strip('\n').split(',')]

def to_ascii(li):
    return ''.join(chr(char) for char in li)

def from_ascii(s):
    return [ord(char) for char in s]+[10]

class IntcodeComputer():
    
    def __init__(self, opcodes, inputs=[]):
        self.memory = {i: x for i, x in enumerate(opcodes)}
        self.pointer = 0
        self.pointer_jump = {1: 4, 2: 4, 3: 2, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}
        self.jumped = False
        self.awaiting_input = False
        self.active = True
        self.input_queue = deque(inputs)
        self.input_pointer = 0
        self.output_queue = deque()
        self.output = 0
        self.relative_base = 0
        self.steps = 0
    
    def step(self):
        opcode, values = self._parse_instruction(self.memory[self.pointer])
        self._run_instruction(opcode, values)
        if not self.awaiting_input:
            self._pointer_step(opcode)
        self.steps += 1
        
    def _run_instruction(self, opcode, values):
        if opcode == 1: # add
            self._write(values[2], values[0]+values[1])

        elif opcode == 2: # mulitply
            self._write(values[2], values[0]*values[1])
           
        elif opcode == 3: # input
            if not self.input_queue:
                self.awaiting_input = True
            else:
                self._write(values[0], self.input_queue.popleft())
                self.awaiting_input = False
            
        elif opcode == 4: # output
            self.output = values[0]
            self.output_queue.append(self.output)
            
        elif opcode == 5: # jump-if-true
            if values[0]:
                self._jump_to(values[1])
                
        elif opcode == 6: # jump-if-false
            if not values[0]:
                self._jump_to(values[1])
                
        elif opcode == 7: # less than
            self._write(values[2], int(values[0] < values[1]))
            
        elif opcode == 8: # equals
            self._write(values[2], int(values[0] == values[1]))
        
        elif opcode == 9: # adjust relative base
            self.relative_base += values[0]
            
        elif opcode == 99: # shutdown
            self.active = False
    
    def _parse_instruction(self, opcode):
        opcode = str(opcode).zfill(5)
        two_digit_opcode = int(opcode[-2:])
        parameters = [int(opcode[2]), int(opcode[1]), int(opcode[0])]
        
        values = []
        if two_digit_opcode in (1, 2, 4, 5, 6, 7, 8, 9):
            for i in range(2):
                if parameters[i] == 0:
                    values.append(self._read(self.memory[self.pointer+i+1]))
                elif parameters[i] == 1:
                    values.append(self._read(self.pointer+i+1))
                elif parameters[i] == 2:
                    values.append(self._read(self.memory[self.pointer+i+1]+self.relative_base))
        
        if two_digit_opcode in (1, 2, 7, 8):
            if parameters[2] == 0:
                values.append(self._read(self.pointer+3))
            elif parameters[2] == 1:
                values.append(self.pointer+3)
            elif parameters[2] == 2:
                values.append(self._read(self.pointer+3)+self.relative_base)
        
        if two_digit_opcode == 3:
            if parameters[0] in range(2):
                values.append(self._read(self.pointer+1))
            elif parameters[0] == 2:
                values.append(self._read(self.pointer+1)+self.relative_base)
                
        return two_digit_opcode, values
    
    def _read(self, adress):
        if adress not in self.memory:
            self.memory[adress] = 0
        return self.memory[adress]
    
    def _write(self, adress, value):
        self.memory[adress] = value
    
    def _jump_to(self, pointer):
        self.pointer = pointer
        self.jumped = True
    
    def _pointer_step(self, opcode):
        if self.active:
            if self.jumped:
                self.jumped = False
            else:
                self.pointer += self.pointer_jump[opcode]
    
    def get_output(self):
        return self.output_queue.popleft()
    
    def print_out(self):
        print(to_ascii(self.output_queue))
        self.output_queue = deque([])

    def write(self, s):
        self.input_queue = deque(from_ascii(s))
