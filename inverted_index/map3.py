#!/usr/bin/env python3
"""Map 3."""
import sys
from ast import literal_eval

for line in sys.stdin:
    TOTAL_DOCS = 0
    with open('total_document_count.txt', 'r', encoding="utf-8") as f:
        TOTAL_DOCS = f.read().split()[0]
    term, df, documents = line.split(maxsplit=2)
    documents = literal_eval(documents)
    print(f"{term}\t{TOTAL_DOCS} {df} {documents}")
