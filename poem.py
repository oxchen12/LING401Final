import urllib.request
import gzip
import json
import sys
import logging
from pprint import pprint

data = None
logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def init_data():
    """
    Fetches poem data from the Gutenberg corpus.

    :return: None
    """
    global data
    if data is None:
        with urllib.request.urlopen('http://static.decontextualize.com/gutenberg-poetry-v001.ndjson.gz') as fp:
            with gzip.open(fp) as d:
                data = [json.loads(line) for line in d]
                logging.debug("loaded data from Gutenberg poetry corpus")


def get(gid: int):
    """
    Generator for getting a specific poem by gid.

    :param gid: the gid of the poem to access
    :returns: a line of the poem
    """
    # could optimize since objs are returned in gid order
    global data
    init_data()
    for obj in data:
        if int(obj["gid"]) != gid:
            continue

        yield obj["s"]
