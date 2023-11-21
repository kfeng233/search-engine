"""Insta485 REST API."""

from index.api.main import services, hits
import os
import index

dic = {}
def load_index():
    with open('index_server/index/stopwords.txt', 'r') as f:
        dic['stopwords'] = f.read().split()
    with open('index_server/index/pagerank.out', 'r') as f:
        dic['pagerank'] = f.read().split()
        dic['pagerank'] = dict((tuple(item.split(",")) for item in dic['pagerank']))
    segment = index.app.config["INDEX_PATH"]
    with open(os.path.join('index_server/index/inverted_index', segment), 'r') as f:
        dic['index'] = {}
        for line in f:
            temp = line.split()
            dic['index'][temp[0]] = temp
    
