""" Utilities for preprocessing and extraction """


def normalize_whitespace(text):
    """ Replace two or more subsequent whitespaces, and non-breaking spaces, with a single space. """
    pass


def normalize_dashes(text):
    """ Replace various dashes with a normal hyphen. """
    pass


def normalize_logograms(text):
    """ Replace logograms with their corresponding word or phrase. """
    pass


def normalize_unicode_quotes(text):
    """ Replace left and right quotation marks (single and double) with 'normal' quotes (ascii ' and "). """
    pass



def vg_preprocess(text):
    patterns = [
        (r"\s+", " "),      # Overdreven whitespace
        ("\u2013", "-"),    # EN DASH
        ("\u2014", "-"),    # EM DASH
        (r"-\s+", ""),      # Hyphen on sentence boundary
        (r"&", "en"),
        ("/", ","),         # zgn. 'kunstkomma'
        ("\u00a0", " "),    # NO-BREAK SPACE
        ("\u2018", "'"),    # LEFT SINGLE QUOTATION MARK
        ("\u2019", "'"),    # RIGHT SINGLE QUOTATION MARK
        ("\u201c", '"'),    # LEFT DOUBLE QUOTATION MARK
        ("\u201d", '"'),    # RIGHT DOUBLE QUOTATION MARK
        ("\u00bb", '"')     # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    ]

    for pat in patterns:
        text = re.sub(*pat, text)
    return text
