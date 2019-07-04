""" Utilities for preprocessing and extraction """
from collections import Counter
import itertools
import logging
import re

import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import textacy.keyterms

log = logging.getLogger(__name__)


def normalize_whitespace(text, spaces=None):
    """ Replace two or more subsequent whitespaces, and non-breaking spaces, with a single space. """

    if not spaces:
        spaces = [r"\s+", r"\u00a0"]
    log.debug(f"whitespace patterns: {spaces}")
    return re.sub("|".join(spaces), " ", text).strip()


def normalize_dashes(text, dashes=None):
    """ Replace various dashes with minus. """

    if not dashes:
        dashes = [r"\u2013", r"\u2014", r"\u2500"]
    log.debug(f"normalizing dashes: {dashes}")
    text = re.sub("|".join(dashes), "-", text)

    return text


def normalize_quotes(text):
    """ Replace left and right quotation marks (single and double) with 'normal' quotes (ascii ' and "). """

    # left and right single quotation marks & single guillemets
    singles = [r"\u2018", r"\u2019", r"\u2039", r"\u203a"]
    text = re.sub(r"|".join(singles), "'", text)
    log.debug(f"normalizing single quotes: {singles}")

    doubles = [r"\u201c", r"\u201d", r"\u00ab", r"\u00bb"]
    text = re.sub(r"|".join(doubles), '"', text)
    log.debug(f"normalizing double quotes: {doubles}")

    return text


def normalize_patterns(text, patterns=None):
    """ Replace logograms with their corresponding word or phrase.

        parameters:
            patterns: a list of (pattern, replacement) tuples.
    """

    if not patterns:
        patterns = [(r"&", "en"), (r"-\s+", ""), (r"/", ","), (r"(t)'(\w+)", r"\1\2"), (r"_", " ")]
    log.debug(f"substitution patterns: {patterns}\n")
    for pat in patterns:
        text = re.sub(*pat, text)

    return text


def pipeline(text, whitespace=True, dashes=True, quotes=True, patterns=True):

    if whitespace:
        text = normalize_whitespace(text)
    if dashes:
        text = normalize_dashes(text)
    if quotes:
        text = normalize_quotes(text)
    if patterns:
        text = normalize_patterns(text)

    return text


def ngrams(text, n=2):

    if n == 2:
        a, b = itertools.tee(text, 2)
        next(b, None)
        grams = list(zip(a, b))
    elif n == 3:
        a, b, c = itertools.tee(text, 3)
        next(b, None)
        next(c, None)
        next(c, None)
        grams = list(zip(a, b, c))
    else:
        logging.error(f"invalid n: {n}. Bigrams or trigrams only.")
        raise ValueError(f"invalid n: {n}. Bigrams or trigrams only.")

    for ng in grams:
        if isinstance(ng[0], spacy.tokens.token.Token):
            if any(x.like_num or x.is_stop for x in ng):
                continue
            yield " ".join(n.lemma_ for n in ng)
        else:
            yield " ".join(ng)


def key_sentences(sents, n=10):
    tfidf = TfidfVectorizer().fit_transform(sents)
    sim_graph = nx.from_scipy_sparse_matrix(tfidf * tfidf.T)
    results = sorted(list(zip(sents, nx.pagerank(sim_graph).values())), key=lambda x: x[1], reverse=True)
    return results[:n]


def stats(doc):
    """ Return basic counts.

    Parameters:
        doc: text processed by Spacy (spacy.tokens.doc.Doc)
    """
    if len(doc) < 1:
        log.warning(f"Empty document")
        return {}

    words = [w for w in doc if not w.is_punct and not w.is_space and not w.is_currency]
    word_frequencies = Counter(w.lemma_ for w in words if not w.is_stop
                               and not w.pos in ["PART", "PRON", "NUM", "CONJ", "CCONJ", "DET"])
    sentences = [s.text for s in doc.sents]
    avg_sent_length = len(words) / len(sentences)
    bgrams = list(ngrams([w for w in words]))
    tgrams = list(ngrams([w for w in words], 3))
    pos_bigrams = list(ngrams([w.pos_ for w in words if not w.like_num]))
    pos_trigrams = list(ngrams([w.pos_ for w in words if not w.like_num], 3))

    return {
        "n_words": len(words),
        "words_freq": word_frequencies.most_common(10),
        "n_sents": len(sentences),
        "avg_sentence_length": avg_sent_length,
        "bigrams": Counter(bgrams).most_common(10),
        "trigrams": Counter(tgrams).most_common(10),
        "abstract_bigrams": Counter(pos_bigrams).most_common(10),
        "abstract_trigrams": Counter(pos_trigrams).most_common(10),
        "key_sentences": key_sentences(sentences),
        "key_terms": textacy.keyterms.textrank(doc)
    }
