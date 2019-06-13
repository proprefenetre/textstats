from gensim import corpora, models
from itertools import islice
from pprint import pprint
import spacy
from spacy.lang.nl import STOP_WORDS as stops_nl
from spacy.lang.en import STOP_WORDS as stops_en
from spacy.lang.fr import STOP_WORDS as stops_fr
from pathlib import Path
from teidoc import TeiDoc


class VGCorpus:
    def __init__(self, texts):
        self.texts = texts
        self.dictionary = corpora.Dictionary(self.texts)

    def __iter__(self):
        for d in self.texts:
            yield self.dictionary.doc2bow(d)


def texts(path, nlp, n=False):
    corpus = Path(path).glob("let*.xml")
    if n:
        corpus = islice(corpus, n)
    for d in corpus:
        yield nlp(TeiDoc(d.as_posix()).preprocess())


corpus_dir = "/home/niels/projects/vangogh/letters/"

nlp = spacy.load('nl_core_news_sm')

stop_words = stops_nl | stops_en | stops_fr

tokenized_texts = []
for doc in texts(corpus_dir, nlp, n=50):
    tokenized_texts.append([t.lemma_ for t in doc if not t.is_stop \
                            and not t.is_punct \
                            and not t.like_num \
                            and not t.is_space \
                            and t.lemma_ not in stop_words])

# d = corpora.Dictionary(tokenized_texts)
# d.save(f"{corpus_dir}vg_50.dict")
# corpus = [d.doc2bow(t) for t in tokenized_texts]
# corpora.MmCorpus.serialize(f"{corpus_dir}vg_50.mm", corpus)

d = corpora.Dictionary.load(f"{corpus_dir}vg_50.dict")
corpus = corpora.MmCorpus(f"{corpus_dir}vg_50.mm")

tfidf = models.TfidfModel(corpus)
c_tfidf = tfidf[corpus]
lsi = models.LsiModel(c_tfidf, id2word=d, num_topics=5)
c_lsi = lsi[c_tfidf]
