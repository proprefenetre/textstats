import re

from flask import Flask, request, jsonify
import spacy

from .teidoc import TeiDocument
from .processing import pipeline, counts

app = Flask(__name__)


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

    nlp = spacy.load("nl_core_news_sm")
    doc = nlp(pipeline(td.text()))

    stats["counts"] = counts(doc)

    # stats["sgrank"] = sorted(keyterms.sgrank(doc, ngrams=2, window_width=500), key=lambda x: x[1], reverse=True)
    # stats["textrank"] = sorted(keyterms.textrank(doc), key=lambda x: x[1], reverse=True)

    # stats["counts"] = txt.TextStats(doc).basic_counts

    return jsonify(stats)
