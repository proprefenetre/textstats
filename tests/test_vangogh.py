from vangogh import teidoc as td


class TestTeiDoc:

    def test_text_extraction(self):
        letter = td.TeiDoc(f"/home/niels/projects/vangogh/letters/let001.xml")
        layers = letter.text()
        assert isinstance(layers, dict)
        assert len(layers) == 4
        assert all(key in layers for key in ["original", "translation",
                                             "textualNotes", "notes"])
        assert all(isinstance(v, str) for v in layers.values())
