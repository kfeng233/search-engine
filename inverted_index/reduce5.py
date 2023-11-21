#!/usr/bin/env python3
import sys
import itertools

def reduce_one_group(key, group):
    """Reduce one group."""
    documents = []
    for line in group:
        doc_id, tf, n_factor = line.partition("\t")[2].split()
        documents.append((doc_id, tf, n_factor))
    print(f"{key} {documents}")
        


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
