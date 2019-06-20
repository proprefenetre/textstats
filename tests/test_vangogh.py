#! /usr/bin/local/python3

from vangogh import teidoc as td


class TestTeiDoc:

    def test_teidoc(self):
        letter = td.TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = td.TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            assert isinstance(d, td.TeiDoc)

    def test_text_extraction(self):
        letter = td.TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        assert len(letter.text()) == 4
        rm = td.TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        assert len(rm.text()) == 3
        for d in [letter, rm]:
            assert d.text() is not None
            assert isinstance(d.text(), list)
            assert d.processed_text() is not None
            assert isinstance(d.processed_text(), str)

        assert letter.text() != letter.processed_text()

    def test_header_extraction(self):
        letter = td.TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = td.TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            header = d.metadata()
            assert isinstance(header, dict)
            assert header.get("id", None) != None
            assert header.get("author", None) != None
            assert header.get("addressee", None) != None
            assert header.get("place", None) != None
            assert header.get("date", None) != None

    def test_name_extraction(self):
        letter = td.TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = td.TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            names = d.entities()
            assert isinstance(names, list)
            for n in names:
                assert len(n) == 3

    def test_language_detection(self):
        lett_nl = td.TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        lett_fr = td.TeiDoc("/Users/niels/projects/vangogh/letters/let571.xml")
        assert lett_nl.lang() == 'nl'
        assert lett_fr.lang() == 'fr'

import json
from vangogh import vangogh as vg

class TestFreqInfo:

    def output_is_json(self):
        corpus = vg.VGCorpus
        assert json.loads
