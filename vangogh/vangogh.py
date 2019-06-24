from itertools import islice
import json
from pathlib import Path
import pickle
from pprint import pprint

from corpus import VGLetter, VGCorpus
from teidoc import TeiDoc


CORPUS_DIR = "/Users/niels/projects/vangogh/letters/"
MODELS_DIR = "/Users/niels/projects/vangogh/models/"


def get_letters(corpus_path, n=False):
    if not Path(corpus_path).exists():
        raise FileNotFoundError
    corpus = Path(corpus_path).glob("*.xml")
    if n:
        corpus = islice(corpus, n)
    for p in corpus:
        td = TeiDoc(p.as_posix())
        yield VGLetter(td.metadata(), td.lang(), td.processed_text())


def load_letters(path, n=5):
    p = Path(path)
    if p.exists():
        with p.open("rb") as f:
            letters = pickle.load(f)
    else:
        letters = get_letters(CORPUS_DIR, n)
        with p.open("wb") as f:
            pickle.dump(list(letters), f)
    return letters


# docs = load_letters(MODELS_DIR + "vg-model-5let.pickle")
docs = get_letters(CORPUS_DIR, n=5)
crp = VGCorpus(list(docs))
data1 = json.loads(crp.frequencies())
