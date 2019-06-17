from gensim import corpora, models
from itertools import islice, chain
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
        yield (td.metadata(), nlp(td.processed_text()))


processed_texts_path = Path(MODEL_DIR + "processed_texts_all_nl.pickle")

if processed_texts_path.exists():
    docs, texts = pickle.load(processed_texts_path.open("rb"))
    print("pickle loaded")
else:
    docs, texts = zip(*get_texts(CORPUS_DIR, nlp))
    pickle.dump((docs, texts), processed_texts_path.open("wb"))
    print("pickle dumped")

# sentence lenght
sentences = list(chain(*[d.sents for d in texts]))
avg_sent_length = sum([len(s.text.split()) for s in sentences]) / len(sentences)

sent_length_letters = {}
for let, text in zip(docs, texts):
    sents = [s.text.split() for s in text.sents]
    avg_length = sum([len(s) for s in sents]) / len(sents)
    sent_length_letters[let] = avg_length


stops = stops_nl | stops_en | stops_fr

tokenized_texts = []
for doc in texts:
    tokenized_texts.append([t.lemma_ for t in doc if not t.is_stop
                       and t.lemma_ not in stops
                       and not t.is_punct
                       and not t.is_space])

from sklearn.feature_extraction.text import CountVectorizer
docs = [" ".join(t) for t in tokenized_texts]
cv = CountVectorizer(max_df=.85, stop_words=stops)
word_count_vector = cv.fit_transform(docs)
# if Path(MODEL_DIR + "vg_dict_all_nl.dict").exists():
#     vg_dict = corpora.Dictionary.load(MODEL_DIR + "vg_dict_all_nl.dict")
#     print("dict loaded")
# else:
#     vg_dict = corpora.Dictionary(tokenized_texts)
#     vg_dict.save(MODEL_DIR + "vg_dict_all_nl.dict")
#     print("dict saved")


# class VGCorpus:
#     def __init__(self, tokens):
#         self.dictionary = corpora.Dictionary(tokens)
#         self.tokens = tokens

#     def __iter__(self):
#         for d in self.tokens:
#             yield self.dictionary.doc2bow(d)


# vg_dict.save(MODEL_DIR + "vg_dict_all_nl.dict")
# corpus = VGCorpus(tokenized_texts)

# # tfidf = models.TfidfModel(corpus)
# # c_tfidf = tfidf[corpus]
