import logging
import os
import re

from flask import Flask, request, jsonify
import spacy

from .teidoc import TEIDocument
from .processing import pipeline, counts


log_file = os.path.join(os.path.dirname(__file__), "textstats.log")
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_file, filemode="w", format=FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)


app = Flask(__name__)


@app.route("/logs", methods=["GET"])
def logs():
    with open(log_file, "r") as f:
        logs = f.read()
    return jsonify(logs)


@app.route("/", methods=["POST"])
def textstats():
    if request.data and isinstance(request.data, bytes):
        data = request.data
    elif request.form:
        if request.form.get("file", None):
            data = request.form.get("file")
        else:
            return "Invalid request\n"
    else:
        return "No document specified\n"

    td = TEIDocument()
    td.load(data)
    log.debug(f"TEIDocument loaded: {td.docinfo()}")
    stats = dict()

    # TODO: add names
    log.debug("Add entities")
    stats["entities"] = td.entities()
    for k, v in stats["entities"].items():
        stats[f"num_{k}"] = len(v)

    log.debug("Load Spacy model")
    nlp = spacy.load("nl_core_news_sm")

    log.debug("Normalize text")
    doc = nlp(pipeline(td.text()))

    stats["counts"] = counts(doc)
    log.debug("Add counts")

    log.debug(f"text: {doc.text}")
    log.debug(80 * "_")

    # stats["sgrank"] = sorted(keyterms.sgrank(doc, ngrams=2, window_width=500), key=lambda x: x[1], reverse=True)
    # stats["textrank"] = sorted(keyterms.textrank(doc), key=lambda x: x[1], reverse=True)

    # stats["counts"] = txt.TextStats(doc).basic_counts

    return jsonify(stats)
