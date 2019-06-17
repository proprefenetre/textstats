from gensim import corpora, models
from itertools import islice
from pprint import pprint
import spacy
from spacy.lang.nl import STOP_WORDS as stops_nl
from spacy.lang.en import STOP_WORDS as stops_en
from spacy.lang.fr import STOP_WORDS as stops_fr
from pathlib import Path
import pickle
from teidoc import TeiDoc


CORPUS_DIR = "/home/niels/projects/vangogh/letters/"
MODEL_DIR =  "/home/niels/projects/vangogh/vangogh/models/"

nlp = spacy.load("nl_core_news_sm") # geen word vectors


def get_texts(path, nlp, n=False, languages=['nl']):
    corpus = Path(path).glob("*.xml")
    if n:
        corpus = islice(corpus, n)
    for d in corpus:
        td = TeiDoc(d.as_posix())
        if td.lang() not in languages:
            continue
        yield (td.metadata()["id"], nlp(td.processed_text()))


processed_texts_path = Path(MODEL_DIR + "processed_texts_all_nl.pickle")

if processed_texts_path.exists():
    docs, texts = pickle.load(processed_texts_path.open("rb"))
    print("pickle loaded")
else:
    docs, texts = zip(*get_texts(CORPUS_DIR, nlp))
    pickle.dump((docs, texts), processed_texts_path.open("wb"))
    print("pickle dumped")


tokenized_texts = []
for doc in texts:
    tokenized_texts.append([t.lemma_ for t in doc if not t.is_stop
                       and t.lemma_ not in stops_nl | stops_en | stops_fr
                       and not t.is_punct
                       and not t.is_space])


if Path(MODEL_DIR + "vg_dict_all_nl.dict").exists():
    vg_dict = corpora.Dictionary.load(MODEL_DIR + "vg_dict_all_nl.dict")
    print("dict loaded")
else:
    vg_dict = corpora.Dictionary(tokenized_texts)
    vg_dict.save(MODEL_DIR + "vg_dict_all_nl.dict")
    print("dict saved")


class VGCorpus:
    def __init__(self, tokens):
        self.dictionary = corpora.Dictionary(tokens)
        self.tokens = tokens

    def __iter__(self):
        for d in self.tokens:
            yield self.dictionary.doc2bow(d)


vg_dict.save(MODEL_DIR + "vg_dict_all_nl.dict")
corpus = VGCorpus(tokenized_texts)

# tfidf = models.TfidfModel(corpus)
# c_tfidf = tfidf[corpus]

# lsi = models.LsiModel(c_tfidf, id2word=corpus.dictionary, num_topics=5)
# c_lsi = lsi[c_tfidf] # apply LSI to the BoW vectors

# lda = models.LdaModel(c_tfidf, id2word=corp.dictionary, )

# for doc in zip([text[0] for text in texts], c_lsi):
#     md = doc[0].metadata()
#     topic = lsi.show_topic([max(doc[1], key=lambda x: x[1])[0]])
#     print(md["id"], topic)
