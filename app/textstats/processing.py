""" Utilities for preprocessing and extraction """
from collections import Counter
import itertools
import re


def normalize_whitespace(text, spaces=None):
    """ Replace two or more subsequent whitespaces, and non-breaking spaces, with a single space. """
    if not spaces:
        spaces = [r"\s+", r"\u00a0"]

    return re.sub("|".join(spaces), " ", text)


def normalize_dashes(text, dashes=None):
    """ Replace various dashes with minus. """
    if not dashes:
        dashes = [r"\u2013", r"\u2014", r"\u2500"]
    text = re.sub("|".join(dashes), "-", text)

    return text


def normalize_quotes(text):
    """ Replace left and right quotation marks (single and double) with 'normal' quotes (ascii ' and "). """

    # left and right single quotation marks & single guillemets
    text = re.sub(r"|".join([r"\u2018", r"\u2019", r"\u2039", r"\u203a"]), "'", text)

    text = re.sub(r"|".join([r"\u201c", r"\u201d", r"\u00ab", r"\u00bb"]), '"', text)
    return text


def normalize_patterns(text, patterns=None):
    """ Replace logograms with their corresponding word or phrase.

        parameters:
            patterns: a list of (pattern, replacement) tuples.
    """
    if not patterns:
        patterns = [(r"&", "en"), (r"-\s+", ""), (r"/", ","), (r"(t)'(\w+)", r"\1\2")]

    for pat in patterns:
        text = re.sub(*pat, text)
    return text


def pipeline(text, whitespace=True, dashes=True, quotes=True, patterns=True):
    if whitespace:
        text = normalize_whitespace(text).strip()
    if dashes:
        text = normalize_dashes(text)
    if quotes:
        text = normalize_quotes(text)
    if patterns:
        text = normalize_patterns(text)

    return text


def bigrams(text):
    a, b = itertools.tee(text, 2)
    next(b, None)
    grams = list(zip(a, b))
    for ng in grams:
        # if any(x.like_num or x.is_stop for x in ng):
        #     continue
        try:
            yield " ".join(n.lemma_ for n in ng)
        except:
            yield " ".join(ng)


def trigrams(text):
    a, b, c = itertools.tee(text, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    grams = list(zip(a, b, c))
    for ng in grams:
        # if any(x.like_num or x.is_stop for x in ng):
        #     continue
        try:
            yield " ".join(n.lemma_ for n in ng)
        except:
            yield " ".join(ng)


def counts(doc):
    """ Return basic counts.

    Parameters:
        doc: text processed by Spacy (spacy.tokens.doc.Doc)
    """
    words = [w for w in doc if not w.is_punct and not w.is_space and not w.is_currency]
    hapaxes = list({w.lemma_ for w in words if not w.is_stop and not w.like_num})

    bgrams = list(bigrams([w for w in words]))
    tgrams = list(trigrams([w for w in words]))

    pos_grams = list(trigrams([w.pos_ for w in words if not w.like_num])) + list(bigrams([w.pos_ for w in words if not w.like_num]))

    return {
        "n_words": len(words),
        "words_freq": Counter(w.lemma_ for w in words).most_common(10),
        "n_sents": len(list(doc.sents)),
        "hapaxes": sorted(hapaxes, reverse=True),
        "n_hapaxes": len(hapaxes),
        "bigrams": Counter(bgrams).most_common(10),
        "trigrams": Counter(tgrams).most_common(10),
        "constructions": Counter(pos_grams).most_common(10),
    }
