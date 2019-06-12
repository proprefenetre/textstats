from constants import VG_UNICODE_PUNCT
from lxml import etree
import re
import string
import sys
import unicodedata

class TeiDoc:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True), codepoints=VG_UNICODE_PUNCT):
        self.xml = etree.parse(xml, parser)
        self.codepoints = codepoints

    def metadata(self):
        """
        Extract metadata from the TEI.
        returns: dict
        """
        pass

    def people(self):
        """
        Extract names of people mentioned in the letters
        """
        names = {}
        find_names = etree.ETXPath("//{http://www.tei-c.org/ns/1.0}rs")
        for e in find_names(self.xml):
            names[re.sub(r"\s+", r" ", e.text)] = e.get("key")
        return names

    def text(self):
        """
        Extract text from the xml.

        Returns: dict with text layers and notes
        """
        text_tree = etree.ElementTree(self.xml.find("{http://www.tei-c.org/ns/1.0}text"))
        self.layers = {}
        for e in text_tree.findall(".//{http://www.tei-c.org/ns/1.0}div"):
            self.layers[e.get("type")] = "".join(e.xpath(".//text()"))
        return self.layers

    def _whitespace(self, text):
        return re.sub("\s+", " ", text).strip()

    def _apostrophes(self, text):
        """
        RIGHT SINGLE QUOTATION MARK is used in contractions. Replace them with
        ascii apostrophes to keep the contractions intact.
        """
        return re.sub("\u2019", "'", text)

    def _unicode(self, text):
        """
        Remove unicode. Keep other punctuation for sentence boundary recognition

        """
        return re.sub(rf"[{''.join(self.codepoints)}]", "", text)

    def _contractions(self, text):
        """
        Remove contractions, e.g.:
            t'huis → thuis
            't → het
            d' → de
        """
        patterns =[
            ("\b(t)'(\w+)", "\g<1>\g<2>"),
            ("d'(\w+)", "de \g<1>" )
        ]
        for pat in patterns:
            text = re.sub(pat[0], pat[1], text)

        return text


    def _diacritics(self, text):
        """
           Replace characters with diacritical marks with their ascii equivalents
           """
        return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))

    def preprocess(self, funcs=["apostrophes", "unicode", "diacritics", "contractions", "whitespace"]):

        dispatch = {"whitespace": self._whitespace,
                    "apostrophes": self._apostrophes,
                    "unicode": self._unicode,
                    "contractions": self._contractions,
                    "diacritics": self._diacritics,}

        text = self.layers["original"]
        for fun in funcs:
            text = dispatch[fun](text)
        return text
