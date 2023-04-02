import nltk
import re

ENTRIES = nltk.corpus.cmudict.entries()
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


def arpa_to_ipa(arpa: list[str]):
    buf = ""
    for seg in arpa:
        phon, stress = re.findall(r"^([A-Z]+)([0-2]?)$", seg)[0]
        if stress == "1":
            buf += "\u02C8"
        elif stress == "2":
            buf += "\u02CC"
        buf += ARPA_DICT[phon]
    return buf
