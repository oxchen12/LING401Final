from __future__ import annotations

from dataclasses import dataclass

import nltk
import re

CMU_ENTRIES = nltk.corpus.cmudict.entries()
CMU_DICT = nltk.corpus.cmudict.dict()
ARPA_DICT = {
    "AA": "a",
    "AE": "\u00e6",
    "AH": "\u0250",
    "AO": "\u0254",
    "AW": "a\u028A",
    # "AX": "\u0259",
    "AY": "a\u026A",
    "B": "b",
    "CH": "t\u0283",
    "D": "d",
    "DH": "\u00F0",
    "EH": "\u025B",
    "ER": "\u025B\u02DE",
    "EY": "e\u026A",
    "F": "f",
    "G": "g",
    "HH": "h",
    "IH": "\u026A",
    # "IX": "\u0268",
    "IY": "i",
    "JH": "\u0064\u0292",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "NG": "\u014B",
    "OW": "o\u028A",
    "OY": "\u0254\u026A",
    "P": "p",
    "R": "\u0279",
    "S": "s",
    "SH": "\u0283",
    "T": "t",
    "TH": "\u03B8",
    "UH": "\u028A",
    "UW": "u",
    "V": "v",
    "W": "w",
    "Y": "j",
    "Z": "z",
    "ZH": "\u0292"
}


@dataclass
class Segment:
    phone: str
    stress: int

    @classmethod
    def from_str(cls, s: str):
        """
        Factory method for creating segments from ARPA format.

        :param s: the ARPA segment as a string
        :return: a new Segment object with the corresponding data
        """

        split = re.findall(r"^([A-Z]+)([0-2]?)$", s)[0]
        if not split:
            return None

        ph, st = split

        return cls(ph, 0 if not st else int(st))


def arpa_to_ipa(arpa: list[str]) -> str:
    """
    Converts an ARPA word into Unicode-formatted IPA.

    :param arpa: the ARPA formatted segments of the word
    :return: Unicode-formatted IPA string representation of the word
    """
    buf = []
    for seg in arpa:
        seg = Segment.from_str(seg)
        if seg.stress == 1:
            buf.append("\u02C8")
        elif seg.stress == 2:
            buf.append("\u02CC")
        buf.append(ARPA_DICT[seg.phone])
    return "".join(buf)


def get_pron(word: str):
    return CMU_DICT[word][0]
