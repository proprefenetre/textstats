import logging
import os
import re

from flask import Flask, request, jsonify, session
import langdetect
import spacy

from .teidoc import TEIDocument
from .processing import pipeline, Stats


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
    log.debug(
        f"HEADERS:\n{request.headers}\n"
        f"REQ_path: {request.path}\n"
        f"ARGS: {request.args}\n"
        f"DATA: {request.data}\n"
        f"FORM: {list(request.form.keys())}\n"
        f"FILES: {request.files}\n"
    )

    if request.method == "POST":
        if request.data and isinstance(request.data, bytes):
            data = request.data
        elif request.form:
            data = request.files.get("file", None)
            if not data:
                log.warning("No file provided")
            else:
                log.debug(f"file provided: {data}")
            layer = request.form.get("layer", False)
            entities = request.form.get("entities", False)
            log.debug(f"Merge layers: {layer}\nentities: {entities}")
        else:
            return "No document specified\n"

    td = TEIDocument()
    td.load(data)
    log.debug(
        f"TEIDocument loaded: {request.files.get('filename', None)}:{td.docinfo()}"
    )
    text_stats = dict()

    if entities:
        log.debug(f"Entities {entities}")
        text_stats["entities"] = td.entities()
        for k, v in text_stats["entities"].items():
            text_stats[f"num_{k}"] = len(v)

    if layer:
        if layer in td.text().keys():
            text = " ".join(td.text().get(layer))
        else:
            log.debug(f"'{layer}' not in layers")
            return f"Invalid text layer: '{layer}'"
    else:
        text = " ".join(td.text().values())

    log.debug(f"text: {text[:40]}")

    models = {"en": "en_core_web_sm", "fr": "fr_core_news_sm", "nl": "nl_core_news_sm"}

    lang = langdetect.detect(text)

    log.debug(f"language: {lang}")

    nlp = spacy.load(models[lang])

    doc = nlp(pipeline(text))

    text_stats.update(Stats(doc).all_stats(n=10, r=2))

    return jsonify(text_stats)
