#! /usr/bin/local/python
import json
import os
import os.path
import pickle
import pytest


from vangogh.teidoc import TeiDoc
from vangogh.corpus import VGCorpus


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
            assert isinstance(header.get("name", None), str)
            assert isinstance(header.get("author", None), str)
            assert isinstance(header.get("addressee", None), str)
            assert isinstance(header.get("place", None), str)
            assert isinstance(header.get("date", None), str)

    def test_name_extraction(self):
        letter = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        rm = TeiDoc("/Users/niels/projects/vangogh/letters/RM01.xml")
        for d in [letter, rm]:
            names = d.metadata()["entities"]
            assert isinstance(names, list)
            for n in names:
                assert len(n) == 3

    def test_language_detection(self):
        lett_nl = TeiDoc("/Users/niels/projects/vangogh/letters/let001.xml")
        lett_fr = TeiDoc("/Users/niels/projects/vangogh/letters/let571.xml")
        assert lett_nl.lang() == 'nl'
        assert lett_fr.lang() == 'fr'


@pytest.mark.dontskip
class TestCorpus:
    tmp_model = "/tmp/test-model.pickle"
    corpus_path = "/Users/niels/projects/vangogh/letters/"
    n_letters = 3

    def test_create(self):
        C = VGCorpus(self.corpus_path)
        C.create(self.n_letters, save=True)
        assert len(C.letters) == self.n_letters
        assert os.path.exists(self.corpus_path + "van_gogh.pickle")
        assert pickle.load(self.corpus_path + "van_gogh.pickle") == C.letters

        os.remove(self.corpus_path + "van_gogh.pickle")

    def test_create_path(self):
        C = VGCorpus(self.corpus_path)
        C.create(self.n_letters, save=self.tmp_model)
        assert C.letters == self.n_letters
        assert os.path.exists(self.tmp_model)
        assert pickle.load(self.tmp_model) == C.letters

        os.remove("/tmp/test-model.pickle")

    def test_create_no_save(self):
        C = VGCorpus(self.corpus_path)
        C.create(self.n_letters, save=False)
        assert C.letters == self.n_letters
        assert os.path.exists(self.tmp_model) is False

        os.remove(self.tmp_model)

    def test_load(self):
        C = VGCorpus(self.corpus_path)
        C.create(self.n_letters, save=self.tmp_model)

        D = VGCorpus()
        D.load(self.tmp_model)
        assert D.letters == C.letters

        os.remove(self.tmp_model)


    # def test_pickling(self):
    #     tmp_path =
    #     n_letters = 3

    #     C =
    #     load_letters(tmp_path, n=n_letters)
    #     assert os.path.exists("/tmp/test-model.pickle")
    #     os.remove(tmp_path)

    # def test_loading(self):
    #     tmp_path = "/tmp/test-model.pickle"
    #     n_letters = 3

    #     letters = load_letters(tmp_path, n=n_letters)
    #     assert isinstance(letters, list)
    #     assert len(letters) == n_letters

    #     with open(tmp_path, "rb") as f:
    #         pickled_lets = pickle.load(f)
    #     assert isinstance(pickled_lets, list)
    #     assert len(pickled_lets) == n_letters

    #     assert pickled_lets == letters
    #     os.remove(tmp_path)

    # def test_no_persistence(self):
    #     n_letters = 3
    #     letters = load_letters(n=n_letters)
    #     assert isinstance(letters, list)
    #     assert len(letters) == n_letters


class TestFreqInfo:

    def test_output_is_json(self):
        corpus = VGCorpus(CORPUS_DIR)
        assert isinstance(json.loads(corpus.frequencies()), dict)

    def test_letter_is_VGLetter(self):
        letter = list(VGCorpus(CORPUS_DIR, n=1).get_letters())[0]
        assert isinstance(letter, VGLetter)
        assert all(hasattr(letter, a) for a in ['id', 'language', 'text',
                                               'wordcount', 'sentcount', 'avg_sentence_length'])

    def test_n_matters(self):
        corpus_5 = VGCorpus(CORPUS_DIR, n=5)
        assert len(list(corpus_5.get_letters())) == 5
        freq = json.loads(corpus_5.frequencies())
        assert freq["corpus"]["n_letters"] == 5

        corpus_100 = VGCorpus(CORPUS_DIR, n=100)
        assert len(list(corpus_100.get_letters())) == 100
        freq = json.loads(corpus_100.frequencies())
        assert freq["corpus"]["n_letters"] == 100

        corpus_all = VGCorpus(CORPUS_DIR)
        assert len(list(corpus_all.get_letters())) == 928
        freq = json.loads(corpus_all.frequencies())
        assert freq["corpus"]["n_letters"] == 928
