from itertools import islice
import logging
import os
import re

from flask import Flask, request, jsonify, session
import langdetect
import spacy
from teidocument import TEIDocument

from .processing import pipeline, Stats


log_file = os.path.join(os.path.dirname(__file__), "textstats.log")
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_file, filemode="w", format=FORMAT, level=logging.DEBUG)
log = logging.getLogger(__name__)

app = Flask(__name__)


def _head(obj, n=10):
    if hasattr(obj, "read") or hasattr(obj, '__getitem__'):
        return list(islice(obj, n))
    else:
        raise TypeError(f"Object of type {type(obj)} does not support indexing")


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


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
        elif request.files:
            data = request.files.get("file", None)
            if not data:
                log.warning("No file provided")
            else:
                log.debug(f"file provided: {data}")
            layer = request.form.get("layer", False)
            entities = False
        else:
            raise InvalidUsage("No document provided", status_code=400)

    try:
        td = TEIDocument(data)
    except AssertionError as err:
        Raise InvalidUsage(f"Invalid XML: {_head(data)}")

    text_stats = dict()

    if entities:
        log.debug(f"Entities {entities}")
        text_stats["entities"] = td.entities()
        for k, v in text_stats["entities"].items():
            text_stats[f"num_{k}"] = len(v)

    if layer:
        try:
            text = " ".join(td.text()[layer])
        except KeyError:
            raise InvalidUsage(f"'{layer}' not in layers", status_code=400)
    else:
        text = " ".join(t[0] for t in td.text().values())

    models = {"en": "en_core_web_sm", "fr": "fr_core_news_sm", "nl": "nl_core_news_sm"}

    lang = langdetect.detect(text)

    log.debug(f"language: {lang}")

    nlp = spacy.load(models[lang])

    doc = nlp(pipeline(text))

    try:
        text_stats.update(Stats(doc).all_stats(n=10, r=2))
    except AttributeError:
        raise InvalidUsage("Document is too short", status_code=400)

    return jsonify(text_stats)
