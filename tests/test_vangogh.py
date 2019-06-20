#! /usr/bin/local/python3

from vangogh.teidoc import TeiDoc

class TestTeiDoc:

    def test_teidoc(self):
        letter = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            assert isinstance(d, TeiDoc)

    def test_text_extraction(self):
        letter = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        assert len(letter.text()) == 4
        rm = TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        assert len(rm.text()) == 3
        for d in [letter, rm]:
            assert d.text() is not None
            assert isinstance(d.text(), list)
            assert d.processed_text() is not None
            assert isinstance(d.processed_text(), str)

        assert letter.text() != letter.processed_text()

    def test_header_extraction(self):
        letter = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            header = d.metadata()
            assert isinstance(header, dict)
            assert header.get("id", None) != None
            assert header.get("author", None) != None
            assert header.get("addressee", None) != None
            assert header.get("place", None) != None
            assert header.get("date", None) != None

    def test_name_extraction(self):
        letter = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            names = d.entities()
            assert isinstance(names, list)
            for n in names:
                assert len(n) == 3

    def test_language_detection(self):
        lett_nl = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        lett_fr = TeiDoc("/Users/niels/projects/vangogh/letters/let571.xml")
        assert lett_nl.lang() == 'nl'
        assert lett_fr.lang() == 'fr'

import json
from vangogh.vangogh import VGCorpus

class TestFreqInfo:

    def output_is_json(self):
        corpus = VGCorpus(vg.CORPUS_DIR, n=50)
        assert isinstance(json.loads(corpus.frequencies()), dict)

    def n_matters(self):
        corpus_50 = VGCorpus(vg.CORPUS_DIR, n=50)
        assert len(list(corpus_50.get_letters())) == 50
        corpus_100 = VGCorpus(vg.CORPUS_DIR, n=100)
        assert len(list(corpus_100.get_letters())) == 100
