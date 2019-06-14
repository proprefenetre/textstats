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
        self.dictionary = corpora.Dictionary(texts)

    def __iter__(self):
        for d in self.texts:
            yield self.dictionary.doc2bow(d)


def texts(path, nlp, n=False):
    corpus = Path(path).glob("let*.xml")
    if n:
        corpus = islice(corpus, n)
    for d in corpus:
        td = TeiDoc(d.as_posix())
        if td.lang() == 'nl':
            yield (td, nlp(td.processed_text()))


corpus_dir = "/home/niels/projects/vangogh/letters/"

STOP_WORDS = stops_nl | stops_en | stops_fr

documents = []
tokenized_texts = []
for doc in texts(corpus_dir, spacy.load("nl_core_news_sm")):
    documents.append(doc[0])
    tokenized_texts.append(
        [
            t.lemma_
            for t in doc[1]
            if not t.is_stop
            and t.lemma_ not in STOP_WORDS
            and not t.is_punct
            and not t.like_num
            and not t.is_space
        ]
    )


corp = VGCorpus(tokenized_texts)

tfidf = models.TfidfModel(corp)
c_tfidf = tfidf[corp]

lsi = models.LsiModel(c_tfidf, id2word=corp.dictionary, num_topics=5)
c_lsi = lsi[c_tfidf]

for doc in zip(documents, c_lsi):
    md = doc[0].metadata()
    # fail: doc is een np.array
    topic = lsi.show_topic([max(doc[1], key=lambda x: x[1])[0]])
    print(md['letter_id'], topic)
