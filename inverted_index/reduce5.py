#!/usr/bin/env python3
import sys
import itertools

def reduce_one_group(key, group):
    """Reduce one group."""
    lines = list(group)
    terms = {}
    for line in lines:
        term, doc_id, idf, tf, n_factor = line.partition("\t")[2].split()
        if (term, idf) in terms:
            terms[(term, idf)].append((doc_id, tf, n_factor))
        else:
            terms[(term, idf)] = [(doc_id, tf, n_factor)]
    for item, values in terms.items():
        term, idf = item
        result = ' '.join([f"{doc_id} {tf} {n_factor}" for doc_id, tf, n_factor in values])
        print(f"{term} {idf} {result}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)


if __name__ == "__main__":
    main()
