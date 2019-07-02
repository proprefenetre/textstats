import re

from flask import Flask, request, jsonify
import spacy
# import textacy as txt
# import textacy.keyterms as keyterms

from .teidoc import TeiDocument


app = Flask(__name__)


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


@app.route("/", methods=["POST"])
def textstats():
    if request.data and isinstance(request.data, bytes):
        doc = request.data
    elif request.form:
        if request.form.get("file", None):
            doc = request.form.get("file")
        else:
            return "Invalid request\n"
    else:
        return "Specify document\n"

    td = TeiDocument(doc)
    stats = dict()

    # TODO: add names
    stats["entities"] = td.entities()
    for k, v in stats["entities"].items():
        stats[f"num_{k}"] = len(v)

    text = vg_preprocess(td.text())

    nlp = spacy.load("nl_core_news_sm")
    doc = nlp(text)

    # stats["sgrank"] = sorted(keyterms.sgrank(doc, ngrams=2, window_width=500), key=lambda x: x[1], reverse=True)
    # stats["textrank"] = sorted(keyterms.textrank(doc), key=lambda x: x[1], reverse=True)

    # stats["counts"] = txt.TextStats(doc).basic_counts

    stats["text"] = text

    return jsonify(stats)
