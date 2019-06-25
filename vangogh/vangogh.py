from itertools import islice
from pathlib import Path
import pickle
from pprint import pprint

from utils import timethis
from corpus import VGCorpus
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
        yield (td.metadata(), td.lang(), td.processed_text())


@timethis
def load_letters(path=None, n=False):
    if path is None:
        return list(get_letters(CORPUS_DIR, n))
    p = Path(path)
    if p.exists():
        with p.open("rb") as f:
            letters = pickle.load(f)
    else:
        letters = list(get_letters(CORPUS_DIR, n))
        with p.open("wb") as f:
            pickle.dump(letters, f)
    return letters


pprint(VGCorpus(load_letters(None, n=5)).frequencies())
# VGCorpus(load_letters(None, n=5)).frequencies_loop()
