#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 20:46:21 2023

@author: amm
"""

import nltk
from rhymeutil import poem
from rhymeutil.rhyme import *
from nltk.tokenize import word_tokenize
from typing import Iterable
import string


class RhymeSet:
    """Encapsulates a set of rhyming words with a representative member"""

    def __init__(self, rep: str, id_: str = None):
        self.rep = rep
        self.pron = None
        self.id_ = id_
        self.words = set(rep)
        self.type = RhymeType.UNDETERMINED

    def __repr__(self) -> str:
        return f"RhymeSet({self.rep}, {len(self.words)})"

    def __str__(self) -> str:
        if self.id_ is not None:
            return self.id_
        return self.__repr__()

    def add(self, word: str) -> bool:
        if self.pron is not None:
            # representative pronunciation exists
            if not is_rhyme_pron_word(self.pron, word):
                return False
        else:
            # representative pronuciation does not exist
            res = get_rhyme_prons(self.rep, word)
            if res is None:
                return False
            # rhyming pronunciations found
            self.pron = res[0]
        if self.type == RhymeType.UNDETERMINED:
            self.type = rhyme_type(self.rep, word)
        self.words.add(word)
        return True


def last_word(line: str):
    """
    Gets the last word in a line.

    :param line: string line of poem
    :return: string last word of poem
    """
    words = [w for w in word_tokenize(line.lower()) if w.isalpha()]
    return None if len(words) == 0 else words[-1]


def _names(chars=string.ascii_uppercase, char_lim=4):
    """
    Internal convenience generator for RhymeSet IDs from a given character set.

    :param chars: character set to generate names from
    :param char_lim: maximum number of characters allowed
    :return: the next name
    """
    buf = [0]
    while len(buf) <= char_lim:
        yield "".join(chars[c] for c in buf)
        carry = True
        pos = 0
        while carry and pos < len(buf):
            div, buf[pos] = divmod(buf[pos] + 1, len(chars))
            carry = div > 0
            pos += 1
        if carry:
            buf = [0] * (pos + 1)


def annotate_poem_rhymes(gid: int):
    """
    Convenience function for annotating a Gutenberg poetry corpus poem by gid.

    :param gid: gid of the poem to be annotated
    :return: line annotations of RhymeSets and
             a dictionary containing representative member keys and RhymeSet values
    """
    return annotate_rhymes(poem.get(gid))


def annotate_rhymes(lines: Iterable[str], names_gen=_names):
    """
    Annotates lines with RhymeSets.

    :param lines: iterable containing lines of the poem
    :param names_gen: generator for providing short identifiers to RhymeSets
    :return: line annotations of RhymeSets and
             a dictionary containing representative member keys and RhymeSet values
    """
    rhyme_sets = dict()
    annotations_ = []  # index i contains a tuple of line i and the RhymeSet for that line
    names = names_gen()
    for line in lines:
        last = last_word(line)
        if last is None:
            continue
        cur_set = None
        for rep, rset in rhyme_sets.items():  # check existing RhymeSets for match
            if is_rhyme(rep, last):
                cur_set = rset
                break
        if cur_set is None:  # if None, word is unique; create new RhymeSet
            cur_set = RhymeSet(last, id_=next(names))
            rhyme_sets[last] = cur_set
        else:
            cur_set.add(last)
        annotations_.append((line, cur_set))
    return annotations_, rhyme_sets
