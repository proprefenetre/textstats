from lxml import etree
import re
import string
import sys
import unicodedata

class TeiDoc:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True)):
        self.xml = etree.parse(xml, parser)
        self.namespaces = {"tei": "{http://www.tei-c.org/ns/1.0}",
                           "vg": "http://www.vangoghletters.org/ns/"}

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
        layers = {}
        for e in text_tree.findall(".//{http://www.tei-c.org/ns/1.0}div"):
            layers[e.get("type")] = "".join(e.xpath(".//text()"))
        return layers

    def _whitespace(self, text):
        return re.sub("\s+", " ", text).strip()

    def _apostrophes(self, text):
        """
        Replace RIGHT SINGLE QUOTATION MARK with ascii apostrophe
        """
        return re.sub("\u2019", "'", text)

    def _punctuation(self, text):
        """
        Remove unicode. Keep other punctuation for sentence boundary recognition

        """
        unicode_punct = [
            '\u00a0', # NO-BREAK SPACE
            '\u00a3', # POUND SIGN
            '\u00b0', # DEGREE SIGN
            '\u00b1', # PLUS-MINUS SIGN
            '\u00b4', # ACUTE ACCENT
            '\u00b7', # MIDDLE DOT
            '\u00bb', # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
            '\u00bd', # VULGAR FRACTION ONE HALF
            '\u2013', # EN DASH
            '\u2014', # EM DASH
            '\u2018', # LEFT SINGLE QUOTATION MARK
            '\u201c', # LEFT DOUBLE QUOTATION MARK
            '\u201d', # RIGHT DOUBLE QUOTATION MARK
            '\u2026', # HORIZONTAL ELLIPSIS
            '\u2500', # BOX DRAWINGS LIGHT HORIZONTAL
            '\u25a1', # WHITE SQUARE
            '\u2019', # RIGHT SINGLE QUOTATION MARK
        ]

        return re.sub(rf"[{''.join(unicode_punct)}]", "", text)

    def _contractions(self, text, patterns=[(r"\b(t)'(\w+)", "\g<1>\g<2>"), (r"d'(\w+)", "de \g<2>" )]):
        """
        Remove contractions, e.g.:
            t'huis → thuis
            't → het
            d' → de
        """
        for pat in patterns:
            text = re.sub(pat[0], pat[1], text)
        return text

    def _diacritics(self, text):
        """
        Replace characters with diacritical marks with their ascii equivalents
        """
        return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))

    def preprocess(self, funcs=["apostrophes", "punctuation", "diacritics", "contractions", "whitespace"]):
        """
        preprocess the text,

        """
        dispatch = {"whitespace": self._whitespace,
                    "apostrophes": self._apostrophes,
                    "punctuation": self._punctuation,
                    "contractions": self._contractions,
                    "diacritics": self._diacritics,}


        for l in levels:
            text = dispatch[l](text)
        return text
