""" Utilities for preprocessing and extraction """
from collections import Counter
import itertools
import re
import spacy


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
        raise ValueError(f"invalid n: {n}. Bigrams or trigrams only.")

    for ng in grams:
        if isinstance(ng[0], spacy.tokens.token.Token):
            if any(x.like_num or x.is_stop for x in ng):
                continue
            yield " ".join(n.lemma_ for n in ng)
        else:
            yield " ".join(ng)


def counts(doc):
    """ Return basic counts.

    Parameters:
        doc: text processed by Spacy (spacy.tokens.doc.Doc)
    """
    words = [w for w in doc if not w.is_punct and not w.is_space and not w.is_currency]
    hapaxes = list({w.lemma_ for w in words if not w.is_stop and not w.like_num})
    sentences = [s.text for s in doc.sents]
    bgrams = list(ngrams([w for w in words]))
    tgrams = list(ngrams([w for w in words], 3))
    pos_bigrams = list(ngrams([w.pos_ for w in words if not w.like_num]))
    pos_trigrams = list(ngrams([w.pos_ for w in words if not w.like_num], 3))

    return {
        "n_words": len(words),
        "words_freq": Counter(w.lemma_ for w in words).most_common(10),
        "n_hapaxes": len(hapaxes),
        "n_sents": len(sentences),
        "avg_sentence_length": sum(len(s.split()) for s in sentences) / len(sentences),
        "bigrams": Counter(bgrams).most_common(10),
        "trigrams": Counter(tgrams).most_common(10),
        "abstract_bigrams": Counter(pos_bigrams).most_common(10),
        "abstract_trigrams": Counter(pos_trigrams).most_common(10),
    }
