#!/usr/bin/env python3
import sys

documents = []
for line in sys.stdin:
    term, idf, doc_id, tf, n_factor = line.split()
    print(f"{term} {idf}\t{doc_id} {tf} {n_factor}")