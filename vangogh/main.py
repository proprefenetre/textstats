from io import BytesIO
import json
from pathlib import Path

from lxml import etree
from flask import Flask, request, jsonify
from werkzeug import ImmutableMultiDict
import textacy as txt
import textacy.preprocess as prep
import textacy.keyterms as keyterms

# import xmltodict

from .teidoc import TeiDocument


app = Flask(__name__)


@app.before_request
def before_request():
    if True:
        print(
            f"HEADERS:\n {request.headers}\n"
            f"REQ_path: {request.path}\n"
            f"ARGS: {request.args}\n"
            f"DATA: {request.data}\n"
            f"FORM: {request.form}\n"
        )


@app.route("/", methods=["POST"])
def textstats():
    if request.data and isinstance(request.data, bytes):
        doc = TeiDocument(request.data)
    elif request.form:
        fn = request.form.get("file", None)
        if fn:
            doc = TeiDocument(fn)
        else:
            return "Incorrect request\nGot form but no key\n"

    stats = dict()
    stats["entities"] = doc.entities()
    for k, v in stats["entities"].items():
        stats[f"num_{k}"] = len(v)

    stats["unicode_entities"] = doc._unicode_characters()

    # remove / replace unicode entities by hand :(
    stats["text"] = doc.text(preprocess=True)

    # text = prep.normalize_unicode(text)
    # text = prep.normalize_whitespace(text)
    # text = prep.preprocess_text(text, no_currency_symbols=True)

    # doc = txt.make_spacy_doc(text)

    # stats["key terms"] = keyterms.textrank(doc, normalize="lemma", n_keyterms=5)
    # ts = txt.TextStats(doc)
    # stats["counts"] = ts.basic_counts
    # stats["readability"] = ts.readability_stats

    # stats["text"] = textV

    # return json.dumps(stats)
    return jsonify(stats)


@app.route("/files", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return "no file"
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
    return f"got yer file: {file.filename}"
