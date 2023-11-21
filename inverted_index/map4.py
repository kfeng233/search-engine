#!/usr/bin/env python3
import sys

for line in sys.stdin:
    term, idf, documents = line.split(maxsplit=2)
    documents = eval(documents)
    for doc_id, tf in documents:
        print(f"{doc_id}\t{tf} {term} {idf}")