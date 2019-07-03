import logging
import re

from flask import Flask, request, jsonify
import spacy

from .teidoc import TeiDocument
from .processing import pipeline, counts


logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


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
        return "No document specified\n"

    td = TeiDocument(doc)
    logger.debug(f"Created TeiDocument")
    stats = dict()

    # TODO: add names
    stats["entities"] = td.entities()
    for k, v in stats["entities"].items():
        stats[f"num_{k}"] = len(v)
    logger.debug("Add entities")

    nlp = spacy.load("nl_core_news_sm")
    logger.debug("Load spacy nl model")

    doc = nlp(pipeline(td.text()))
    logger.debug("Normalize text")

    stats["counts"] = counts(doc)
    logger.debug("Add counts")

    # stats["sgrank"] = sorted(keyterms.sgrank(doc, ngrams=2, window_width=500), key=lambda x: x[1], reverse=True)
    # stats["textrank"] = sorted(keyterms.textrank(doc), key=lambda x: x[1], reverse=True)

    # stats["counts"] = txt.TextStats(doc).basic_counts

    return jsonify(stats)
