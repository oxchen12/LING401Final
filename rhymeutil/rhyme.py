from __future__ import annotations
from enum import Enum, auto
from rhymeutil import *


class RhymeType(Enum):
    SINGLE = auto()
    DOUBLE = auto()
    DACTYLIC = auto()
    OTHER = auto()
    NO_RHYME = auto()


def is_rhyme(a: str, b: str) -> bool:
    """
    Checks if two words form a perfect rhyme.

    :param a: the first word to be checked
    :param b: the second word to be checked
    :return: false if either word is not in the CMU dictionary
             false if the words do not rhyme
             true if the words rhyme
    """
    if a not in CMU_DICT or b not in CMU_DICT:
        return False

    a_pron = get_pron(a)
    b_pron = get_pron(b)

    phon_pairs = zip(reversed(a_pron), reversed(b_pron))

    found_stress = False
    for a_phon, b_phon in phon_pairs:
        if found_stress:
            return a_phon != b_phon

        if a_phon != b_phon:
            return False

        if a_phon[-1] == "1":
            # primary stress found, we done
            found_stress = True

    return len(a_pron) != len(b_pron)  # words do not rhyme with themselves


def rhyme_type(a: str, b: str) -> RhymeType:
    """
    Checks the perfect rhyme type between two words

    :param a: the first word to be checked
    :param b: the second word to be checked
    :return: the RhymeType corresponding to the rhyme type
    """
    if not is_rhyme(a, b):
        return RhymeType.NO_RHYME

    found_stress = False
    syll_count = 0
    for phon in get_pron(a):
        if found_stress and not phon[-1].isalpha():
            syll_count += 1

        if phon[-1] == "1":
            found_stress = True

    if syll_count == 0:
        return RhymeType.SINGLE
    elif syll_count == 1:
        return RhymeType.DOUBLE
    elif syll_count == 2:
        return RhymeType.DACTYLIC
    else:
        # WTF
        return RhymeType.OTHER
