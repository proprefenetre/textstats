import json

from flask import Flask, request
import textacy

from teidoc import TeiDocument


app = Flask(__name__)


@app.route("/", methods=["POST"])
def textstats():
    xml = request.form["xml"]
    stats = dict()

    return json.dumps(stats)
