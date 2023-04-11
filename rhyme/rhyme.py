from __future__ import annotations
from __init__ import CMU_DICT
import nltk
import re
from dataclasses import dataclass
from enum import Enum, auto


class RhymeType(Enum):
    SINGLE = auto()
    DOUBLE = auto()
    DACTYLIC = auto()
    OTHER = auto()
    NO_RHYME = auto()


def is_rhyme(a: str, b: str) -> bool:
    found_stress = False

    for a_phon, b_phon in zip(reversed(CMU_DICT[a][0]), reversed(CMU_DICT[b][0])):
        if found_stress:
            return a_phon != b_phon

        if a_phon != b_phon:
            return False

        if a_phon[-1] == "1":
            # primary stress found, we done
            found_stress = True

    return False  # dummy value, should never occur


def rhyme_type(a: str, b: str) -> RhymeType:
    if not is_rhyme(a, b):
        return RhymeType.NO_RHYME

    found_stress = False
    syll_count = 0
    for phon in CMU_DICT[a][0]:
        if phon[-1] == "1":
            found_stress = True

        if found_stress and not phon[-1].isalpha():
            syll_count += 1

    match syll_count:
        case 0:
            return RhymeType.SINGLE
        case 1:
            return RhymeType.DOUBLE
        case 2:
            return RhymeType.DACTYLIC
        case _:
            # WTF
            return RhymeType.OTHER
