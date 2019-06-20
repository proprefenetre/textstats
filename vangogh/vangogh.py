#! /usr/local/bin/python3

from itertools import islice, chain
import json
import spacy
from spacy.lang.nl import STOP_WORDS as stops_nl
from spacy.lang.en import STOP_WORDS as stops_en
from spacy.lang.fr import STOP_WORDS as stops_fr
from pathlib import Path

from vangogh.teidoc import TeiDoc


CORPUS_DIR = "/Users/niels/projects/vangogh/letters/"
# MODEL_DIR =  "/home/niels/projects/vangogh/vangogh/models/"

nlp = spacy.load("nl_core_news_sm") # sm → geen word vectors
nlp_fr = spacy.load("fr_core_news_md")


class VGLetter:
    def __init__(self, id, language, text):
        self.id = id
        self.language = language
        self.text = text

    def wordcount(self):
        return len(self.text.split())

    def sentcount(self):
        return len(self.text.sents)

    def avg_sentence_length(self):
        return sum([len(s.text.split()) for s in self.text.sents]) / len(self.text.sents)


class VGCorpus:
    def __init__(self, path, languages=["nl"], n=None):
        self.path = path
        # TODO load appropriate spacy models for each language
        self.languages = languages
        self.n = n

    def get_letters(self):
        corpus = Path(self.path).glob("*.xml")
        if self.n:
            corpus = islice(corpus, self.n)
        for p in corpus:
            td = TeiDoc(p.as_posix())
            yield VGLetter(td.metadata()["id"], td.lang(), nlp(td.processed_text()))

    def avg_sentence_length(self):
        sentences = list(chain(*(d.sents for d in (txt for _, _, txt in self.get_letters()))))
        avg_sent_length = sum([len(s.text.split()) for s in sentences]) / len(sentences)

    def frequencies(self):
        freq = {}
        for l in self.get_letters():
            freq[l.id] = {
                "n_words": l.wordcount(),
                "n_sentences": l.sentcount(),
                "avg_sentence_length": l.avg_sentence_length(),
                "keywords": [],
            }

        total_words = sum(l["n_words"] for l in freq)
        total_sentences = sum(l["n_sentences"] for l in freq)
        total_letters = len(freq)
        avg_words_letter = total_words / total_letters
        avg_sentences_letter =  total_sentences / total_letters

        freq["corpus"] = {
            "n_letters": total_letters,
            "n_words": total_words,
            "n_sentences": total_sentences,
            "avg_sentence_length":  self.avg_sentence_length(),
            "avg_sentences_letter": avg_sentences_letter,
            "avg_words_letter": avg_words_letter,
        }

        return json.dumps(freq)
