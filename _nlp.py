#!/usr/bin/env python
#-*- encoding: utf-8 -*-

## In The Name of Allah

import spacy

from sklearn.cluster import DBSCAN as dbscan
from gensim.models.word2vec import Word2Vec
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel as DLA


## REF: https://github.com/kavgan/nlp-in-practice/blob/master/tf-idf/Keyword%20Extraction%20with%20TF-IDF%20and%20SKlearn.ipynb
def __sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def __extract_top_from_vector(feature_names, sorted_items, topn=None):
    #use only topn items from vector
    if topn is not None:
        sorted_items = sorted_items[:topn]

    for idx, score in sorted_items:
        yield feature_names[idx]
## END REF

def __cluster_present(cluster, keywords_list, keyword):
    lbl = cluster.labels_[cluster.components_.tolist().index(keyword)]
    for kwv in keywords_list:
        kws_idx = cluster.components_.tolist().index(kwv)
        kws_lbl = cluster.labels_[kw_idx]
        if kws_lbl == lbl:
            return False
    return True


def _extract_topic(tlist):
    max_topic = (-1, -1)
    for topic in tlist:
        if max_topic[1] < topic[1]:
            max_topic = topic
    return max_topic[0]

def _multiindex(list_like, *indices):
    return (list_like[i] for i in indices)

def extract_concepts(docs, lang="en"):
    """ extract_concepts(docs: [<str>*]) -> [<str>*]

    Estracts concepts from a document set.

    The process is:
    First, normalizing each document to prepare them for further processing
    Then tokenize and PoS tag. After that, removing punctuations and pronouns.
    Now, stemming/lemmatize each word to prevent detection of same concepts by
    different words.

    to further fine tune the model we train a word vector embedding on the whole
    cleaned document corpus and use DBSCAN to cluster similar words.

    After all, do topic modeling on whole corpus and tag each document.
    At this time we compute tf-idf score of each word in each topic and then
    populates lists of highest scored words which are not in same cluster as concepts
    for every topic.

    At last, returns union of concepts lists for all topics.

    :param: docs List of Documents which concepts extracts from them

    "return" list of strings
    """

    nlp = spacy.load(lang)
    cleaned_docs = [
            [
                tok.lemma_.lower() for tok in nlp(doc) if not (
                    tok.is_bracket or 
                    tok.is_punct or 
                    tok.is_quote or 
                    tok.is_space or 
                    tok.is_space or 
                    tok.is_stop) and tok.pos_ != "PRON"
            ] for doc in docs
    ]

    dict_corpus = Dictionary(cleaned_docs)
    bow_corpus = [dict_corpus.doc2bow(doc) for doc in cleaned_docs]

    ## TODO: word vector embedding learning
    w2v = Word2Vec(sentences=cleaned_docs, size=300, iter=20)

    ## TODO: DBSCAN clustering of word embeddings
    cluster = dbscan(eps=0.1, min_samples=0, n_jobs=-1, metric="cosine")
    cluster.fit(w2v.wv.vectors)

    ## TODO: LDA/LSA Topic modeling on whole docs
    lda = LDA(bow_corpus, passes=10, num_topics=10)
    docs_topics = [_extract_topic(lda[doc]) for doc in bow_corpus]

    topics = dict()
    for idx, topic in enumerate(docs_topics):
        try:
            topics[topic].append(idx)
        except KeyError:
            topics[topic] = [idx]

    doc_topics = {
            key: _multiindex(cleaned_docs, topics[key])
                for key in topics
    }

    ## TODO: tf-idf score calculation
    topics_tfidf = {
        key: TfIdfVectorizer().fit(" ".join(doc)
            for doc in doc_topics[key])
        for key in doc_topics
    }

    ## TODO: extract concepts based on tf-idf w.r.t word clusters
    res_keywords = []
    
    for topic in topics:
        tfidfv = topics_tfidf[topic]
        cv = tfidfv.transform(
                " ".join(doc) for doc in doc_topics[key]
        )
        features = tfidfv.get_feature_names()
        kwit = __extract_top_from_vector(
                tfidfv.get_feature_name(),
                __sort_coo(cv.tocoo())
        )

        keywords = []
        keywords_vec = []
        for keyword in kwit:
            if len(keywords) >= 5:
                break
            keyword_vec = w2v.wv[keyword]
            if not __cluster_present(cluster, keywords_vec, keyword_vec):
                keywords.append(keyword)
                keywords_vec.append(keyword_vec)
        res_keywords.extend(keywords)
    return set(res_keywords)
