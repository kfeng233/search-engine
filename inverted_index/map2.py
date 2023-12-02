#!/usr/bin/env python3
"""Map 2."""
import sys

# <(term, doc_id, tf), #,#,#>
for line in sys.stdin:
    term, doc_id, tf = line.split()
    print(f"{term}\t{doc_id} {tf}")
