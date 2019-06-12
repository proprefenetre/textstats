from lxml import etree
import re
import string
import sys
import unicodedata

VG_PUNCT = {
    "\u00a0": " ",  # NO-BREAK SPACE
    "\u00a3": "",    # POUND SIGN
    "\u00b0": "",    # DEGREE SIGN
    "\u00b1": "",    # PLUS-MINUS SIGN
    "\u00b4": "",    # ACUTE ACCENT
    "\u00b7": "",    # MIDDLE DOT
    "\u00bb": "",    # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    "\u00bd": "",    # VULGAR FRACTION ONE HALF
    "\u2013": "",    # EN DASH
    "\u2014": "",    # EM DASH
    "\u2018": "",    # LEFT SINGLE QUOTATION MARK
    "\u201c": "",    # LEFT DOUBLE QUOTATION MARK
    "\u201d": "",    # RIGHT DOUBLE QUOTATION MARK
    "\u2026": "",    # HORIZONTAL ELLIPSIS
    "\u2500": "",    # BOX DRAWINGS LIGHT HORIZONTAL
    "\u25a1": "",    # WHITE SQUARE
    "\u2019": "'",   # RIGHT SINGLE QUOTATION MARK
    "&"     : "en",
    "\s+"   : " ",
    "-"     : "",
    "_"     : "",
    "t'"    : "t",
    "d'"    : "de ",
 }


class TeiDoc:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True)):
        self.xml = etree.parse(xml, parser)

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
        Returns: dict with text layers  and notes:
        {'original': ...,
         'translation': ...,
         'textualNotes': ...,
         'notes': ...}
        """
        text_tree = etree.ElementTree(self.xml.find("{http://www.tei-c.org/ns/1.0}text"))
        self.layers = {}
        for e in text_tree.findall(".//{http://www.tei-c.org/ns/1.0}div"):
            if e.get("type") == "original":
                e.remove(e.findall(".//{http://www.tei-c.org/ns/1.0}div")[0])
            self.layers[e.get("type")] = "".join(e.xpath(".//text()"))

        return self.layers

    def _punctuation(self, text):
        """
        Remove unicode. Keep other punctuation for sentence boundary recognition

        """
        for k, v in VG_PUNCT.items():
            text = re.sub(k, v, text)
        return text


    def _diacritics(self, text):
        return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))

    def preprocess(self, funcs=["punctuation", "diacritics", "contractions"]):

        text = self._punctuation(self._diacritics(self.layers["original"]))
        return text
