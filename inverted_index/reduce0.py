#!/usr/bin/env python3
"""Reduce 0."""
import sys
import itertools


def reduce_one_group(group):
    """Reduce one group."""
    total_num = 0
    for line in group:
        num = line.partition("\t")[2]
        total_num += int(num)
    print(f"{total_num}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)


if __name__ == "__main__":
    main()
