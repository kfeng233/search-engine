#!/usr/bin/env python3
"""Map 1."""
import pathlib
import re
import sys

import bs4

# Open and read from one HTML document at a time
for line in sys.stdin:
    # Each line is a path to a document from the dataset
    # Documents are stored at <INPUT_DIR>/crawl/<doc_id>.html
    doc_path = pathlib.Path(line.strip())

    # Get doc_id from filename
    doc_id = line.split(".")[0][-4:]

    # Read document body from file
    text = doc_path.read_text(encoding="utf-8")

    # Configure Beautiful Soup parser
    soup = bs4.BeautifulSoup(text, "html.parser")

    # Parse text from document
    text = soup.text

    # Data preprocessing and output
    # cleaning
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", text)
    text = str.casefold(text)
    terms = text.split()
    stopwords = []
    with open('stopwords.txt', 'r', encoding="utf-8") as f:
        stopwords = f.read().split()

    terms = [term for term in terms if term not in stopwords]
    # for term in terms:
    #     if term in words:
    #         terms.remove(term)
    for term in terms:
        print(f"{term} {doc_id}\t1")
