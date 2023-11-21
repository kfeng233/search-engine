#!/usr/bin/env python3
import sys

for line in sys.stdin:
    term, idf, documents = line.split(maxsplit=2)
    doc_id, tf = eval(documents)[0]
    print(f"{doc_id}\t{tf} {term} {idf}")