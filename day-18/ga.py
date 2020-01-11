#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:07:00 2019

@author: dennis
"""

from navigator import Navigator
import random

class Genetic():
    
    def __init__(self, n_pop=100):
        self.population = [self.starter() for _ in range(n_pop)]
    
    def starter(self):
        return [x for x in 'zpsuPbkKaBceECowdvWmhxAtXVlTfjLqQJMHDnrRgGyYi']

    def mutate(self, individual):
        if random.randint(1, 10)//10:
            del individual[random.randint(0, len(individual)-1)]
        for _ in range(random.randint(1, 3)):
            swap_distance = random.randint(1, 5)
            swap = random.randint(0, len(individual)-1-swap_distance)
            individual[swap], individual[swap+swap_distance] = individual[swap+swap_distance], individual[swap]
        return individual
            
    def fitness(self, instructions):
        nav = Navigator(grid)
        for instruction in instructions:
            unlockable_doors = nav.reachable_doors() & set(key.upper() for key in nav.inventory)
            reachables = list(nav.reachable_keys() | unlockable_doors)
            if instruction not in reachables:
                return 100000
            
            if instruction.isupper():
                nav.move(nav.doors[instruction])
                nav.open_door(instruction)
            else:
                nav.move(nav.keys[instruction])
                nav.loot_key(instruction)
        if nav.is_completed():
            return nav.distance_traveled
        return 100000
    
    def score(self):
        scores = [self.fitness(ind.copy()) for ind in self.population]
        combined = list(zip(scores.copy(), self.population.copy()))
        combined.sort()
        return combined

    def mate(self, ind1, ind2):
        child = []
        for genes in zip(ind1, ind2):
            gene = genes[random.randint(0, 1)]
            child.append(gene)
        return child

with open('data/modified_input.txt', 'r') as f:
    grid = [line.strip('\n') for line in f.readlines()]

#pop_size = 1000
#ga = Genetic(pop_size)
#ga.population = [ga.mutate(ga.population[0].copy()) for _ in range(pop_size)]
#g = ga.score()
ga = Genetic(1)
results = []
while True:
    starter = [x for x in 'zpPbBcekKaAtsuEvCowdWmhxXVlTfjLqQJMHDnrRgGyYi']
    mutant = ga.mutate(starter)
    score = ga.fitness(mutant)
    if score < 4514:
        print(''.join(mutant), score)
    results.append((score, ''.join(mutant)))
results.sort()
