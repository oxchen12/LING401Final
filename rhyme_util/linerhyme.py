#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:46:21 2023

@author: amm
"""

import nltk
from poem import *
from rhyme import *
from nltk.tokenize import word_tokenize
import urllib.request
import gzip
import json
import sys
import logging

all_lines = []
for line in gzip.open("gutenberg-poetry-v001.ndjson.gz"):
    all_lines.append(json.loads(line.strip()))
all_lines


def lastWord(line):
    text = line['s']
    gid = line['gid']
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha() and gid != '19'] 
    if len(words) > 1:
        return (words[-1], gid)

'''' this only works with 4-line stanzas bc there's no way to distinguish
stanzas'''
def rhyme_type(poemlasts, startline):
    ''' Checks pairs of lines for rhyme
     Returns bool, first rhyming line number, second rhyme line number,
     and the first line number again to distinguish its rhyme.'''
    
    for startline in range(startline, startline + 3):
        if(is_rhyme(poemlasts[startline], poemlasts[startline+1])):
            return (True, startline, startline+1, startline)
        if(is_rhyme(poemlasts[startline], poemlasts[startline + 2])):
            return (True, startline, startline + 2, startline)
        if(is_rhyme(poemlasts[startline], poemlasts[startline + 3])):
            return (True, startline, startline + 3, startline)
    return (False, startline, startline+3, startline)


def get_poem_rhymes(poemlasts):
    poemrhymes = [0] * len(poemlasts)
    for i in range(0, len(poemlasts)-3, 1):
        rt = rhyme_type(poemlasts, i)
        if(rt[0]):
            poemrhymes[rt[1]] = (poemlasts[rt[1]], rt[3])
            poemrhymes[rt[2]] = (poemlasts[rt[2]], rt[3])

def printwords(poemrhymes):
    rhymenums = []
    for word in poemrhymes:
        if(word != 0):
            rhymenums.append(word[1])
            print (word)
def howManyRhymes(rhymenums):
    howmanyrhymes = nltk.FreqDist(rhymenums).most_common()
    uniquerhymes = [rhyme for rhyme, common in howmanyrhymes if common == 2]
    print("There are " + str(len(uniquerhymes)) + " unique rhyming pairs")

         
    #Assign first line rhyme to be "A" or 1 (might be easier)
    #check the rhyme between first line and next line
    #assign 1 to the next line if they rhyme, 1 + 1 if they don't
    #etcetcetc go thru whole poem so you have a series of numbers
    #chained if statement or match/switch statement to match to 
    #specific rhyme pattern
    
    
    
















