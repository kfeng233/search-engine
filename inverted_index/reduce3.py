#!/usr/bin/env python3
"""Reduce 3."""
import sys
import itertools
import math
from ast import literal_eval


def reduce_one_group(key, group):
    """Reduce one group."""
    for line in group:
        total_docs, df, documents = (line.partition("\t")[2]).split(maxsplit=2)
        documents = literal_eval(documents)
        idf = math.log10((int)(total_docs) / (int)(df))
        print(f"{key} {idf} {documents}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
