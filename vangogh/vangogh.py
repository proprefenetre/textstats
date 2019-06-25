from itertools import islice
from pathlib import Path
import pickle
from pprint import pprint
from functools import wraps
import time

from corpus import VGLetter, VGCorpus
from teidoc import TeiDoc


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__module__}.{func.__name__} : {end-start}")
        return r

    return wrapper


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


@timethis
def load_letters(path, n=False):
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


# docs = get_letters(CORPUS_DIR, n=5)
crp = VGCorpus(load_letters(None, n=5)).frequencies()
pprint(crp["corpus"])
