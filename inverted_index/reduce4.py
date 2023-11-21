#!/usr/bin/env python3
import sys
import itertools
import math

def reduce_one_group(key, group):
    """Reduce one group."""
    total_tf = 0
    n_factor = 0
    lines = list(group)
    for line in lines:
        tf, term, idf = line.partition("\t")[2].split()
        total_tf += (int)(tf)
        n_factor += (float)(idf) ** 2 * (int)(tf)
    for line in lines:
        tf, term, idf = line.partition("\t")[2].split()
        tf = (int)(math.sqrt((int)(tf)))
        print(f"{term} {idf} {key} {tf} {n_factor}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
