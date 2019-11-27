#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# In The Name of Allah

import gensim
import gensim.models as m


class Corpus(object):
    def __init__(self, path):
        self.corpus_file = path

    def __iter__(self):
        ll = []
        with open(self.corpus_file, "r") as f:
            for w in f:
                if len(ll) > 50:
                    yield ll
                    ll.clear()
                w = w.strip()
                if w != "":
                    ll.append(w.strip())
            if len(ll) > 0:
                yield ll


def load_w2v(fname):
    return m.Word2Vec.load(fname)


def load_ft(fname):
    return m.FastText.load(fname)


def main():
    import sys
    from pprint import pprint
    corpus_path = sys.argv[1]
    corpus = Corpus(corpus_path)
    w2v = m.Word2Vec(sentences=corpus)
    print()
    print("Word2Vec vectors:")
    pprint(w2v.wv.vectors)
    print("=" * 80)
    w2v.save(f"{corpus_path}.w2v")
    ft = m.FastText(sentences=corpus)
    print()
    print("FastText vectors:")
    pprint(ft.wv.vectors)
    print()
    ft.save(f"{corpus_path}.ft")


if __name__ == "__main__":
    main()
