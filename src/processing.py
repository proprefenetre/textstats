""" Utilities for preprocessing and extraction """
from collections import Counter
import itertools
import logging
import operator
import re

import cytoolz
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
        patterns = [
            # (r"&", "en"),
            (r"-\s+", ""),
            (r"/", ","),
            (r"(t)'(\w+)", r"\1\2"),
            (r"_", " "),
            (r"\u00b7", ","),
            ("'t", "het"),
        ]
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


def key_sentences(text, n=10):
    sents = [s.text for s in text.sents]
    tfidf = TfidfVectorizer().fit_transform(sents)
    sim_graph = nx.from_scipy_sparse_matrix(tfidf * tfidf.T)
    results = sorted(
        list(zip(sents, nx.pagerank(sim_graph).values())),
        key=lambda x: x[1],
        reverse=True,
    )
    return results[:n]


class Stats:
    """ Return basic text statistics

    Parameters:
        doc: spacy.tokens.doc.Doc
    """

    def __init__(self, doc):
        if len(doc) < 50:
            log.warning(f"Document is very short")
            return None
        log.debug("Counting")
        self.doc = doc
        self.words = [
            w for w in doc if not w.is_punct and not w.is_space and not w.is_currency
        ]
        self.n_words = len(self.words)
        self.avg_word_length = sum(len(w) for w in self.words) / self.n_words
        self.sentences = [s.text for s in doc.sents]
        self.n_sentences = len(self.sentences)
        self.avg_sent_length = self.n_words / self.n_sentences

    @property
    def word_frequencies(
        self, posfilter=("ADP", "CONJ", "CCONJ", "DET", "PART", "PRON")
    ):
        return Counter(w.lemma_ for w in self.words if w.pos_ not in posfilter)

    @property
    def nouns(self):
        return Counter(w.lemma_ for w in self.words if w.pos_ == "NOUN")

    @property
    def verbs(self):
        return Counter(w.lemma_ for w in self.words if w.pos_ == "VERB")

    def n_grams(self, n):
        grams = cytoolz.sliding_window(n, self.words)
        for bg in cytoolz.remove(
            lambda x: any(t.like_num or t.is_stop for t in x), grams
        ):
            yield " ".join(g.text for g in bg)

    def pos_grams(self, n):
        grams = cytoolz.sliding_window(n, self.words)
        for bg in cytoolz.remove(
            lambda x: any(t.like_num or t.is_stop for t in x), grams
        ):
            yield " ".join(g.pos_ for g in bg)

    def all_stats(self, n=None, r=False):
        """ Return all statistics

        n: return n-n most frequent elements. If `None` return all elements,
        r: round decimals to `r` digits precision. If `None` return unrounded averages
        """

        def maybe_round(num):
            return round(num, r) if r else num

        return {
            "n_words": self.n_words,
            "words_freq": self.word_frequencies.most_common(n),
            "avg_word_length": maybe_round(self.avg_word_length),
            "frequent_nouns": self.nouns.most_common(n),
            "frequent_verbs": self.verbs.most_common(n),
            "key_terms": textacy.keyterms.textrank(self.doc),
            "n_sents": self.n_sentences,
            "avg_sentence_length": maybe_round(self.avg_sent_length),
            "key_sentences": key_sentences(self.doc),
            "bigrams": Counter(self.n_grams(2)).most_common(n),
            "trigrams": Counter(self.n_grams(3)).most_common(n),
            "abstract_trigrams": Counter(self.pos_grams(3)).most_common(n),
        }
