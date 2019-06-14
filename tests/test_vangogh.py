from vangogh import teidoc as td


class TestTeiDoc:

    def test_teidoc(self):
        letter = td.TeiDoc("/home/niels/projects/vangogh/letters/let001.xml")
        assert isinstance(letter, td.TeiDoc)

    def test_text_extraction(self):
        letter = td.TeiDoc("/home/niels/projects/vangogh/letters/let001.xml")
        assert letter.text() is not None
        assert isinstance(letter.text(), str)
        assert letter.processed_text() is not None
        assert isinstance(letter.processed_text(), str)

        assert letter.text() != letter.processed_text()

    def test_header_extraction(self):
        letter = td.TeiDoc("/home/niels/projects/vangogh/letters/let001.xml")
        header = letter.metadata()
        assert isinstance(header, dict)
        assert header.get("author", None) != None
        assert header.get("addressee", None) != None
        assert header.get("place", None) != None
        assert header.get("date", None) != None
        assert header.get("year", None) != None

    def test_name_extraction(self):
        letter = td.TeiDoc("/home/niels/projects/vangogh/letters/let001.xml")
        names = letter.mentions()
        assert isinstance(names, list)
        for n in names:
            assert len(n) == 3

    def test_language_detection(self):
        lett_nl = td.TeiDoc("/home/niels/projects/vangogh/letters/let001.xml")
        lett_fr = td.TeiDoc(f"/home/niels/projects/vangogh/letters/let571.xml")
        assert lett_nl.lang() == 'nl'
        assert lett_fr.lang() == 'fr'
