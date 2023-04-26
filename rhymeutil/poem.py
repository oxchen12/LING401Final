import urllib.request
import gzip
import json
import sys
import logging

data = []
logging.basicConfig(format='%(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stderr)


def _init_data():
    """
    Fetches poem data from the Gutenberg corpus and stores in in the global data.

    :return: None
    """
    global data
    while not data:
        try:
            with gzip.open("./gutenberg-poetry-v001.ndjson.gz") as d:
                logging.info("found Gutenberg poetry corpus on local")
                data = [json.loads(line) for line in d]
                logging.info("loaded data from Gutenberg poetry corpus")
        except FileNotFoundError:
            logging.info("downloading Gutenberg poetry corpus from remote...")
            urllib.request.urlretrieve("http://static.decontextualize.com/gutenberg-poetry-v001.ndjson.gz",
                                       "./gutenberg-poetry-v001.ndjson.gz")
            logging.info("downloaded Gutenberg poetry corpus from remote")


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


def gids():
    """
    Provides a list of all (unique) gids in the corpus.

    :return: a list of all gids in the corpus
    """
    global data
    _init_data()
    return sorted(set(int(obj["gid"]) for obj in data))
