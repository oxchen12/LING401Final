from __future__ import annotations
from enum import Enum, auto
import rhyme
import __init__

class RhymeType(Enum):
    SINGLE = auto()
    DOUBLE = auto()
    DACTYLIC = auto()
    OTHER = auto()
    NO_RHYME = auto()


def is_rhyme(a: str, b: str) -> bool:
    """
    Checks if two words rhyme.

    :param a: the first word to be checked
    :param b: the second word to be checked
    :return: false if either word is not in the CMU dictionary
             false if the words do not rhyme
             true if the words rhyme
    """
    if a not in rhyme.CMU_DICT or b not in rhyme.CMU_DICT:
        return False

    found_stress = False

    for a_phon, b_phon in zip(
            reversed(rhyme.CMU_DICT[a][0]), reversed(rhyme.CMU_DICT[b][0])):
        if found_stress:
            return a_phon != b_phon

        if a_phon != b_phon:
            return False

        if a_phon[-1] == "1":
            # primary stress found, we done
            found_stress = True

    return False  # dummy value, should never occur


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
    for phon in rhyme.CMU_DICT[a][0]:
        if phon[-1] == "1":
            found_stress = True

        if found_stress and not phon[-1].isalpha():
            syll_count += 1

    if (syll_count == 0):
        return RhymeType.SINGLE
    elif(syll_count == 1):
        return RhymeType.DOUBLE
    elif (syll_count == 2):
        return RhymeType.DACTYLIC
    else:
        # WTF
        return RhymeType.OTHER
