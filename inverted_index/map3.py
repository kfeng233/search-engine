#!/usr/bin/env python3
import sys


for line in sys.stdin:
    total_docs = 0
    with open('total_document_count.txt', 'r') as f:
        total_docs = f.read().split()[0]

    term, df, documents = line.split(maxsplit=2)
    documents = eval(documents)
    print(f"{term}\t{total_docs} {df} {documents}")