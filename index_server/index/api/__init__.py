"""Insta485 REST API."""

import os
from index.api.main import services, hits
import index

dic = {}


def load_index():
    """Load index."""
    with open('index_server/index/stopwords.txt', 'r', encoding='utf-8') as f:
        dic['stopwords'] = f.read().split()
    with open('index_server/index/pagerank.out', 'r', encoding='utf-8') as f:
        dic['pagerank'] = f.read().split()
        dic['pagerank'] = dict(
            (tuple(item.split(",")) for item in dic['pagerank'])
        )
    segment = index.app.config["INDEX_PATH"]
    with open(
            os.path.join(
                'index_server/index/inverted_index', segment
            ), 'r', encoding='utf-8'
    ) as f:
        dic['index'] = {}
        for line in f:
            temp = line.split()
            dic['index'][temp[0]] = temp
