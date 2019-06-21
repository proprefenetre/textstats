#! /usr/local/bin/python3

from itertools import islice, chain
import json
from pprint import pprint
import os
from pathlib import Path
import spacy
from spacy.lang.nl import STOP_WORDS as stops_nl
from spacy.lang.en import STOP_WORDS as stops_en
from spacy.lang.fr import STOP_WORDS as stops_fr

from teidoc import TeiDoc

# TODO: load corpus_dir from a config file
CORPUS_DIR = "/Users/niels/projects/vangogh/letters/"

NLP_NL = spacy.load("nl_core_news_sm") # sm → geen word vectors
NLP_FR = spacy.load("fr_core_news_md")


def get_letters(corpus_path):
    if not os.path.exists(corpus_path):
        # TODO: dir not found error
        raise FileNotFoundError
    corpus = os.listdir(corpus_path)
    if n:
        corpus = islice(corpus, n)
    for p in corpus:
        yield TeiDoc(p.as_posix())
        # VGLetter(td.metadata()["id"], td.lang(), td.processed_text())


class VGLetter:
    def __init__(self, id, language, text):
        self.id = id
        self.language = language
        self.text = text
        if language == 'fr':
            self.doc = NLP_FR(text)
        else:
            self.doc = NLP_NL(text)
        self.sentences = [s.text for s in self.doc.sents]

    def wordcount(self):
        return len(self.text.strip().split())

    def sentcount(self):
        return len(self.sentences)

    def sentence_lengths(self):
        return [len(s.split()) for s in self.sentences]

    def avg_sentence_length(self):
        return sum(self.sentence_lengths()) / len(self.sentences)


class VGCorpus:
    def __init__(self, path, n=None):
        self.n = n


    def frequencies(self):
        texts = {}

        for text in self.get_letters():

            texts[text.id] = {
                "language": text.language,
                "n_words": text.wordcount(),
                "n_sentences": text.sentcount(),
                "sentence_lengths": text.sentence_lengths(),
                "avg_sentence_length": text.avg_sentence_length(),
                "keywords": [],
            }

        corpus = {
            "n_texts": len(texts),
            "n_words": sum(t["n_words"] for t in texts.values()),
            "n_sentences": sum(t["n_sentences"] for t in texts.values()),
            # "avg_sentence_length": sum(sum(t["sentence_lengths"]) for t in texts) / len(texts),
            "avg_sentences_letter": sum(t["n_sentences"] for t in texts.values()) / len(texts),
            "avg_words_letter": sum(t["n_words"] for t in texts.values()) / len(texts),
            "texts": texts,
        }

        # for text in letters.values():
        #     corpus["n_letters"] += 1
        #     corpus["n_words"] += text["n_words"]
        #     corpus["n_sentences"] += text["n_sentences"]
        #     corpus["avg_words_letter"] = / total_letters
        # avg_sentences_letter =  total_sentences / total_letters

        return json.dumps(corpus)
