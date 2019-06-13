from vangogh import teidoc as td


class TestTeiDoc:

    letter = td.TeiDoc(f"/home/niels/projects/vangogh/letters/let001.xml")
    layers = letter.text()

    def test_teidoc(self):
        assert isinstance(self.letter, td.TeiDoc)
        assert hasattr(self.letter, 'xml')
        assert hasattr(self.letter, 'layers')

    def test_layers(self):
        assert isinstance(self.layers, dict)
        assert len(self.layers) == 3
        assert all(key in self.layers for key in ["original", "translation", "notes"])

    def test_text_extraction(self):
        assert all(isinstance(v, str) for v in self.layers.values())
        assert all(len(v) > 0 for v in self.layers.values())
        text = self.letter.preprocess()
        assert isinstance(text, str)

    def test_header_extraction(self):
        header = self.letter.metadata()
        assert isinstance(header, dict)
        assert header.get("author", None) != None
        assert header.get("addressee", None) != None
        assert header.get("place", None) != None
        assert header.get("date", None) != None
        assert header.get("year", None) != None
