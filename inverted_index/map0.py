#!/usr/bin/env python3
"""Map 0."""
import sys

# Open and read from filepaths.txt
for line in sys.stdin:
    files = line.split()
    # key = 1
    for file in files:
        print(f"{1}\t1")
