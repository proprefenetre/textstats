from flask import Flask, request, jsonify
import spacy
import textacy as txt
import textacy.preprocess as prep
import textacy.keyterms as keyterms

# import xmltodict

from .teidoc import TeiDocument

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
    stats["entities"] = td.entities()
    for k, v in stats["entities"].items():
        stats[f"num_{k}"] = len(v)

    # stats["unicode_entities"] = td._unicode_characters()

    text = td.text()

    # TODO: remove / replace specific unicode entities by hand :(

    text = prep.normalize_unicode(text)
    text = prep.normalize_whitespace(text)
    text = prep.preprocess_text(text, no_currency_symbols=True)

    nlp = spacy.load("nl_core_news_sm")
    doc = nlp(text)

    stats["key terms"] = sorted(keyterms.textrank(doc, normalize="lemma", n_keyterms=10),
                                key=lambda x: x[1], reverse=True)
    ts = txt.TextStats(doc)
    stats["counts"] = ts.basic_counts

    stats["text"] = text

    return jsonify(stats)