from functools import wraps
import time

import spacy
from spacy.lang.nl import Dutch
from spacy.lang.fr import French


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__module__}.{func.__name__} : {end-start}")
        return r

    return wrapper


NLP_NL = spacy.load("nl_core_news_sm")  # sm → geen word vectors
NLP_FR = spacy.load("fr_core_news_md")


class VGLetter:
    def __init__(self, metadata, language, text, sentence_detection="nlp"):
        self.metadata = metadata
        self.language = language
        if language == "fr":
            self.doc = NLP_FR(text)
        else:
            self.doc = NLP_NL(text)
        self.sentences = [s.text for s in self.doc.sents]
        self.text = " ".join(self.sentences).strip()

    def _detect_sentences(self):
        pass

    def word_count(self):
        return len(self.text.split())

    def sentence_count(self):
        return len(self.sentences)

    def sentence_lengths(self):
        return [len(s.split()) for s in self.sentences]

    def avg_sentence_length(self):
        return sum(self.sentence_lengths()) / len(self.sentences)

    def keywords(self):
        pass


class VGCorpus:
    def __init__(self, letters):
        self.letters = letters

    @timethis
    def frequencies(self):
        texts = {
            text.metadata["name"]: {
                "metadata": text.metadata,
                "language": text.language,
                "word_count": text.word_count(),
                "sentence_count": text.sentence_count(),
                "avg_sentence_length": text.avg_sentence_length(),
                "keywords": text.keywords(),
            }
            for text in self.letters
        }

        corpus = {
            "num_texts": len(self.letters),
            "word_count": sum(t.word_count() for t in self.letters),
            "sentence_count": sum(t.sentence_count() for t in self.letters),
        }

        corpus["avg_sentence_length"] = (
            sum(sum(letter.sentence_lengths()) for letter in self.letters)
            / corpus["sentence_count"]
        )
        corpus["avg_words_per_letter"] = corpus["word_count"] / corpus["num_texts"]
        corpus["avg_sentences_per_letter"] = (
            corpus["sentence_count"] / corpus["num_texts"]
        )

        return {"corpus": corpus, "texts": texts}

    @timethis
    def frequencies_loop(self):
        texts = {}
        corpus = {"num_texts": len(self.letters), "word_count": 0, "sentence_count": 0}

        for text in self.letters:

            text.metadata["name"]: {
                "metadata": text.metadata,
                "language": text.language,
                "word_count": text.word_count(),
                "sentence_count": text.sentence_count(),
                "avg_sentence_length": text.avg_sentence_length(),
                "keywords": text.keywords(),
            }
            corpus["word_count"] += text.word_count()
            corpus["sentence_count"] += text.sentence_count()

        corpus["avg_sentence_length"] = (
            sum(sum(letter.sentence_lengths()) for letter in self.letters)
            / corpus["sentence_count"]
        )
        corpus["avg_words_per_letter"] = corpus["word_count"] / corpus["num_texts"]
        corpus["avg_sentences_per_letter"] = (
            corpus["sentence_count"] / corpus["num_texts"]
        )

       return {"corpus": corpus, "texts": texts}
