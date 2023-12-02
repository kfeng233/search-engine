#!/usr/bin/env python3
"""Map 4."""
import sys
from ast import literal_eval

for line in sys.stdin:
    term, idf, documents = line.split(maxsplit=2)
    documents = literal_eval(documents)
    for doc_id, tf in documents:
        print(f"{doc_id}\t{tf} {term} {idf}")
