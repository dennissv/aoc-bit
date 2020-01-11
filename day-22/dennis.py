#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 20:18:19 2019

@author: dennis
"""

import re

def deal_into_new(deck):
    return deck[::-1]

def cut(deck, n):
    return deck[n:]+deck[:n]

def increment(deck, n):
    new_deck = [-1 for _ in deck]
    length = len(deck)
    for i, card in enumerate(deck):
        new_deck[(i*n)%length] = card
    return new_deck

def quick_shuffle(deck, dict_):
    new_deck = [-1 for _ in deck]
    for i, card in enumerate(deck):
        new_deck[i] = deck[dict_[i]]

def build_quick_dict(deck):
    dict_ = {}
    for i, card in enumerate(deck):
        dict_[card] = deck.index(card)

deck = [x for x in range(13007)]
#deck = [x for x in range(10)]

results = []
c = 0
while True:
    for line in open('data/input.txt'):
        line.strip()
        match = re.search('[0-9]+', line)
        if match:
            n = int(match[0])
            if '-' in line:
                n *= -1
        if 'cut' in line:
            deck = cut(deck, n)
        elif 'increment' in line:
            deck = increment(deck, n)
        elif 'stack' in line:
            deck = deal_into_new(deck)
#    result = deck.copy()
    result = deck[2019]
    if result in results:
        print('Duplicate at', c)
    if (not c%100) and c:
        print(c)
    results.append(result)
    c += 1
