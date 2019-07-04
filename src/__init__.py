import logging
import os
import re

from flask import Flask, request, jsonify
import spacy

from .teidoc import TEIDocument
from .processing import pipeline, stats


log_file = os.path.join(os.path.dirname(__file__), "textstats.log")
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_file, filemode="w", format=FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/logs", methods=["GET"])
def logs():
    with open(log_file, "r") as f:
        logs = f.read()
    return logs


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
    text_stats = dict()

    # TODO: add names
    if td.entities():
        log.debug("Add entities")
        text_stats["entities"] = td.entities()
        for k, v in text_stats["entities"].items():
            text_stats[f"num_{k}"] = len(v)

    nlp = spacy.load("nl_core_news_sm")

    doc = nlp(pipeline(" ".join(td.text())))

    text_stats["counts"] = stats(doc)

    log.debug(f"processed text: {doc.text}")

    return jsonify(text_stats)
