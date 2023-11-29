#!/usr/bin/env python3
"""Map 5."""
import sys

for line in sys.stdin:
    term, idf, doc_id, tf, n_factor = line.split()
    segment = (int)(doc_id) % 3
    print(f"{segment}\t{term} {doc_id} {idf} {tf} {n_factor}")
