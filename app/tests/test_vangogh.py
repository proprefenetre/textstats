#! /usr/bin/local/python
import json
import os
import os.path
import pickle
from pprint import pprint
import pytest


@pytest.fixture
def teidocument():
    from src.teidoc import TEIDocument
    with open("/Users/niels/projects/vangogh/data/tei-example.xml", "rb") as f:
        return TEIDocument(f)


@pytest.fixture
def entities():
    from src.teidoc import TEIDocument
    return TEIDocument("/Users/niels/projects/vangogh/data/tei-example.xml").entities()


def test_teidoc(teidocument):
    from src.teidoc import TEIDocument
    assert isinstance(teidocument, TEIDocument)


# def test_get_nsmap(teidocument):
#     assert isinstance(teidocument.nsmap, dict)
#     assert "tei" in teidocument.nsmap
#     assert "vg" in teidocument.nsmap


# def test_entities(entities):
#     outp = {"topo": {"1", "2"},
#             "pers": {"442", "443", "524", "526", "642", "643"}}
#     assert entities == outp


# def test_text(teidocument):
#     original_text = """Den Haag, 29 september 1872. Waarde Theo, Dank voor je brief, het deed mij genoegen dat je weer goed aangekomen zijt. Ik heb je de eerste dagen ge- mist & het was mij vreemd je niet te vinden als ik s’mid- dags t’huis kwam. Wij hebben prettige dagen sa- men gehad, en tusschen de droppeltjes door toch nog al eens gewandeld & het een en ander gezien. Wat vreesselijk weer, je zult het wel benauwd hebben op je wandelingen naar Oisterwijk. Gisteren is het hard- draverij geweest ter gelegenheid van de tentoonstelling, maar de illumi- natie & het vuurwerk zijn uit gesteld, om het slechte weer, het is dus maar goed dat je niet gebleven zijt om die te zien. Groeten van de familie Haanebeek & Roos. Steeds je liefh. Vincent"""
#     assert original_text == teidocument.text()


# def test_unicode_characters(teidocument):
#     assert teidocument.unicode_characters()[0] == {
#         'character': '’',
#         'codepoint': '0x2019',
#         'category': 'Pf',
#         'name': 'RIGHT SINGLE QUOTATION MARK'
#     }


# def test_language_detection(teidocument):
#     assert teidocument.language() == 'nl'

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
