from lxml import etree
import re
import string
import sys
import unicodedata


class TeiDoc:

    def __init__(self, xml, parser=etree.XMLParser(attribute_defaults=True), nsmap={"tei" : "http://www.tei-c.org/ns/1.0",
                 "vg": "http://www.vangoghletters.org/ns/"}):
        self.nsmap = nsmap
        self.xml = etree.parse(xml, parser)
        self.layers = self.text()

    def metadata(self):
        """
        Extract author, addressee, place the letter was written, date of writing
        returns: dict
        """
        lh = self.xml.getroot().xpath("//tei:teiHeader//tei:sourceDesc/vg:letDesc/vg:letHeading", namespaces=self.nsmap)[0]
        metadata = {"author": lh[0].text,
                    "addressee": lh[1].text,
                    "place": lh[2].text,
                    "date": lh[3].text,
                    "year": int(lh[3].text.split()[-1])
        }

        return metadata

    def mentions(self):
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
        Returns: dict with text layers  and notes
        """
        text_tree = etree.ElementTree(self.xml.find("{http://www.tei-c.org/ns/1.0}text"))
        layers = {}
        for e in text_tree.findall(".//{http://www.tei-c.org/ns/1.0}div"):
            # remove textualNotes
            if e.get("type") == "original":
                try:
                    e.remove(e.findall(".//{http://www.tei-c.org/ns/1.0}div")[0])
                except:
                    # no textualNotes
                    pass
            layers[e.get("type")] = "".join(e.xpath(".//text()"))

        return layers

    def _punctuation(self, text):
        """
        Remove +unicode+ useless stuff. Keep some punctuation for sentence boundary recognition

        """
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
            "'t"    : "het",
            "/"     : ",",
        }

        for k, v in VG_PUNCT.items():
            text = re.sub(k, v, text)
        return text

    def _capitals(self,text):
        "remove caps at the start of a sentence"
        re.sub(r"(\.) ([A-Z])(\w+)", "\g<1> \g")

    def _diacritics(self, text):
        """
        Remove accented or otherwise decorated characters
        """

        return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))

    def preprocess(self):

        return self._punctuation(self._diacritics(self.layers["original"]))
