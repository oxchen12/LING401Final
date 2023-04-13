import urllib.request
import gzip
import json
import sys
import logging

data = []
logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def _init_data():
    """
    Fetches poem data from the Gutenberg corpus and stores in in the global data.

    :return: None
    """
    global data
    if not data:
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
    _init_data()
    for obj in data:
        if int(obj["gid"]) != gid:
            continue

        yield obj["s"]
