#! /usr/bin/local/python
import json
import os
import os.path
import pickle
import pytest


@pytest.fixture
def teidocument():
    from vangogh.teidoc import TeiDocument
    return TeiDocument("/Users/niels/projects/vangogh/data/tei-example-facsimiles.xml")


@pytest.fixture
def metadata():
    from vangogh.teidoc import TeiDocument
    return TeiDocument("/Users/niels/projects/vangogh/data/tei-example-facsimiles.xml").metadata()


def test_teidoc(teidocument):
    from vangogh.teidoc import TeiDocument
    assert isinstance(teidocument, TeiDocument)


def test_get_nsmap(teidocument):
    assert isinstance(teidocument.nsmap, dict)
    assert "tei" in teidocument.nsmap
    assert "vg" in teidocument.nsmap


def test_metadata(metadata):
    assert isinstance(metadata, tuple)
    # assert "fileDesc" in metadata
    # assert "sourceDesc" in metadata["fileDesc"]
    print(len(metadata))





# class TestFreqInfo:

#     def test_output_is_json(self):
#         corpus = VGCorpus(CORPUS_DIR)
#         assert isinstance(json.loads(corpus.frequencies()), dict)

#     def test_letter_is_VGLetter(self):
#         letter = list(VGCorpus(CORPUS_DIR, n=1).get_letters())[0]
#         assert isinstance(letter, VGLetter)
#         assert all(hasattr(letter, a) for a in ['id', 'language', 'text',
#                                                'wordcount', 'sentcount', 'avg_sentence_length'])

#     def test_n_matters(self):
#         corpus_5 = VGCorpus(CORPUS_DIR, n=5)
#         assert len(list(corpus_5.get_letters())) == 5
#         freq = json.loads(corpus_5.frequencies())
#         assert freq["corpus"]["n_letters"] == 5

#         corpus_100 = VGCorpus(CORPUS_DIR, n=100)
#         assert len(list(corpus_100.get_letters())) == 100
#         freq = json.loads(corpus_100.frequencies())
#         assert freq["corpus"]["n_letters"] == 100

#         corpus_all = VGCorpus(CORPUS_DIR)
#         assert len(list(corpus_all.get_letters())) == 928
#         freq = json.loads(corpus_all.frequencies())
#         assert freq["corpus"]["n_letters"] == 928
