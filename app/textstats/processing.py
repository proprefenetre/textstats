""" Utilities for preprocessing and extraction """
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
        patterns = [(r"&", "en"),
                    (r"-\s+", ""),
                    (r"/", ","),
                    (r"(t)'(\w+)", r"\1\2")]

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
