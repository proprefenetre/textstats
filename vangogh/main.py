import json

from flask import Flask, request
import textacy as txt
import textacy.preprocess as prep
import textacy.keyterms as keyterms

from .teidoc import TeiDocument


app = Flask(__name__)


@app.route("/", methods=["POST"])
def textstats():
    xml = request.form["xml"]
    print(type(xml))

    td = TeiDocument(xml)
    stats = dict()

    stats["entities"] = td.entities()
    for k, v in stats["entities"].items():
        stats[f"num_{k}"] = len(v)

    text = prep.normalize_unicode(td.text(), "NFKC")
    text = prep.normalize_whitespace(text)
    text = prep.preprocess_text(text, no_currency_symbols=True)

    doc = txt.make_spacy_doc(text)

    stats["key terms"] = keyterms.textrank(doc, normalize="lemma", n_keyterms=5)
    ts = txt.TextStats(doc)
    stats["counts"] = ts.basic_counts
    stats["readability"] = ts.readability_stats

    return json.dumps(stats)
